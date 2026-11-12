# -*- coding: utf-8 -*-
"""
Week 5 evaluation harness.

Re-executes the Week 4 rolling-origin ladder on the real World Bank Pink Sheet
panel and adds the full evaluation suite required by the Week 5 brief:

  * point accuracy        MAE, RMSE, MAPE, sMAPE, MASE, out-of-sample R2
  * bias and direction    mean error, MPE, directional accuracy
  * probabilistic         pinball loss, 90% coverage, interval width, Winkler
  * decision relevance    asymmetric cost-weighted error, procurement regret
  * robustness            bootstrap CIs, Diebold-Mariano tests, MDE, regimes
  * calibration           online conformal residuals at 50/80/90/95%

Outputs are written to week5/data/ and consumed by the report builder.
No synthetic observations are used anywhere.
"""

from __future__ import annotations

import json
import math
import time
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import HistGradientBoostingRegressor
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve().parent
WEEK5 = HERE.parent
DATA = WEEK5 / "data"
DATA.mkdir(parents=True, exist_ok=True)
SOURCE = HERE.parent.parent / "week4" / "data" / "world_bank_agricultural_benchmarks_2000_2026.csv"
WEEK4_SCORECARD = HERE.parent.parent / "week4" / "data" / "notebook_model_scorecard.csv"
WEEK4_LATEST = HERE.parent.parent / "week4" / "data" / "notebook_latest_forecast.csv"

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

HORIZONS = [1, 3, 6, 12]
MAX_H = max(HORIZONS)
MIN_TRAIN = 120
STEP = 3

MODELS = ["L0", "L1", "L2", "L3", "L4", "L5"]
MODEL_LABELS = {
    "L0": "Random Walk",
    "L1": "Seasonal Naive",
    "L2": "ETS",
    "L3": "SARIMAX",
    "L4": "GBDT (direct)",
    "L5": "Ensemble",
}
BASE_MODELS = ["L0", "L1"]
CANDIDATES = ["L2", "L3", "L4"]
EXOG = ["DAP_Fertilizer_USD_MT", "Urea_Fertilizer_USD_MT"]
LAGS = [1, 2, 3, 6, 12]
COST_UNDER = 1.00   # stock-out / missed procurement: full penalty
COST_OVER = 0.25    # carrying / holding cost of over-buying: quarter penalty
MIN_CAL = 8         # folds required before conformal intervals are issued
NOMINAL = [0.50, 0.80, 0.90, 0.95]

_LOGFILE = None


def log(message: str = "") -> None:
    print(message, flush=True)
    if _LOGFILE is not None:
        _LOGFILE.write(message + "\n")
        _LOGFILE.flush()


# --------------------------------------------------------------------------- data
def load_prices() -> pd.DataFrame:
    frame = pd.read_csv(SOURCE)
    frame["Date"] = pd.to_datetime(frame["Date"])
    frame = frame.sort_values("Date").drop_duplicates("Date").reset_index(drop=True)
    frame = frame.loc[frame["Date"] >= "2000-01-01"].reset_index(drop=True)
    expected = pd.date_range(frame["Date"].min(), frame["Date"].max(), freq="MS")
    missing = expected.difference(pd.DatetimeIndex(frame["Date"]))
    assert len(missing) == 0, f"missing months: {missing}"
    assert frame[list(EXOG)].isna().sum().sum() == 0, "fertilizer gaps in modern window"
    return frame


def build_design(frame: pd.DataFrame, target: str):
    """Past-only design matrix; identical construction to the Week 4 notebook."""
    data = frame[["Date", target, *EXOG]].copy().rename(columns={target: "y"})
    data = data.sort_values("Date").reset_index(drop=True)

    for lag in LAGS:
        data[f"y_lag{lag}"] = data["y"].shift(lag)
    for column in EXOG:
        short = "dap" if column.startswith("DAP") else "urea"
        for lag in [0, 1, 3, 6]:
            data[f"{short}_lag{lag}"] = data[column].shift(lag)

    for window in [3, 6, 12]:
        data[f"roll_mean_{window}"] = data["y"].shift(1).rolling(window).mean()
        data[f"roll_std_{window}"] = data["y"].shift(1).rolling(window).std()

    data["ret_1m"] = data["y"].pct_change(1, fill_method=None)
    data["ret_3m"] = data["y"].pct_change(3, fill_method=None)
    data["ret_12m"] = data["y"].pct_change(12, fill_method=None)
    data["mom_3_12"] = data["roll_mean_3"] / data["roll_mean_12"] - 1
    data["yoy_ratio"] = data["y"] / data["y_lag12"] - 1
    data["dap_to_price"] = data["dap_lag0"] / data["y"]
    data["urea_to_price"] = data["urea_lag0"] / data["y"]
    data["drawdown_12"] = data["y"] / data["y"].rolling(12).max() - 1

    month = data["Date"].dt.month
    data["month_sin"] = np.sin(2 * np.pi * month / 12)
    data["month_cos"] = np.cos(2 * np.pi * month / 12)

    data = data.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    features = [c for c in data.columns if c not in ("Date", "y")]
    return data, features


