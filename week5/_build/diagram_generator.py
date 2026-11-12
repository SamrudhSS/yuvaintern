# -*- coding: utf-8 -*-
"""Render the Week 5 evaluation figures from executed outputs."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from scipy.interpolate import PchipInterpolator
from statsmodels.tsa.stattools import acf

import facts as F

HERE = Path(__file__).resolve().parent
FIGS = HERE / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
DATA = HERE.parent / "data"

PRIMARY = "#1B4332"
SECONDARY = "#2D6A4F"
ACCENT = "#B5651D"
BLUE = "#2471A3"
RED = "#B03A2E"
GREY = "#7F8C8D"
LIGHT = "#E8EFE9"
PALE = "#F4F8F5"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.titlecolor": PRIMARY,
    "axes.labelsize": 9,
    "axes.labelcolor": "#34443B",
    "axes.edgecolor": "#B9C6BC",
    "axes.linewidth": 0.9,
    "axes.grid": True,
    "grid.color": "#DDE6DF",
    "grid.linewidth": 0.7,
    "legend.frameon": False,
    "legend.fontsize": 8,
    "xtick.color": "#4D5B53",
    "ytick.color": "#4D5B53",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def _clean(ax, left=True, bottom=True):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if not left:
        ax.spines["left"].set_visible(False)
    if not bottom:
        ax.spines["bottom"].set_visible(False)


def _source(fig, text):
    fig.text(0.01, 0.008, text, fontsize=6.4, color=GREY, ha="left")


def fig_architecture():
    fig, ax = plt.subplots(figsize=(13.6, 5.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    stages = [
        ("1", "EVIDENCE", "Frozen folds\nReal prices, no leakage\nReproducible artefacts",
         "#1B4332"),
        ("2", "METRICS", "Accuracy, calibration\ndirection, stability\nand decision cost", "#2D6A4F"),
        ("3", "TESTS", "Paired bootstrap\nDiebold-Mariano\nPower and MDE", "#3E7C59"),
        ("4", "PICTURES", "One message per chart\nAudience-matched\nUncertainty visible", "#B5651D"),
        ("5", "DECISIONS", "Use, limit or reject\nNamed owner\nReview date", "#8A4B16"),
    ]
    box_w, gap = 16.2, 5.2
    x = 2.2
    for i, (number, title, body, color) in enumerate(stages):
        x0 = x + i * (box_w + gap)
        box = FancyBboxPatch((x0, 32), box_w, 46, boxstyle="round,pad=0.4,rounding_size=1.4",
                             linewidth=0, facecolor=PALE, zorder=1)
        ax.add_patch(box)
        band = FancyBboxPatch((x0, 68), box_w, 10, boxstyle="round,pad=0.4,rounding_size=1.4",
                              linewidth=0, facecolor=color, zorder=2)
        ax.add_patch(band)
        ax.text(x0 + box_w / 2, 73, f"{number}   {title}", ha="center", va="center",
                color="white", fontsize=9.5, fontweight="bold", zorder=3)
        ax.text(x0 + box_w / 2, 52, body, ha="center", va="center", color="#24352C",
                fontsize=8.2, linespacing=1.45, zorder=3)
        if i < len(stages) - 1:
            arrow = FancyArrowPatch((x0 + box_w + 0.5, 55), (x0 + box_w + gap - 0.5, 55),
                                    arrowstyle="-|>", mutation_scale=14, linewidth=1.4,
                                    color="#8A9A8F", zorder=4)
            ax.add_patch(arrow)

    ax.text(50, 91, "Evaluation is a production line, not a verdict",
            ha="center", va="center", fontsize=15, fontweight="bold", color=PRIMARY)
    ax.text(50, 84.5, "Every stage has an owner, an artefact and a gate; a failure at any stage stops publication",
            ha="center", va="center", fontsize=9.2, color=GREY)

    ax.text(50, 21, "GATE 1  no leakage        GATE 2  benchmark beaten        GATE 3  effect is real        "
                    "GATE 4  message survives a non-expert",
            ha="center", va="center", fontsize=7.6, color=ACCENT, fontweight="bold")
    ax.text(50, 10, "Reported to the decision owner with a range, a benchmark and a stated failure condition",
            ha="center", va="center", fontsize=8.4, color="#34443B", style="italic")
    _source(fig, "Week 5 evaluation architecture. Executed against World Bank Pink Sheet data, 2000-01 to 2026-10.")
    fig.savefig(FIGS / "evaluation_architecture.png")
    plt.close(fig)


def fig_heatmap():
    pivot = F.SCORECARD.pivot(index="model", columns="horizon", values="mase_rw")
    gates = F.SCORECARD.pivot(index="model", columns="horizon", values="gate")
    pivot = pivot.reindex(F.MODEL_ORDER)
    gates = gates.reindex(F.MODEL_ORDER)
    data = pivot.to_numpy(float)

    fig, ax = plt.subplots(figsize=(10.6, 4.5))
    norm = TwoSlopeNorm(vmin=0.90, vcenter=1.0, vmax=1.30)
    cmap = plt.get_cmap("RdYlGn_r")
    im = ax.imshow(data, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([f"h = {h} month{'s' if h > 1 else ''}" for h in pivot.columns])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([f"{m}" for m in pivot.index])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    for i, model in enumerate(pivot.index):
        for j, h in enumerate(pivot.columns):
            value = data[i, j]
            gate = gates.loc[model, h]
            mark = "★" if gate == "baseline" else ("✓" if gate == "PASS" else "✗")
            color = "white" if value > 1.14 or value < 0.93 else "#16241C"
            ax.text(j, i - 0.10, f"{value:.3f}", ha="center", va="center",
                    fontsize=9.4, fontweight="bold", color=color)
            ax.text(j, i + 0.20, mark, ha="center", va="center",
                    fontsize=8.5, color=color)
    ax.set_title("MASE against the random walk, by model and horizon", loc="left", pad=12)
    ax.text(1.0, 1.035, "1.000 = no better than a random walk",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color=GREY)

    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("MASE vs RW", fontsize=8)
    cbar.ax.tick_params(labelsize=7.5)
    cbar.outline.set_visible(False)

    fig.subplots_adjust(bottom=0.18)
    fig.text(0.01, 0.045, "★ = benchmark    ✓ = beats both benchmarks    ✗ = fails the gate",
             fontsize=7.6, color="#4D5B53")
    _source(fig, "Source: Week 5 evaluation harness on World Bank Pink Sheet wheat prices. 60 folds, step 3 months, 2010-12 to 2025-09 origins.")
    fig.savefig(FIGS / "scorecard_heatmap.png")
    plt.close(fig)


def _fan_paths():
    latest = F.LATEST.sort_values("horizon")
    hs = latest["horizon"].to_numpy(float)
    grid = np.arange(1, 13)
    point = PchipInterpolator(hs, latest["forecast"].to_numpy(float))(grid)

    levels = {}
    for level in (50, 80, 90):
        lo_off = PchipInterpolator(hs, latest[f"lo{level}"].to_numpy(float) - latest["forecast"].to_numpy(float))(grid)
        hi_off = PchipInterpolator(hs, latest[f"hi{level}"].to_numpy(float) - latest["forecast"].to_numpy(float))(grid)
        levels[level] = (point + lo_off, point + hi_off)
    return grid, point, levels


def fig_fan():
    prices = pd.read_csv(HERE.parent.parent / "week4" / "data" / "world_bank_agricultural_benchmarks_2000_2026.csv",
                         parse_dates=["Date"])
    prices = prices[prices["Date"] >= "2018-01-01"]
    grid, point, bands = _fan_paths()
    origin = pd.Timestamp(F.LATEST["origin"].iloc[0])
    future = pd.date_range(origin + pd.offsets.MonthBegin(1), periods=12, freq="MS")
    hist = prices[prices["Date"] <= origin]

    fig, ax = plt.subplots(figsize=(11.6, 5.2))
    ax.plot(hist["Date"], hist["Wheat_HRW_USD_MT"], color=PRIMARY, lw=1.9, label="Wheat, US HRW (actual)")
    ax.plot([origin], [hist["Wheat_HRW_USD_MT"].iloc[-1]], "o", color=PRIMARY, ms=5, zorder=5)
    ax.plot(future, point, color=ACCENT, lw=2.1, label="Ensemble forecast")
    for level, alpha, label in ((90, 0.16, "90% band"), (80, 0.22, "80% band"), (50, 0.30, "50% band")):
        lo, hi = bands[level]
        ax.fill_between(future, lo, hi, color=ACCENT, alpha=alpha, linewidth=0,
                        label=label)
    ax.axvline(origin, color=GREY, ls=(0, (3, 3)), lw=1)
    ax.text(origin, ax.get_ylim()[1], " forecast origin\n Oct 2026", va="top", ha="left",
            fontsize=7.6, color=GREY)

    last_actual = float(hist["Wheat_HRW_USD_MT"].iloc[-1])
    f12 = float(point[-1])
    ax.annotate(f"12-month point\n{f12:,.0f} USD/MT",
                xy=(future[-1], f12), xytext=(-62, -34), textcoords="offset points",
                fontsize=8, color=ACCENT, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.8))
    ax.set_ylabel("USD / metric ton")
    ax.set_title("What the forecast actually claims: a range, not a number", loc="left", pad=12)
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(pd.Timestamp("2018-01-01"), future[-1] + pd.DateOffset(months=2))
    ax.legend(loc="upper left", ncol=2, fontsize=7.6)
    _clean(ax)
    _source(fig, f"Last actual {last_actual:,.1f} USD/MT (Oct 2026). Bands are conformal 50/80/90% intervals from 60 backtest folds; path interpolated between the four evaluated horizons.")
    fig.savefig(FIGS / "fan_chart.png")
    plt.close(fig)


def fig_predicted_actual():
    folds = pd.read_csv(DATA / "fold_predictions_wheat.csv", parse_dates=["target"])
    fig, axes = plt.subplots(2, 1, figsize=(11.6, 6.6), sharex=True)
    for ax, h in zip(axes, [1, 12]):
        block = folds[(folds["horizon"] == h) & (folds["model"] == "L5")].sort_values("target")
        block = block[block["target"] >= "2019-01-01"]
        ax.plot(block["target"], block["actual"], color=PRIMARY, lw=1.8, label="Actual")
        ax.plot(block["target"], block["forecast"], color=ACCENT, lw=1.5, ls="--", label="Forecast")
        ax.fill_between(block["target"], block["actual"], block["forecast"],
                        color=ACCENT, alpha=0.12, linewidth=0, label="Absolute error")
        mae = float(np.mean(np.abs(block["actual"] - block["forecast"])))
        ax.set_title(f"h = {h} month{'s' if h > 1 else ''} ahead  ·  MAE {mae:,.1f} USD/MT",
                     loc="left", fontsize=9.5)
        ax.set_ylabel("USD / MT")
        _clean(ax)
    axes[0].legend(loc="upper left", ncol=3, fontsize=7.6)
    axes[1].xaxis.set_major_locator(mdates.YearLocator(1))
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.suptitle("Forecast and outcome move together; the gap is the honest part",
                 x=0.01, ha="left", fontsize=11.5, fontweight="bold", color=PRIMARY)
    _source(fig, "Ensemble forecasts, wheat, evaluated folds with targets from 2019 onward. Shaded area is absolute error, not uncertainty.")
    fig.savefig(FIGS / "predicted_vs_actual.png")
    plt.close(fig)


def fig_error_horizon():
    hs = F.HORIZONS
    rw = [F.score(h, "Random Walk")["mae"] for h in hs]
    ens = [F.score(h, "Ensemble")["mae"] for h in hs]
    l3 = [F.score(h, "SARIMAX")["mae"] for h in hs]
    mase_ens = [F.score(h, "Ensemble")["mase_rw"] for h in hs]
    mase_l3 = [F.score(h, "SARIMAX")["mase_rw"] for h in hs]

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.5))
    x = np.arange(len(hs))
    w = 0.36
    ax = axes[0]
    ax.bar(x - w / 2, rw, w, color="#B9C6BC", label="Random walk")
    ax.bar(x + w / 2, ens, w, color=PRIMARY, label="Ensemble")
    for i, (a, b) in enumerate(zip(rw, ens)):
        ax.text(i - w / 2, a + 0.8, f"{a:,.0f}", ha="center", va="bottom", fontsize=7.6, color=GREY)
        ax.text(i + w / 2, b + 0.8, f"{b:,.0f}", ha="center", va="bottom", fontsize=7.6,
                color=PRIMARY, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([f"h = {h}" for h in hs])
    ax.set_ylabel("MAE (USD / metric ton)")
    ax.set_title("Error grows with the horizon — for every model", loc="left")
    ax.legend(loc="upper left")
    _clean(ax)

    ax = axes[1]
    ax.plot(x, mase_ens, marker="o", color=PRIMARY, lw=2, label="Ensemble")
    ax.plot(x, mase_l3, marker="s", color=BLUE, lw=1.5, label="SARIMAX")
    ax.axhline(1.0, color=RED, lw=1.2, ls="--")
    ax.text(len(hs) - 0.5, 1.006, "gate: 1.000", ha="right", va="bottom", fontsize=7.6, color=RED)
    for i, v in enumerate(mase_ens):
        ax.text(i, v - 0.018, f"{v:.3f}", ha="center", va="top", fontsize=7.4, color=PRIMARY)
    ax.set_xticks(x)
    ax.set_xticklabels([f"h = {h}" for h in hs])
    ax.set_ylabel("MASE vs random walk")
    ax.set_ylim(0.92, 1.08)
    ax.set_title("Skill relative to the benchmark, not to zero", loc="left")
    ax.legend(loc="upper right")
    _clean(ax)

    fig.suptitle("The same result looks strong or weak depending on the scale",
                 x=0.01, ha="left", fontsize=11.5, fontweight="bold", color=PRIMARY)
    _source(fig, "Left: absolute error in decision units. Right: error divided by the random-walk error on the same folds and horizon.")
    fig.savefig(FIGS / "error_by_horizon.png")
    plt.close(fig)


def fig_calibration():
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.5))
    ax = axes[0]
    colors = {1: PRIMARY, 3: SECONDARY, 6: "#6A9A78", 12: ACCENT}
    for h in F.HORIZONS:
        block = F.calibration(h, "Ensemble")
        ax.plot(block["nominal"], block["empirical"], marker="o", lw=1.8,
                color=colors[h], label=f"h = {h}")
    ax.plot([45, 100], [45, 100], color=GREY, lw=1, ls="--")
    ax.text(78, 73, "perfect calibration", fontsize=7.4, color=GREY, rotation=36)
    ax.set_xlabel("Nominal interval level (%)")
    ax.set_ylabel("Empirical coverage (%)")
    ax.set_title("Intervals mean what they say", loc="left")
    ax.set_xlim(45, 100)
    ax.set_ylim(45, 100)
    ax.legend(loc="lower right", ncol=2)
    _clean(ax)

    ax = axes[1]
    models = ["Random Walk", "SARIMAX", "Ensemble"]
    width = 0.26
    x = np.arange(len(F.HORIZONS))
    palette = ["#B9C6BC", BLUE, PRIMARY]
    for i, (model, color) in enumerate(zip(models, palette)):
        vals = [F.score(h, model)["coverage90"] for h in F.HORIZONS]
        ax.bar(x + (i - 1) * width, vals, width, color=color, label=model)
        for xi, v in zip(x + (i - 1) * width, vals):
            ax.text(xi, v + 0.6, f"{v:.0f}", ha="center", va="bottom", fontsize=7.2, color="#34443B")
    ax.axhline(90, color=RED, ls="--", lw=1.1)
    ax.text(len(F.HORIZONS) - 0.55, 90.8, "nominal 90%", ha="right", va="bottom", fontsize=7.4, color=RED)
    ax.set_xticks(x)
    ax.set_xticklabels([f"h = {h}" for h in F.HORIZONS])
    ax.set_ylim(80, 100)
    ax.set_ylabel("Empirical 90% coverage (%)")
    ax.set_title("Coverage is engineered, not discovered", loc="left")
    ax.legend(loc="lower left", ncol=3, fontsize=7.2)
    _clean(ax)

    fig.suptitle("Calibration: the test a point-forecast metric cannot perform",
                 x=0.01, ha="left", fontsize=11.5, fontweight="bold", color=PRIMARY)
    _source(fig, "Online conformal intervals built from prior-fold residuals; fold k uses folds < k only.")
    fig.savefig(FIGS / "calibration.png")
    plt.close(fig)


def fig_residuals():
    folds = pd.read_csv(DATA / "fold_predictions_wheat.csv", parse_dates=["target"])
    block = folds[(folds["horizon"] == 1) & (folds["model"] == "L5")].sort_values("target")
    resid = (block["actual"] - block["forecast"]).to_numpy(float)
    fitted = block["forecast"].to_numpy(float)

    fig, axes = plt.subplots(2, 2, figsize=(11.6, 6.8))
    ax = axes[0, 0]
    ax.plot(block["target"], resid, color=PRIMARY, lw=1.1)
    ax.axhline(0, color=GREY, lw=0.9)
    ax.set_title("Residuals over time", loc="left")
    ax.set_ylabel("Actual − forecast (USD/MT)")
    _clean(ax)

    ax = axes[0, 1]
    ax.hist(resid, bins=16, color=SECONDARY, alpha=0.75, edgecolor="white", density=True)
    xs = np.linspace(resid.min(), resid.max(), 200)
    ax.plot(xs, stats_norm_pdf(xs, resid.mean(), resid.std(ddof=1)), color=ACCENT, lw=1.5)
    ax.set_title("Distribution of residuals", loc="left")
    ax.set_xlabel("USD / metric ton")
    ax.set_ylabel("Density")
    _clean(ax)

    ax = axes[1, 0]
    lags = 24
    acf_vals = acf(resid, nlags=lags, fft=False)
    ax.bar(range(lags + 1), acf_vals, color=PRIMARY, width=0.7)
    ax.axhline(0, color=GREY, lw=0.9)
    bound = 1.96 / math.sqrt(len(resid))
    ax.axhline(bound, color=RED, lw=1, ls="--")
    ax.axhline(-bound, color=RED, lw=1, ls="--")
    ax.set_title("Autocorrelation of residuals", loc="left")
    ax.set_xlabel("Lag (months)")
    ax.set_ylabel("ACF")
    _clean(ax)

    ax = axes[1, 1]
    ordered = np.sort(resid)
    probs = (np.arange(1, len(ordered) + 1) - 0.5) / len(ordered)
    theoretical = stats_norm_ppf(probs, resid.mean(), resid.std(ddof=1))
    ax.scatter(theoretical, ordered, s=16, color=SECONDARY, alpha=0.8, edgecolor="none")
    lims = [min(theoretical.min(), ordered.min()), max(theoretical.max(), ordered.max())]
    ax.plot(lims, lims, color=ACCENT, lw=1.2, ls="--")
    ax.set_title("Q–Q plot against a normal", loc="left")
    ax.set_xlabel("Theoretical quantile")
    ax.set_ylabel("Observed quantile")
    _clean(ax)

    fig.suptitle("Residual diagnostics: what the score cannot show",
                 x=0.01, ha="left", fontsize=11.5, fontweight="bold", color=PRIMARY)
    _source(fig, "Ensemble, h = 1, 60 folds. Autocorrelation beyond the dashed band means the model has left structure on the table.")
    fig.savefig(FIGS / "residual_diagnostics.png")
    plt.close(fig)


def stats_norm_pdf(x, mean, sd):
    return (1 / (sd * math.sqrt(2 * math.pi))) * np.exp(-0.5 * ((x - mean) / sd) ** 2)


def stats_norm_ppf(p, mean, sd):
    from scipy.stats import norm
    return norm.ppf(p, loc=mean, scale=sd)


def fig_cross_commodity():
    rows = []
    for crop in F.CROPS:
        row = {"crop": crop}
        for h in F.HORIZONS:
            best = F.cross_score(crop, h)
            row[h] = best
        rows.append(row)

    fig, ax = plt.subplots(figsize=(10.6, 4.4))
    data = np.array([[row[h]["mase_rw"] for h in F.HORIZONS] for row in rows])
    norm = TwoSlopeNorm(vmin=0.90, vcenter=1.0, vmax=1.30)
    im = ax.imshow(data, cmap=plt.get_cmap("RdYlGn_r"), norm=norm, aspect="auto")
    ax.set_xticks(range(len(F.HORIZONS)))
    ax.set_xticklabels([f"h = {h}" for h in F.HORIZONS])
    ax.set_yticks(range(len(F.CROPS)))
    ax.set_yticklabels(F.CROPS)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i, row in enumerate(rows):
        for j, h in enumerate(F.HORIZONS):
            best = row[h]
            mark = "✓" if best["gate"] == "PASS" else "✗"
            value = best["mase_rw"]
            color = "white" if value > 1.14 or value < 0.93 else "#16241C"
            ax.text(j, i - 0.10, f"{F.SHORT[best['model']]}  {value:.3f}",
                    ha="center", va="center", fontsize=9, fontweight="bold", color=color)
            ax.text(j, i + 0.22, mark, ha="center", va="center", fontsize=8.5, color=color)
    ax.set_title("The same model is good on maize and useless on wheat", loc="left", pad=12)
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("MASE vs RW", fontsize=8)
    cbar.ax.tick_params(labelsize=7.5)
    cbar.outline.set_visible(False)
    fig.subplots_adjust(bottom=0.18)
    fig.text(0.01, 0.045, "Best candidate per cell; ✓ beats both benchmarks, ✗ does not.",
             fontsize=7.6, color="#4D5B53")
    _source(fig, "45 folds per commodity, step 4 months. Same hyperparameters, no per-crop tuning.")
    fig.savefig(FIGS / "cross_commodity.png")
    plt.close(fig)


def fig_decision():
    d = F.DECISION
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.5))
    ax = axes[0]
    ax.plot(d["tau"] * 100, d["mean_cost"], color=PRIMARY, lw=2, label="Threshold rule")
    ax.axhline(F.DECISION_SUMMARY["always_wait"], color=GREY, ls="--", lw=1.2, label="Always wait")
    ax.axhline(F.DECISION_SUMMARY["perfect"], color=ACCENT, ls=":", lw=1.4, label="Perfect foresight")
    best_tau = F.DECISION_SUMMARY["best_tau"] * 100
    best_cost = F.DECISION_SUMMARY["best_cost"]
    ax.scatter([best_tau], [best_cost], s=45, color=ACCENT, zorder=5)
    ax.annotate(f"best τ = {best_tau:+.1f}%", xy=(best_tau, best_cost), xytext=(10, 12),
                textcoords="offset points", fontsize=8, color=ACCENT, fontweight="bold")
    ax.set_xlabel("Buy-now threshold, τ (% forecast rise)")
    ax.set_ylabel("Average procurement cost (USD/MT)")
    ax.set_title("A forecast becomes useful only at a threshold", loc="left")
    ax.legend(loc="upper right", fontsize=7.4)
    _clean(ax)

    ax = axes[1]
    ax.plot(d["tau"] * 100, d["hit_rate"], color=PRIMARY, lw=1.8, label="Hit rate when buying")
    ax.plot(d["tau"] * 100, d["rises_captured"], color=BLUE, lw=1.5, ls="--", label="Share of rises captured")
    ax.axhline(50, color=RED, lw=1, ls=":")
    ax.text(-2.8, 51, "coin flip", fontsize=7.4, color=RED)
    ax.set_xlabel("Buy-now threshold, τ (% forecast rise)")
    ax.set_ylabel("Percent")
    ax.set_ylim(0, 105)
    ax.set_title("Direction is the weak link", loc="left")
    ax.legend(loc="lower left", fontsize=7.4)
    _clean(ax)

    fig.suptitle("Decision-relevant evaluation: cost, not accuracy",
                 x=0.01, ha="left", fontsize=11.5, fontweight="bold", color=PRIMARY)
    _source(fig, "One-month procurement rule. Cost is the realised purchase price; perfect foresight buys at the lower of origin and target price.")
    fig.savefig(FIGS / "decision_curve.png")
    plt.close(fig)


def fig_dashboard():
    fig = plt.figure(figsize=(13.4, 7.6))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.15, 1], hspace=0.42, wspace=0.28,
                          left=0.055, right=0.985, top=0.855, bottom=0.07)

    fig.text(0.055, 0.955, "WHEAT PRICE OUTLOOK  ·  EVALUATION DASHBOARD", fontsize=8,
             color=ACCENT, fontweight="bold")
    fig.text(0.055, 0.915, "The forecast is not reliably better than a random walk — use it as a range, not a trigger",
             fontsize=13.2, color=PRIMARY, fontweight="bold")
    fig.text(0.985, 0.925, "Origin: Oct 2026", fontsize=8, color=GREY, ha="right")

    # fan
    ax = fig.add_subplot(gs[0, :2])
    prices = pd.read_csv(HERE.parent.parent / "week4" / "data" / "world_bank_agricultural_benchmarks_2000_2026.csv",
                         parse_dates=["Date"])
    prices = prices[prices["Date"] >= "2022-01-01"]
    grid, point, bands = _fan_paths()
    origin = pd.Timestamp(F.LATEST["origin"].iloc[0])
    future = pd.date_range(origin + pd.offsets.MonthBegin(1), periods=12, freq="MS")
    hist = prices[prices["Date"] <= origin]
    ax.plot(hist["Date"], hist["Wheat_HRW_USD_MT"], color=PRIMARY, lw=1.7)
    ax.plot(future, point, color=ACCENT, lw=1.8)
    for level, alpha in ((90, 0.15), (80, 0.20), (50, 0.28)):
        lo, hi = bands[level]
        ax.fill_between(future, lo, hi, color=ACCENT, alpha=alpha, linewidth=0)
    ax.axvline(origin, color=GREY, ls=(0, (3, 3)), lw=0.9)
    ax.set_title("Forecast to October 2027", loc="left", fontsize=9.5)
    ax.set_ylabel("USD / MT")
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    _clean(ax)

    # traffic lights
    ax = fig.add_subplot(gs[0, 2])
    ax.axis("off")
    ax.set_title("Horizon verdicts", loc="left", fontsize=9.5)
    verdicts = []
    for h in F.HORIZONS:
        hd = F.head(h)
        verdicts.append((h, hd["gate"], hd["mase_rw"], hd["mae"]))
    y = 0.82
    for h, gate, mase, mae in verdicts:
        passed = gate == "PASS"
        ax.add_patch(FancyBboxPatch((0.02, y - 0.08), 0.96, 0.15, boxstyle="round,pad=0.01,rounding_size=0.02",
                                    linewidth=0, facecolor="#EDF3EE" if passed else "#FBEAE7",
                                    transform=ax.transAxes))
        ax.text(0.07, y, ("✓" if passed else "✗"), fontsize=13,
                color=SECONDARY if passed else RED, transform=ax.transAxes, va="center")
        ax.text(0.19, y + 0.015, f"h = {h}m", fontsize=8.6, fontweight="bold",
                color=PRIMARY, transform=ax.transAxes, va="center")
        ax.text(0.45, y + 0.015, f"MASE/RW {mase:.3f}", fontsize=7.6,
                color="#34443B", transform=ax.transAxes, va="center")
        ax.text(0.45, y - 0.035, f"MAE {mae:,.1f}", fontsize=7.2,
                color=GREY, transform=ax.transAxes, va="center")
        y -= 0.235

    # calibration mini
    ax = fig.add_subplot(gs[1, 0])
    for h, color in zip(F.HORIZONS, [PRIMARY, SECONDARY, "#6A9A78", ACCENT]):
        block = F.calibration(h, "Ensemble")
        ax.plot(block["nominal"], block["empirical"], marker="o", ms=3, lw=1.4, color=color)
    ax.plot([45, 100], [45, 100], color=GREY, ls="--", lw=0.9)
    ax.set_title("Calibration", loc="left", fontsize=9)
    ax.set_xlabel("Nominal %", fontsize=8)
    ax.set_ylabel("Observed %", fontsize=8)
    _clean(ax)

    # error horizon mini
    ax = fig.add_subplot(gs[1, 1])
    ens = [F.score(h, "Ensemble")["mase_rw"] for h in F.HORIZONS]
    ax.bar([f"h{h}" for h in F.HORIZONS], ens, color=[SECONDARY if v < 1 else RED for v in ens], width=0.6)
    ax.axhline(1.0, color=RED, ls="--", lw=1)
    ax.set_ylim(0.9, 1.08)
    ax.set_title("Skill vs random walk", loc="left", fontsize=9)
    ax.set_ylabel("MASE", fontsize=8)
    _clean(ax)

    # decision box
    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    ax.set_title("Recommended use", loc="left", fontsize=9)
    ax.add_patch(FancyBboxPatch((0.02, 0.08), 0.96, 0.82, boxstyle="round,pad=0.01,rounding_size=0.02",
                                linewidth=0.8, edgecolor=ACCENT, facecolor="#FBF4EC",
                                transform=ax.transAxes))
    ax.text(0.08, 0.72, "USE FOR", fontsize=7, color=ACCENT, fontweight="bold", transform=ax.transAxes)
    ax.text(0.08, 0.50, "Budget ranges, contract\nwindows, scenario planning", fontsize=8.2,
            color="#34443B", transform=ax.transAxes, va="center", linespacing=1.4)
    ax.text(0.08, 0.30, "DO NOT USE FOR", fontsize=7, color=RED, fontweight="bold", transform=ax.transAxes)
    ax.text(0.08, 0.13, "Directional trading, daily timing", fontsize=8.2,
            color="#34443B", transform=ax.transAxes, va="center")

    _source(fig, "Illustrative one-screen layout. Every panel traces to the same evaluated fold set; no number is typed by hand.")
    fig.savefig(FIGS / "dashboard_mock.png")
    plt.close(fig)


def main():
    fig_architecture()
    fig_heatmap()
    fig_fan()
    fig_predicted_actual()
    fig_error_horizon()
    fig_calibration()
    fig_residuals()
    fig_cross_commodity()
    fig_decision()
    fig_dashboard()
    print("figures written to", FIGS)


if __name__ == "__main__":
    main()
