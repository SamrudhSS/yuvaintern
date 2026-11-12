# -*- coding: utf-8 -*-
"""Load the executed Week 5 evaluation facts and expose report helpers."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

with open(DATA / "facts.json", "r", encoding="utf-8") as _handle:
    FACTS = json.load(_handle)

META = FACTS["meta"]
SCORECARD = pd.DataFrame(FACTS["scorecard"])
CALIBRATION = pd.DataFrame(FACTS["calibration"])
SIGNIFICANCE = pd.DataFrame(FACTS["significance"])
REGIME = pd.DataFrame(FACTS["regime"])
VOLATILITY = pd.DataFrame(FACTS["volatility"])
DECISION = pd.DataFrame(FACTS["decision"])
DECISION_SUMMARY = FACTS["decision_summary"]
CROSS = pd.DataFrame(FACTS["cross_commodity"])
LATEST = pd.DataFrame(FACTS["latest"])
WEEK4 = pd.DataFrame(FACTS.get("reconciliation", {}).get("week4", []))
REPRODUCE = pd.DataFrame(FACTS.get("reproduce", []))

HORIZONS = [1, 3, 6, 12]
MODEL_ORDER = ["Random Walk", "Seasonal Naive", "ETS", "SARIMAX", "GBDT (direct)", "Ensemble"]
MODEL_KEYS = {"Random Walk": "L0", "Seasonal Naive": "L1", "ETS": "L2",
              "SARIMAX": "L3", "GBDT (direct)": "L4", "Ensemble": "L5"}
SHORT = {"Random Walk": "RW", "Seasonal Naive": "SN", "ETS": "ETS",
         "SARIMAX": "SARIMAX", "GBDT (direct)": "GBDT", "Ensemble": "ENS"}
CROPS = ["Wheat", "Rice", "Maize", "Soybeans", "Cotton"]


def score(horizon: int, model: str) -> dict:
    key = MODEL_KEYS.get(model, model)
    row = SCORECARD[(SCORECARD["horizon"] == horizon) & (SCORECARD["model_key"] == key)]
    return row.iloc[0].to_dict()


def head(horizon: int) -> dict:
    return FACTS["headline"][str(horizon)]


def cross_score(commodity: str, horizon: int, model: str = "best") -> dict:
    block = CROSS[(CROSS["commodity"] == commodity) & (CROSS["horizon"] == horizon)]
    candidates = block[~block["model_key"].isin(["L0", "L1"])]
    if model == "best":
        return candidates.sort_values("mae").iloc[0].to_dict()
    row = block[block["model_key"] == MODEL_KEYS.get(model, model)]
    return row.iloc[0].to_dict()


def cross_best_per_commodity(horizon: int) -> pd.DataFrame:
    rows = []
    for crop in CROPS:
        rows.append(cross_score(crop, horizon))
    return pd.DataFrame(rows)


def pooled_mase(horizon: int) -> float:
    """MAE pooled over commodities, divided by pooled random-walk MAE."""
    block = CROSS[CROSS["horizon"] == horizon]
    best = []
    for crop in CROPS:
        best.append(cross_score(crop, horizon))
    best = pd.DataFrame(best)
    baseline = pd.DataFrame([cross_score(crop, horizon, "Random Walk") for crop in CROPS])
    num = float((best["mae"] * best["n_folds"]).sum())
    den = float((baseline["mae"] * best["n_folds"]).sum())
    return num / den


def calibration(horizon: int, model: str) -> pd.DataFrame:
    return CALIBRATION[(CALIBRATION["horizon"] == horizon) &
                       (CALIBRATION["model"] == model)].sort_values("nominal")


def sig(horizon: int, model: str) -> dict:
    key = MODEL_KEYS.get(model, model)
    row = SIGNIFICANCE[(SIGNIFICANCE["horizon"] == horizon) &
                       (SIGNIFICANCE["model_key"] == key)]
    return row.iloc[0].to_dict()


def regime_row(horizon: int, model: str, period: str) -> dict:
    key = MODEL_KEYS.get(model, model)
    row = REGIME[(REGIME["horizon"] == horizon) & (REGIME["model_key"] == key) &
                 (REGIME["period"] == period)]
    return row.iloc[0].to_dict()


def vol_rows(horizon: int) -> pd.DataFrame:
    return VOLATILITY[VOLATILITY["horizon"] == horizon]


def num(value, digits: int = 2, dash: str = "—") -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return dash
    return f"{value:,.{digits}f}"


def pct(value, digits: int = 1, dash: str = "—") -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return dash
    return f"{value:,.{digits}f}%"


def signed(value, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    return f"{value:+,.{digits}f}"


def gate(g: str) -> str:
    return {"PASS": "✓ PASS", "fail": "✗ FAIL", "baseline": "★ baseline"}.get(g, g)


def gate_count() -> tuple[int, int]:
    rows = SCORECARD[~SCORECARD["model_key"].isin(["L0", "L1"])]
    return int((rows["gate"] == "PASS").sum()), int(len(rows))


def cross_gate_count(horizon: int) -> tuple[int, int]:
    passed = 0
    for crop in CROPS:
        row = cross_score(crop, horizon)
        passed += int(row["gate"] == "PASS")
    return passed, len(CROPS)


def best_overall(horizon: int) -> dict:
    return head(horizon)


def reproduce_max_delta() -> float:
    if REPRODUCE.empty:
        return float("nan")
    return float(REPRODUCE["delta_pct"].abs().max())


def latest_row(horizon: int) -> dict:
    row = LATEST[LATEST["horizon"] == horizon]
    return row.iloc[0].to_dict()


def decision_at(tau: float) -> dict:
    idx = (DECISION["tau"] - tau).abs().idxmin()
    return DECISION.loc[idx].to_dict()


def calibration_summary() -> dict:
    rows = CALIBRATION[CALIBRATION["model"].isin(["Random Walk", "Ensemble"])]
    out = {}
    for model in ["Random Walk", "Ensemble"]:
        block = rows[rows["model"] == model]
        out[model] = {
            "mean_gap": float((block["empirical"] - block["nominal"]).abs().mean()),
            "worst_gap": float((block["empirical"] - block["nominal"]).abs().max()),
        }
    return out