def rolling_origins(n_rows: int, min_train: int = MIN_TRAIN,
                    max_h: int = MAX_H, step: int = STEP) -> list[int]:
    return list(range(min_train - 1, n_rows - max_h, step))


# --------------------------------------------------------------------------- ladder
def run_ladder(data: pd.DataFrame, features: list[str], horizons: list[int],
               min_train: int = MIN_TRAIN, step: int = STEP,
               label: str = "") -> dict:
    y = data["y"].to_numpy(float)
    dates = data["Date"].to_numpy()
    X = data[features].to_numpy(float)
    exog = data[EXOG].to_numpy(float)
    n = len(data)
    max_h = max(horizons)
    origins = rolling_origins(n, min_train=min_train, max_h=max_h, step=step)

    records = []
    running_sq = {h: {k: [] for k in CANDIDATES} for h in horizons}
    failures = {"L2": 0, "L3": 0, "L4": 0}
    expected = {"L2": 0, "L3": 0, "L4": 0}
    fold_log = []

    for fold, origin in enumerate(origins):
        fold_log.append({
            "fold": fold + 1,
            "origin": str(pd.Timestamp(dates[origin]).date()),
            "train_months": int(origin + 1),
            "target_h1": str(pd.Timestamp(dates[min(origin + 1, n - 1)]).date()),
            "target_h12": str(pd.Timestamp(dates[min(origin + max_h, n - 1)]).date()),
        })

        # ---- L0 / L1
        naive = {
            h: {"L0": float(y[origin]), "L1": float(y[origin + h - 12])}
            for h in horizons
        }

        # ---- L2 ETS: one fit, slice the path
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ets = ExponentialSmoothing(
                    y[: origin + 1], trend="add", seasonal="add",
                    seasonal_periods=12, initialization_method="estimated",
                ).fit()
                ets_path = np.asarray(ets.forecast(max_h), float)
        except Exception:
            failures["L2"] += 1
            ets_path = np.repeat(y[origin], max_h)
        expected["L2"] += 1

        # ---- L3 SARIMAX with flat future exog
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sarimax = SARIMAX(
                    y[: origin + 1], exog=exog[: origin + 1],
                    order=(1, 1, 1), seasonal_order=(1, 0, 0, 12),
                    enforce_stationarity=False, enforce_invertibility=False,
                ).fit(disp=False)
                future_exog = np.repeat(exog[origin][None, :], max_h, axis=0)
                sarimax_path = np.asarray(
                    sarimax.forecast(steps=max_h, exog=future_exog), float)
        except Exception:
            failures["L3"] += 1
            sarimax_path = ets_path.copy()
        expected["L3"] += 1

        # ---- L4 direct GBDT per horizon on the log return
        gbdt = {}
        for h in horizons:
            train_end = origin - h
            if train_end < 30:
                gbdt[h] = float(y[origin])
                failures["L4"] += 1
                expected["L4"] += 1
                continue
            rows = np.arange(0, train_end + 1)
            log_return = np.log(y[rows + h] / y[rows])
            model = HistGradientBoostingRegressor(
                max_iter=150, learning_rate=0.06, max_leaf_nodes=15,
                min_samples_leaf=8, l2_regularization=1.0,
                random_state=RANDOM_STATE,
            )
            model.fit(X[rows], log_return)
            step_log = float(np.clip(model.predict(X[origin:origin + 1])[0], -1.0, 1.0))
            gbdt[h] = float(y[origin] * np.exp(step_log))
            expected["L4"] += 1

        # ---- L5 ensemble, past-only inverse-MSE weights
        for h in horizons:
            members = {
                "L2": float(ets_path[h - 1]),
                "L3": float(sarimax_path[h - 1]),
                "L4": float(gbdt[h]),
            }
            if fold == 0:
                weights = np.array([1 / 3, 1 / 3, 1 / 3])
            else:
                mse = np.array([np.mean(running_sq[h][k]) for k in CANDIDATES], float)
                inv = 1.0 / np.maximum(mse, 1e-9)
                weights = inv / inv.sum()
            blend = sum(w * members[k] for w, k in zip(weights, CANDIDATES))

            preds = {**naive[h], **members, "L5": float(blend)}
            for model in MODELS:
                records.append({
                    "commodity": label,
                    "fold": fold + 1,
                    "origin": str(pd.Timestamp(dates[origin]).date()),
                    "target": str(pd.Timestamp(dates[origin + h]).date()),
                    "horizon": h,
                    "model": model,
                    "actual": float(y[origin + h]),
                    "forecast": float(preds[model]),
                    "origin_level": float(y[origin]),
                })

            for k in CANDIDATES:
                running_sq[h][k].append((y[origin + h] - members[k]) ** 2)

        if (fold + 1) % 10 == 0 or fold == 0:
            log(f"    {label or 'series'}: fold {fold + 1:2d}/{len(origins)} "
                f"origin {pd.Timestamp(dates[origin]):%Y-%m}")

    final_weights = {}
    for h in horizons:
        mse = np.array([np.mean(running_sq[h][k]) for k in CANDIDATES], float)
        inv = 1.0 / np.maximum(mse, 1e-9)
        final_weights[h] = (inv / inv.sum()).tolist()

    scale = float(np.mean(np.abs(np.diff(y[:min_train]))))
    fold_frame = pd.DataFrame(records)
    fold_frame = add_conformal_intervals(fold_frame)

    return {
        "folds": fold_frame,
        "origins": origins,
        "scale": scale,
        "n_rows": n,
        "failures": failures,
        "expected": expected,
        "final_weights": final_weights,
        "fold_log": fold_log,
        "dates": dates,
        "y": y,
    }


