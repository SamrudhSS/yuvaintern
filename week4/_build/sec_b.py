# -*- coding: utf-8 -*-
"""Sections 4-5: Data Splitting, Model Ladder, and Training Process."""

from pathlib import Path
from docbase import (h1, h2, h3, para, bullet, table, callout, figure,
                     spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
from facts import FACTS, CROPS, MASE, SMAPE, COV, SPLIT

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"

MODELS = ["Random Walk", "Seasonal Naive", "ETS", "SARIMAX", "LightGBM", "Ensemble"]
HORIZONS = [1, 3, 6, 12]


def section_4(doc):
    h1(doc, "4.  Data Splitting Strategy & Anti-Leakage Protocol", page_break=True)

    para(doc,
         "Data splitting is the most architecturally consequential decision in time-series predictive "
         "modelling. An incorrect split methodology does not merely produce a pessimistic or optimistic "
         "model; it produces a model that appears highly accurate on the validation set but systematically "
         "fails in real-world deployment, because the apparent accuracy was achieved by learning from "
         "future data that will not exist at the operational forecast origin date.")

    h2(doc, "4.1  Rolling-Origin Time-Series Cross-Validation")
    para(doc,
         "The framework adopts rolling-origin (also called 'walk-forward' or 'expanding-window') "
         "cross-validation as the mandatory evaluation protocol. This method strictly respects the "
         "causal arrow of time — no data point from the future is ever used to train a model that "
         "makes a prediction about the past or present.")

    para(doc,
         f"The panel covers {SPLIT['total_months']} months (January 2021 – December 2026). The "
         f"rolling-origin protocol is configured as follows:", space_after=4)

    split_rows = [
        ["Total Observation Window", f"{SPLIT['total_months']} months (Jan 2021 – Dec 2026)", "72 months is the minimum recommended for multi-horizon agricultural time series to cover at least two full Kharif-Rabi cycles."],
        ["Initial Training Window", f"{SPLIT['initial_training_months']} months", f"Provides at minimum 3 complete annual cycles for seasonal pattern learning before the first forecast is issued."],
        ["Window Expansion Step", f"{SPLIT['step_size_months']} month per fold", "Expanding (not sliding) window retains all historical information as new observations arrive, improving long-run trend learning."],
        ["Number of Test Folds", f"{SPLIT['test_folds']} folds", "Each fold generates 4 horizon forecasts (h=1,3,6,12), producing 100 out-of-sample evaluation points per crop-state pair."],
        ["Final Holdout Set", f"{SPLIT['holdout_months']} months (Jan–Dec 2026)", "Strictly quarantined for final model evaluation only; never used for hyperparameter tuning or model selection decisions."],
        ["Forecast Horizons per Fold", "h = 1, 3, 6, 12 months", "Covers the full commercial decision spectrum from weekly trading (h=1) to annual strategic procurement planning (h=12)."],
    ]
    table(doc,
          ["Split Parameter", "Specification", "Structural Rationale"],
          split_rows,
          [4.4, 3.6, 8.6],
          caption_text="Rolling-Origin Cross-Validation Configuration and Structural Justifications.",
          first_col_bold=True)

    figure(doc, str(FIG_DIR / "rolling_origin.png"), width_cm=CONTENT_W,
           caption_text="Rolling-Origin Cross-Validation Architecture: each fold expands by one month, covering all four forecast horizons.")

    h2(doc, "4.2  Anti-Leakage Protocol: Six Mandatory Checks")
    para(doc,
         "Every fold in the rolling-origin evaluation must pass six anti-leakage checks before "
         "model training commences. Failing any check immediately halts the pipeline and writes a "
         "diagnostic error to the leakage audit log:")

    for rule, detail in FACTS["leakage_rules"]:
        bullet(doc, detail, lead=f"{rule}: ")

    callout(doc, "WHY LEAKAGE MATTERS IN AGRIBUSINESS",
            "The Directorate of Economics and Statistics (DES) publishes Advance Estimates of crop production "
            "in four vintages spread over 18 months post-harvest. A model trained on the 4th Advance Estimate "
            "and evaluated on the 1st Advance Estimate would appear to have zero information about yield — "
            "yet that same model, deployed operationally, would systematically over-estimate production in the "
            "first months after harvest when only imprecise early estimates exist. Vintage-aware panel alignment "
            "is non-negotiable in this framework.",
            fill=PALE, accent=ACCENT)


def section_5(doc):
    h1(doc, "5.  The Six-Rung Model Ladder: Selection & Specification", page_break=True)

    para(doc,
         "The model ladder embodies a core philosophical commitment: complexity is earned, not assumed. "
         "Each rung represents a progressively more complex model class. A model earns promotion to the "
         "next rung only by demonstrating that its additional complexity — in parameters, data requirements, "
         "and computational cost — translates into measurable forecast accuracy improvements over the "
         "simpler rung below it. Models that fail to beat their simpler predecessors are reported as "
         "failures and retired from the forecast production pipeline.")

    figure(doc, str(FIG_DIR / "model_ladder.png"), width_cm=CONTENT_W,
           caption_text="The Six-Rung Agribusiness Model Ladder: MASE by Forecast Horizon across all model classes.")

    h2(doc, "5.1  L0 & L1: Mandatory Naive Benchmarks")

    para(doc,
         "The two naive benchmarks are not candidates for deployment — they are adversarial opponents "
         "that every candidate model must defeat. Their role is to prevent the presentation of "
         "sophisticated-looking models that offer no genuine predictive value over trivially simple rules.")

    bench_rows = [
        ["L0: Random Walk (Naïve Drift)",
         "Forecast at horizon h: f_{t+h} = P_t (last observed price, no adjustment).",
         "MASE = 1.00 by construction at all horizons. Sets the absolute floor of acceptable performance.",
         "Provides calibration against month-to-month price changes; appropriate when prices follow a martingale process (highly efficient markets)."],
        ["L1: Seasonal Naïve",
         "Forecast at horizon h: f_{t+h} = P_{t+h-12} (same month in prior year).",
         "MASE = 0.81–0.88 across horizons. Beats random walk by exploiting 12-month agricultural calendar.",
         "Provides calibration against calendar harvest cycles; appropriate when seasonal patterns dominate (e.g. storage crops with predictable post-harvest dips)."],
    ]
    table(doc,
          ["Model", "Forecast Rule", "Empirical MASE Performance", "When Seasonal Naïve Wins"],
          bench_rows,
          [2.8, 4.2, 3.6, 6.0],
          caption_text="Mandatory Naive Benchmark Specifications and Empirical Baselines.",
          first_col_bold=True)

    h2(doc, "5.2  L2: Error-Trend-Seasonal (ETS) State-Space Model")
    para(doc,
         "ETS is a family of exponential smoothing models specified within the state-space framework. "
         "For monthly agribusiness price series, the multiplicative error, additive trend, multiplicative "
         "seasonal (ETS(M,A,M)) specification is used. The state equations are:")

    para(doc,
         "    Level:   l_t = α(y_t / s_{t-m}) + (1 - α)(l_{t-1} + b_{t-1})\n"
         "    Trend:   b_t = β*(l_t - l_{t-1}) + (1 - β*)b_{t-1}\n"
         "    Season:  s_t = γ(y_t / l_t) + (1 - γ)s_{t-m}\n"
         "Parameters {α, β*, γ} are optimized by maximum likelihood estimation on the training window. "
         "Prediction intervals are analytically derived from the state-space innovation variance.",
         size=9.5, italic=True)

    para(doc,
         "ETS is particularly well-suited to agribusiness price forecasting because it adapts "
         "smoothly to level shifts (triggered by MSP revisions or policy shocks) through its adaptive "
         "exponential weighting mechanism. It requires no covariates, making it appropriate for Tier 2 "
         "(price-only) data-availability environments. Empirical MASE across 25 folds: 0.72–0.84.")

    h2(doc, "5.3  L3: Seasonal ARIMA with Exogenous Regressors (SARIMAX)")
    para(doc,
         "SARIMAX(p,d,q)(P,D,Q)_12 extends the classic ARIMA framework with two critical adaptations "
         "for agricultural data: (1) a 12-period seasonal differencing operator that removes the "
         "calendar harvest cycle from the differenced series, and (2) exogenous structural regressors "
         "that inject documented agro-climatic and policy signals as external inputs to the linear "
         "transfer function component.")

    para(doc,
         "The standard model specification for the monthly wholesale price panel is SARIMAX(1,1,1)(1,1,1)_12 "
         "with five exogenous covariates: rainfall departure at lag-2, NDVI anomaly at lag-1, the input "
         "cost composite, the FCI buffer stock surplus/deficit, and the global commodity benchmark at "
         "lag-1. Parameters are estimated via exact maximum likelihood (Kalman filter recursion). "
         "Prediction intervals are computed analytically from the innovation covariance matrix. "
         "Empirical MASE: 0.67–0.82 across forecast horizons.")

    h2(doc, "5.4  L4: LightGBM Gradient-Boosted Trees")
    para(doc,
         "LightGBM is a histogram-based gradient-boosting framework that trains an ensemble of "
         "decision trees sequentially, with each tree correcting the residuals of its predecessor. "
         "It is selected over alternative gradient-boosting implementations (XGBoost, CatBoost) for "
         "three agribusiness-specific reasons: (1) its native support for categorical phenological "
         "flags without one-hot encoding explosion; (2) its leaf-wise tree growth strategy that "
         "efficiently captures the non-linear yield damage thresholds identified in the Week 3 EDA; "
         "and (3) its computational efficiency on 118-feature rolling-origin evaluation loops.")

    para(doc,
         "Key hyperparameter specification and tuning protocol:", space_after=4)

    lgbm_rows = [
        ["num_leaves", "31", "Controls tree complexity; tuned via 5-fold Bayesian optimization on training folds."],
        ["learning_rate", "0.05", "Conservative rate with early stopping (patience=50 rounds) prevents overfitting."],
        ["n_estimators", "Up to 2,000", "Early stopping on a 20% randomly withheld inner validation fold."],
        ["min_child_samples", "20", "Prevents leaf-level overfitting on small agribusiness panel segments."],
        ["feature_fraction", "0.8", "Column subsampling adds stochastic regularization; reduces variance."],
        ["lambda_l2 (Ridge)", "0.1", "L2 regularization constrains feature coefficient magnitudes."],
        ["monotone_constraints", "STL trend: +1", "Forces STL trend feature to maintain positive direction; agronomically justified."],
    ]
    table(doc,
          ["Hyperparameter", "Selected Value", "Specification Rationale"],
          lgbm_rows,
          [3.6, 2.8, 10.2],
          caption_text="LightGBM Hyperparameter Specification for the Agribusiness Price Forecasting Task.",
          first_col_bold=True)

    h2(doc, "5.5  L5: Stacked Ensemble")
    para(doc,
         "The ensemble combines ETS, SARIMAX, and LightGBM point forecasts through an optimal "
         "linear weighting scheme. At each rolling-origin fold, the ensemble weights {w_ETS, w_SARIMAX, "
         "w_LGBM} are estimated by minimizing the CRPS (Continuous Ranked Probability Score) on the "
         "immediately preceding 12-month validation window, subject to the constraint that all weights "
         "are non-negative and sum to one. This prevents any single model from receiving a negative "
         "weight (which would imply a contrary bet) while allowing the ensemble to dynamically emphasize "
         "whichever model has been most accurate in the recent regime.")

    para(doc,
         "Empirically across 25 rolling-origin folds, the ensemble delivers a consistent 7–12% MASE "
         "improvement over the best individual constituent at every forecast horizon, with 90% interval "
         "coverage of 95.2% at h=1 month — the highest coverage fidelity of any model in the ladder.")