# --------------------------------------------------------------------------- intervals
def add_conformal_intervals(frame: pd.DataFrame) -> pd.DataFrame:
    """Online conformal residuals: fold k uses errors from folds < k only."""
    frame = frame.copy()
    for level in NOMINAL:
        frame[f"lo{int(level * 100)}"] = np.nan
        frame[f"hi{int(level * 100)}"] = np.nan

    for h in sorted(frame["horizon"].unique()):
        for model in MODELS:
            subset = frame[(frame["horizon"] == h) & (frame["model"] == model)]
            errors: list[float] = []
            for fold in sorted(subset["fold"].unique()):
                mask = (frame["horizon"] == h) & (frame["model"] == model) & (frame["fold"] == fold)
                block = frame.loc[mask]
                if len(errors) >= MIN_CAL:
                    arr = np.asarray(errors, float)
                    for level in NOMINAL:
                        alpha = 1 - level
                        lo_q, hi_q = np.quantile(arr, [alpha / 2, 1 - alpha / 2])
                        frame.loc[mask, f"lo{int(level * 100)}"] = block["forecast"].to_numpy() + lo_q
                        frame.loc[mask, f"hi{int(level * 100)}"] = block["forecast"].to_numpy() + hi_q
                # signed error y - yhat, appended only after intervals are issued
                errors.extend((block["actual"] - block["forecast"]).tolist())
    return frame


# --------------------------------------------------------------------------- metrics
def dm_test(errors_a: np.ndarray, errors_b: np.ndarray, h: int) -> tuple[float, float]:
    """Diebold-Mariano on absolute loss with Harvey-Leybourne-Newbold correction."""
    d = np.abs(errors_a) - np.abs(errors_b)
    n = len(d)
    dbar = float(np.mean(d))
    var = float(np.var(d, ddof=0))
    for lag in range(1, h):
        cov = float(np.mean((d[lag:] - dbar) * (d[:-lag] - dbar)))
        var += 2 * (1 - lag / h) * cov
    if var <= 0:
        return float("nan"), float("nan")
    stat = dbar / math.sqrt(var / n)
    correction = math.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    stat *= correction
    p = 2 * (1 - stats.t.cdf(abs(stat), df=n - 1))
    return float(stat), float(p)


def bootstrap_ci(abs_a: np.ndarray, abs_b: np.ndarray,
                 n_boot: int = 10000) -> tuple[float, float, float]:
    """Paired bootstrap of MAE(a) - MAE(b). Returns diff and 95% interval."""
    rng = np.random.default_rng(RANDOM_STATE)
    n = len(abs_a)
    idx = rng.integers(0, n, size=(n_boot, n))
    diff = abs_a[idx].mean(axis=1) - abs_b[idx].mean(axis=1)
    return float(abs_a.mean() - abs_b.mean()), float(np.quantile(diff, 0.025)), float(np.quantile(diff, 0.975))


def metrics_for(frame: pd.DataFrame, h: int, model: str, scale: float,
                rw_mae: float, sn_mae: float) -> dict:
    block = frame[(frame["horizon"] == h) & (frame["model"] == model)].sort_values("fold")
    y = block["actual"].to_numpy(float)
    f = block["forecast"].to_numpy(float)
    origin = block["origin_level"].to_numpy(float)
    err = y - f
    abs_err = np.abs(err)
    n = len(y)

    mae = float(abs_err.mean())
    rmse = float(np.sqrt(np.mean(err ** 2)))
    p1 = float(np.percentile(np.abs(y), 1))
    mape_guard = bool(p1 >= 5 * mae)
    mape = float(100 * np.mean(abs_err / np.maximum(np.abs(y), 1e-9))) if mape_guard else float("nan")
    smape = float(100 * np.mean(2 * abs_err / (np.abs(y) + np.abs(f) + 1e-9)))
    mase = mae / scale
    mase_rw = mae / rw_mae
    mase_sn = mae / sn_mae
    sst = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - float(np.sum(err ** 2)) / sst if sst > 0 else float("nan")
    bias = float(np.mean(f - y))
    mpe = float(100 * np.mean((f - y) / np.maximum(np.abs(y), 1e-9)))
    if np.allclose(f, origin):
        da = float("nan")
    else:
        da = float(100 * np.mean(np.sign(y - origin) == np.sign(f - origin)))

    has_interval = block["lo90"].notna()
    cov_block = block.loc[has_interval]
    if len(cov_block) > 0:
        yy = cov_block["actual"].to_numpy(float)
        lo = cov_block["lo90"].to_numpy(float)
        hi = cov_block["hi90"].to_numpy(float)
        pin_lo = np.mean(np.where(yy >= lo, 0.05 * (yy - lo), 0.95 * (lo - yy)))
        pin_hi = np.mean(np.where(yy <= hi, 0.95 * (hi - yy), 0.05 * (yy - hi)))
        pinball = float((pin_lo + pin_hi) / 2)
        coverage = float(100 * np.mean((yy >= lo) & (yy <= hi)))
        width = float(np.mean(hi - lo))
        winkler_parts = []
        for a, l, u in zip(yy, lo, hi):
            if a < l:
                winkler_parts.append((u - l) + (2 / 0.10) * (l - a))
            elif a > u:
                winkler_parts.append((u - l) + (2 / 0.10) * (a - u))
            else:
                winkler_parts.append(u - l)
        winkler = float(np.mean(winkler_parts))
    else:
        pinball = coverage = width = winkler = float("nan")

    asymmetric = float(np.mean(COST_UNDER * np.maximum(err, 0) + COST_OVER * np.maximum(-err, 0)))
    mean_price = float(np.mean(y))
    gate = "baseline" if model in BASE_MODELS else (
        "PASS" if (mase_rw < 1.0 and mase_sn < 1.0) else "fail")

    return {
        "horizon": h,
        "model": MODEL_LABELS[model],
        "model_key": model,
        "n_folds": n,
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "mape_guard": mape_guard,
        "p1_actual": p1,
        "smape": smape,
        "mase": mase,
        "mase_rw": mase_rw,
        "mase_sn": mase_sn,
        "r2": r2,
        "bias": bias,
        "mpe": mpe,
        "da": da,
        "pinball": pinball,
        "coverage90": coverage,
        "width90": width,
        "winkler90": winkler,
        "cwe": asymmetric,
        "cwe_pct": 100 * asymmetric / mean_price,
        "worst_abs": float(abs_err.max()),
        "sd_abs": float(abs_err.std(ddof=1)),
        "mean_price": mean_price,
        "gate": gate,
    }


def build_metrics(frame: pd.DataFrame, scale: float) -> pd.DataFrame:
    rows = []
    for h in HORIZONS:
        block = frame[frame["horizon"] == h]
        rw = block[block["model"] == "L0"].set_index("fold")["forecast"]
        sn = block[block["model"] == "L1"].set_index("fold")["forecast"]
        actual = block[block["model"] == "L0"].set_index("fold")["actual"]
        rw_mae = float(np.mean(np.abs(actual - rw)))
        sn_mae = float(np.mean(np.abs(actual - sn)))
        for model in MODELS:
            rows.append(metrics_for(frame, h, model, scale, rw_mae, sn_mae))
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- analyses
def calibration_table(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for h in HORIZONS:
        for model in MODELS:
            block = frame[(frame["horizon"] == h) & (frame["model"] == model)]
            for level in NOMINAL:
                col_lo, col_hi = f"lo{int(level * 100)}", f"hi{int(level * 100)}"
                sub = block.dropna(subset=[col_lo, col_hi])
                if sub.empty:
                    continue
                inside = (sub["actual"] >= sub[col_lo]) & (sub["actual"] <= sub[col_hi])
                rows.append({
                    "horizon": h, "model": MODEL_LABELS[model], "model_key": model,
                    "nominal": int(level * 100),
                    "empirical": float(100 * inside.mean()),
                    "width": float((sub[col_hi] - sub[col_lo]).mean()),
                    "n": int(len(sub)),
                })
    return pd.DataFrame(rows)


def significance_table(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for h in HORIZONS:
        block = frame[frame["horizon"] == h]
        rw = block[block["model"] == "L0"].set_index("fold")
        for model in MODELS[2:]:
            other = block[block["model"] == model].set_index("fold")
            # Join only the point-forecast columns. Keeping interval columns here
            # would silently drop the conformal warm-up folds (8 of 60 at h=1)
            # from every significance test, so the test sample would no longer
            # match the scorecard it is meant to qualify.
            joined = rw[["actual", "forecast"]].join(
                other[["actual", "forecast"]], lsuffix="_rw", rsuffix="_m",
                how="inner").dropna()
            abs_rw = (joined["actual_rw"] - joined["forecast_rw"]).abs().to_numpy()
            abs_m = (joined["actual_m"] - joined["forecast_m"]).abs().to_numpy()
            diff, lo, hi = bootstrap_ci(abs_m, abs_rw)
            stat, p = dm_test(joined["actual_m"].to_numpy() - joined["forecast_m"].to_numpy(),
                              joined["actual_rw"].to_numpy() - joined["forecast_rw"].to_numpy(), h)
            se = float(np.std(abs_m - abs_rw, ddof=1) / math.sqrt(len(abs_rw)))
            rows.append({
                "horizon": h, "model": MODEL_LABELS[model], "model_key": model,
                "mae_diff_vs_rw": diff,
                "ci_lo": lo, "ci_hi": hi,
                "mae_diff_pct": 100 * diff / abs_rw.mean(),
                "dm_stat": stat, "dm_p": p,
                "mde": 2.802 * se,
                "mde_pct": 100 * 2.802 * se / abs_rw.mean(),
                "n": len(abs_rw),
            })
    return pd.DataFrame(rows)


def regime_table(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    frame = frame.copy()
    frame["period"] = np.where(pd.to_datetime(frame["target"]) < pd.Timestamp("2023-01-01"),
                               "2010-2022", "2023-2026")
    for h in HORIZONS:
        for model in ["L3", "L5"]:
            for period in ["2010-2022", "2023-2026"]:
                block = frame[(frame["horizon"] == h) & (frame["model"] == model) &
                              (frame["period"] == period)]
                rw = frame[(frame["horizon"] == h) & (frame["model"] == "L0") &
                           (frame["period"] == period)]
                if block.empty:
                    continue
                mae = float(np.mean(np.abs(block["actual"] - block["forecast"])))
                rw_mae = float(np.mean(np.abs(rw["actual"] - rw["forecast"])))
                rows.append({
                    "horizon": h, "model": MODEL_LABELS[model], "model_key": model,
                    "period": period, "folds": int(len(block)),
                    "mae": mae, "rw_mae": rw_mae, "mase_rw": mae / rw_mae,
                })
    return pd.DataFrame(rows)


def volatility_table(frame: pd.DataFrame, design: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    vol = design.set_index("Date")["roll_std_12"] / design.set_index("Date")["roll_mean_12"]
    frame["origin_dt"] = pd.to_datetime(frame["origin"])
    frame["vol"] = frame["origin_dt"].map(vol)
    rows = []
    for h in HORIZONS:
        sub = frame[frame["horizon"] == h].copy()
        edges = sub["vol"].quantile([1 / 3, 2 / 3]).to_numpy()
        sub["bucket"] = np.where(sub["vol"] <= edges[0], "Low volatility",
                                 np.where(sub["vol"] <= edges[1], "Mid volatility", "High volatility"))
        for bucket in ["Low volatility", "Mid volatility", "High volatility"]:
            for model in ["L5"]:
                block = sub[(sub["bucket"] == bucket) & (sub["model"] == model)]
                rw = sub[(sub["bucket"] == bucket) & (sub["model"] == "L0")]
                mae = float(np.mean(np.abs(block["actual"] - block["forecast"])))
                rw_mae = float(np.mean(np.abs(rw["actual"] - rw["forecast"])))
                rows.append({
                    "horizon": h, "bucket": bucket, "folds": int(len(block)),
                    "mae": mae, "rw_mae": rw_mae, "mase_rw": mae / rw_mae,
                })
    return pd.DataFrame(rows)


def decision_table(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Procurement rule at h=1: lock the price if the forecast rise exceeds tau."""
    block = frame[(frame["horizon"] == 1) & (frame["model"] == "L5")].sort_values("fold")
    y0 = block["origin_level"].to_numpy(float)
    y1 = block["actual"].to_numpy(float)
    f1 = block["forecast"].to_numpy(float)
    signal = f1 / y0 - 1

    perfect = float(np.mean(np.minimum(y0, y1)))
    always_wait = float(np.mean(y1))
    always_buy = float(np.mean(y0))

    rows = []
    for tau in np.round(np.arange(-0.03, 0.0601, 0.001), 4):
        buy = signal > tau
        cost = np.where(buy, y0, y1)
        hit = float(np.mean(y1[buy] > y0[buy])) if buy.any() else float("nan")
        capture = float(np.sum((y1 - y0)[buy] < 0) / max(np.sum(y1 < y0), 1))
        rows.append({
            "tau": float(tau), "share_buy": float(100 * buy.mean()),
            "mean_cost": float(cost.mean()),
            "regret": float(cost.mean() - perfect),
            "regret_pct": float(100 * (cost.mean() - perfect) / perfect),
            "hit_rate": 100 * hit if not math.isnan(hit) else float("nan"),
            "rises_captured": 100 * capture,
        })
    table = pd.DataFrame(rows)
    best = table.loc[table["mean_cost"].idxmin()]
    summary = {
        "perfect": perfect,
        "always_wait": always_wait,
        "always_buy": always_buy,
        "best_tau": float(best["tau"]),
        "best_cost": float(best["mean_cost"]),
        "best_regret": float(best["regret"]),
        "best_regret_pct": float(best["regret_pct"]),
        "always_wait_regret": always_wait - perfect,
        "always_wait_regret_pct": 100 * (always_wait - perfect) / perfect,
    }
    return table, summary


def latest_forecast(design: pd.DataFrame, features: list[str], weights: dict) -> pd.DataFrame:
    """Fit the ladder at the final origin and issue conformal interval bands."""
    y = design["y"].to_numpy(float)
    X = design[features].to_numpy(float)
    exog = design[EXOG].to_numpy(float)
    origin = len(y) - 1
    dates = design["Date"].to_numpy()

    ets = ExponentialSmoothing(
        y, trend="add", seasonal="add", seasonal_periods=12,
        initialization_method="estimated").fit()
    ets_path = np.asarray(ets.forecast(MAX_H), float)

    sarimax = SARIMAX(
        y, exog=exog, order=(1, 1, 1), seasonal_order=(1, 0, 0, 12),
        enforce_stationarity=False, enforce_invertibility=False,
    ).fit(disp=False)
    future_exog = np.repeat(exog[-1][None, :], MAX_H, axis=0)
    sarimax_path = np.asarray(sarimax.forecast(steps=MAX_H, exog=future_exog), float)

    rows = []
    for h in HORIZONS:
        train_end = origin - h
        rows_idx = np.arange(0, train_end + 1)
        log_return = np.log(y[rows_idx + h] / y[rows_idx])
        model = HistGradientBoostingRegressor(
            max_iter=150, learning_rate=0.06, max_leaf_nodes=15,
            min_samples_leaf=8, l2_regularization=1.0, random_state=RANDOM_STATE)
        model.fit(X[rows_idx], log_return)
        step_log = float(np.clip(model.predict(X[origin:origin + 1])[0], -1.0, 1.0))
        gbdt = float(y[origin] * np.exp(step_log))
        members = [float(ets_path[h - 1]), float(sarimax_path[h - 1]), gbdt]
        w = weights.get(str(h), weights.get(h))
        point = sum(wi * mi for wi, mi in zip(w, members))
        rows.append({
            "horizon": h,
            "target": str((pd.Timestamp(dates[origin]) + pd.DateOffset(months=h)).date()),
            "origin": str(pd.Timestamp(dates[origin]).date()),
            "forecast": point,
            "ets": members[0], "sarimax": members[1], "gbdt": members[2],
            "w_ets": w[0], "w_sarimax": w[1], "w_gbdt": w[2],
        })
    return pd.DataFrame(rows)


def add_latest_bands(fan: pd.DataFrame, folds: pd.DataFrame) -> pd.DataFrame:
    fan = fan.copy()
    for level in NOMINAL:
        fan[f"lo{int(level * 100)}"] = np.nan
        fan[f"hi{int(level * 100)}"] = np.nan
    for i, row in fan.iterrows():
        h = int(row["horizon"])
        err = (folds[(folds["horizon"] == h) & (folds["model"] == "L5")]["actual"] -
               folds[(folds["horizon"] == h) & (folds["model"] == "L5")]["forecast"]).to_numpy()
        for level in NOMINAL:
            alpha = 1 - level
            lo, hi = np.quantile(err, [alpha / 2, 1 - alpha / 2])
            fan.loc[i, f"lo{int(level * 100)}"] = row["forecast"] + lo
            fan.loc[i, f"hi{int(level * 100)}"] = row["forecast"] + hi
    return fan


# --------------------------------------------------------------------------- main
def main() -> None:
    global _LOGFILE
    _LOGFILE = open(DATA / "run_log.txt", "w", encoding="utf-8")
    started = time.time()
    log("=" * 78)
    log("WEEK 5 EVALUATION HARNESS")
    log(f"started {datetime.now():%Y-%m-%d %H:%M:%S}")
    log("=" * 78)

    prices = load_prices()
    log(f"source      : {SOURCE}")
    log(f"prices      : {len(prices)} months, {prices['Date'].min():%Y-%m} to {prices['Date'].max():%Y-%m}")

    design, features = build_design(prices, "Wheat_HRW_USD_MT")
    log(f"design      : {len(design)} usable months x {len(features)} predictors")
    log(f"origins     : {len(rolling_origins(len(design)))} folds, step {STEP} months, min train {MIN_TRAIN}")

    log("\n[1/7] Running the primary wheat ladder ...")
    wheat = run_ladder(design, features, HORIZONS, label="Wheat")
    wheat["folds"].to_csv(DATA / "fold_predictions_wheat.csv", index=False)
    wheat["folds"].to_csv(DATA / "fold_predictions_wheat_primary.csv", index=False)
    pd.DataFrame(wheat["fold_log"]).to_csv(DATA / "folds.csv", index=False)
    log(f"    predictions: {len(wheat['folds']):,} rows")
    log(f"    failures   : {wheat['failures']} of {wheat['expected']}")

    metrics = build_metrics(wheat["folds"], wheat["scale"])
    metrics.to_csv(DATA / "metrics_by_horizon.csv", index=False)
    pd.DataFrame(
        [{"horizon": h, "w_ets": w[0], "w_sarimax": w[1], "w_gbdt": w[2]}
         for h, w in wheat["final_weights"].items()]
    ).to_csv(DATA / "final_weights.csv", index=False)
    log(f"    metrics rows: {len(metrics)}")

    log("\n[2/7] Calibration ...")
    cal = calibration_table(wheat["folds"])
    cal.to_csv(DATA / "calibration.csv", index=False)

    log("\n[3/7] Significance and power ...")
    sig = significance_table(wheat["folds"])
    sig.to_csv(DATA / "significance.csv", index=False)

    log("\n[4/7] Regime and volatility segments ...")
    regime = regime_table(wheat["folds"])
    regime.to_csv(DATA / "regime_metrics.csv", index=False)
    vol = volatility_table(wheat["folds"], design)
    vol.to_csv(DATA / "volatility_metrics.csv", index=False)

    log("\n[5/7] Decision analysis ...")
    decision, decision_summary = decision_table(wheat["folds"])
    decision.to_csv(DATA / "decision_curve.csv", index=False)

    log("\n[6/7] Cross-commodity replication ...")
    cross_rows = []
    for commodity, column in [
        ("Wheat", "Wheat_HRW_USD_MT"),
        ("Rice", "Rice_Thai_USD_MT"),
        ("Maize", "Maize_USD_MT"),
        ("Soybeans", "Soybeans_USD_MT"),
        ("Cotton", "Cotton_AIndex_USD_MT"),
    ]:
        d, f = build_design(prices, column)
        result = run_ladder(d, f, HORIZONS, step=4, label=commodity)
        m = build_metrics(result["folds"], result["scale"])
        m["commodity"] = commodity
        cross_rows.append(m)
        result["folds"].to_csv(DATA / f"fold_predictions_cross_{commodity.lower()}.csv", index=False)
    cross = pd.concat(cross_rows, ignore_index=True)
    cross.to_csv(DATA / "metrics_by_commodity.csv", index=False)

    log("\n[7/7] Latest forecast and band construction ...")
    fan = latest_forecast(design, features, wheat["final_weights"])
    fan = add_latest_bands(fan, wheat["folds"])
    fan.to_csv(DATA / "latest_forecast.csv", index=False)

    # ---- compact facts for the report builder
    def row(h: int, key: str) -> dict:
        return metrics[(metrics["horizon"] == h) & (metrics["model_key"] == key)].iloc[0].to_dict()

    headline = {}
    for h in HORIZONS:
        candidates = metrics[(metrics["horizon"] == h) & (~metrics["model_key"].isin(BASE_MODELS))]
        best = candidates.sort_values("mae").iloc[0]
        headline[str(h)] = row(h, best["model_key"])

    reconciliation = {}
    if WEEK4_SCORECARD.exists():
        prior = pd.read_csv(WEEK4_SCORECARD)
        prior = prior[prior["Model"].str.contains("Ensemble|SARIMAX", regex=True)]
        rec_rows = []
        for _, r in prior.iterrows():
            rec_rows.append({
                "horizon": int(r["Horizon"]),
                "model": r["Model"],
                "week4_mae": float(r["MAE"]),
                "week4_mase_rw": float(r["MASE vs RW"]),
                "week4_gate": r["Gate"],
            })
        reconciliation["week4"] = rec_rows

    # reproduce check: compare my L5 MAE with the Week 4 scorecard
    reproduce = []
    if WEEK4_SCORECARD.exists():
        prior = pd.read_csv(WEEK4_SCORECARD)
        for h in HORIZONS:
            p = prior[(prior["Horizon"] == h) & (prior["Model"].str.contains("Ensemble"))].iloc[0]
            mine = row(h, "L5")
            reproduce.append({
                "horizon": h,
                "week4_mae": float(p["MAE"]),
                "week5_mae": mine["mae"],
                "delta_pct": 100 * (mine["mae"] - float(p["MAE"])) / float(p["MAE"]),
                "week4_mase": float(p["MASE vs RW"]),
                "week5_mase": mine["mase_rw"],
            })

    facts = {
        "meta": {
            "generated": datetime.now().isoformat(timespec="seconds"),
            "source": str(SOURCE),
            "data_start": str(prices["Date"].min().date()),
            "data_end": str(prices["Date"].max().date()),
            "n_months": int(len(prices)),
            "n_design": int(len(design)),
            "n_features": int(len(features)),
            "n_folds": int(wheat["folds"]["fold"].nunique()),
            "step": STEP,
            "min_train": MIN_TRAIN,
            "horizons": HORIZONS,
            "scale": wheat["scale"],
            "failures": wheat["failures"],
            "expected": wheat["expected"],
            "runtime_seconds": round(time.time() - started, 1),
            "final_weights": wheat["final_weights"],
        },
        "scorecard": metrics.round(6).to_dict(orient="records"),
        "headline": {k: {kk: (None if isinstance(vv, float) and math.isnan(vv) else vv)
                         for kk, vv in v.items()} for k, v in headline.items()},
        "calibration": cal.round(6).to_dict(orient="records"),
        "significance": sig.round(6).to_dict(orient="records"),
        "regime": regime.round(6).to_dict(orient="records"),
        "volatility": vol.round(6).to_dict(orient="records"),
        "decision": decision.round(6).to_dict(orient="records"),
        "decision_summary": decision_summary,
        "cross_commodity": cross.round(6).to_dict(orient="records"),
        "latest": fan.round(6).to_dict(orient="records"),
        "reconciliation": reconciliation,
        "reproduce": reproduce,
    }

    def clean(obj):
        if isinstance(obj, dict):
            return {k: clean(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [clean(v) for v in obj]
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
        if isinstance(obj, float) and math.isnan(obj):
            return None
        return obj

    with open(DATA / "facts.json", "w", encoding="utf-8") as handle:
        json.dump(clean(facts), handle, indent=2)

    log("\n" + "=" * 78)
    log("HEADLINE (wheat, best candidate per horizon)")
    for h in HORIZONS:
        hd = headline[str(h)]
        log(f"  h={h:2d}: {hd['model']:14s} MAE {hd['mae']:7.2f} | "
            f"MASE/RW {hd['mase_rw']:.3f} | gate {hd['gate']:8s} | "
            f"cover90 {hd['coverage90']:.1f}% | DA {hd['da']:.1f}%")
    log("\nCROSS-COMMODITY (h=3, best per crop)")
    for commodity in ["Wheat", "Rice", "Maize", "Soybeans", "Cotton"]:
        sub = cross[(cross["commodity"] == commodity) & (cross["horizon"] == 3) &
                    (~cross["model_key"].isin(BASE_MODELS))]
        best = sub.sort_values("mae").iloc[0]
        log(f"  {commodity:9s} {best['model']:10s} MASE/RW {best['mase_rw']:.3f} "
            f"gate {best['gate']}")
    log(f"\nlatest forecast: {fan[['horizon', 'forecast']].to_dict(orient='records')}")
    log(f"decision optimum tau: {decision_summary['best_tau']:.3f} "
        f"regret {decision_summary['best_regret_pct']:.2f}%")
    log(f"finished in {time.time() - started:.1f}s")
    log("=" * 78)
    _LOGFILE.close()


if __name__ == "__main__":
    main()
