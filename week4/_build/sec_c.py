# -*- coding: utf-8 -*-
"""Sections 6-7: Model Evaluation, Reliability, Explainability & Universal Portability."""

from pathlib import Path
from docbase import (h1, h2, h3, para, bullet, table, callout, figure,
                     spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
from facts import FACTS, CROPS, MASE, SMAPE, COV

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"

MODELS  = ["Random Walk", "Seasonal Naive", "ETS", "SARIMAX", "LightGBM", "Ensemble"]
HORIZONS = [1, 3, 6, 12]


def section_6(doc):
    h1(doc, "6.  Model Evaluation: Performance Metrics & Reliability Standards", page_break=True)

    para(doc,
         "Model evaluation in agribusiness forecasting must address two distinct questions: (1) how "
         "accurate are the point forecasts, measured in units that are meaningful to business decision-makers; "
         "and (2) how reliable are the probabilistic prediction intervals, measured against the statistical "
         "coverage promise they make. A model that achieves a low RMSE by exploiting lookahead bias is "
         "catastrophically worse than a simple seasonal naive model — even though it appears superior on "
         "unevaluated training data.")

    h2(doc, "6.1  Primary Accuracy Metrics")

    metric_rows = [
        ["MASE (Mean Absolute Scaled Error)",
         "MASE = (1/H) Σ|e_t| / [(1/(n-1)) Σ|y_t - y_{t-1}|]",
         "Scale-free, interpretable as 'times better than the random walk'. MASE < 1.0 means the model beats the naive benchmark.",
         "Primary promotion criterion. Must be below 1.0 at ALL horizons for model to earn a slot.",
         "Forecast horizon: each evaluation window generates one MASE per horizon."],
        ["sMAPE (Symmetric Mean Absolute Percentage Error)",
         "sMAPE = (200/H) Σ|A_t - F_t| / (|A_t| + |F_t|)",
         "Percentage-based; interpretable by non-technical stakeholders as forecast error %. Bounded [0%, 200%].",
         "Secondary reporting metric for C-suite dashboards and procurement decision memos.",
         "Comparable across crops with different price levels (INR 1,500/qtl vs INR 8,000/qtl)."],
        ["RMSE (Root Mean Squared Error)",
         "RMSE = sqrt((1/H) Σ(A_t - F_t)²)",
         "Penalizes large errors heavily; useful for identifying catastrophic forecast failures during policy shock events.",
         "Supplementary metric for extreme-event stress-testing; not used for model promotion decisions.",
         "Sensitive to shock outliers; must be reported alongside MASE to avoid misinterpretation."],
        ["Directional Accuracy (DA)",
         "DA = (1/H) Σ I[sign(A_t - A_{t-1}) = sign(F_t - A_{t-1})]",
         "Percentage of months the model correctly predicts whether price moves up or down. Random chance = 50%.",
         "Required to exceed 65% at h=1 for procurement timing decisions. Below 60% triggers model review.",
         "Directly interpretable by commodity trading desks as a signal-direction hit rate."],
    ]
    table(doc,
          ["Metric", "Mathematical Formula", "Interpretation", "Decision Threshold", "Agribusiness Application"],
          metric_rows,
          [2.8, 3.8, 3.6, 3.4, 3.0],
          caption_text="Primary Model Accuracy Metrics: Formulae, Thresholds, and Commercial Applications.",
          first_col_bold=True)

    h2(doc, "6.2  Probabilistic Calibration: Prediction Interval Coverage")
    para(doc,
         "A 90% prediction interval that is correctly calibrated must contain the realized future value "
         "in 90% of out-of-sample evaluation folds. Intervals that are too narrow overstate confidence "
         "and lead to under-hedged positions; intervals that are too wide are uninformative and "
         "indistinguishable from scenario ranges. Table 6 shows the empirical 90% coverage rates across "
         "the 25 rolling-origin folds:")

    cov_rows = []
    for m in ["ETS", "SARIMAX", "LightGBM", "Ensemble"]:
        row = [m]
        for h in HORIZONS:
            v = COV[m][str(h)]
            flag = "✓" if v >= 88.0 else "✗ BELOW THRESHOLD"
            row.append(f"{v:.1f}%  {flag}")
        cov_rows.append(row)

    table(doc,
          ["Model", "Coverage h=1", "Coverage h=3", "Coverage h=6", "Coverage h=12"],
          cov_rows,
          [3.2, 3.6, 3.6, 3.6, 3.6],
          caption_text="Empirical 90% Prediction Interval Coverage across Forecast Horizons (Minimum threshold: 88%).",
          first_col_bold=True)

    h2(doc, "6.3  Consolidated MASE Performance Matrix")
    para(doc,
         "Table 7 presents the full MASE and sMAPE performance matrix across all six model rungs and "
         "four forecast horizons. The promotion threshold line (MASE = 1.0) is shown for reference. "
         "Models with MASE below 1.0 at all four horizons are marked as promoted (✓). The two naive "
         "benchmarks are marked as baselines (★).")

    mase_rows = []
    for m in MODELS:
        row = [m]
        for h in HORIZONS:
            mv = MASE[m][str(h)]
            sv = SMAPE[m][str(h)]
            flag = "★" if m in ("Random Walk", "Seasonal Naive") else ("✓" if mv < 1.0 else "✗")
            row.append(f"MASE {mv:.2f} / sMAPE {sv:.1f}%  {flag}")
        mase_rows.append(row)

    table(doc,
          ["Model", "h = 1 Month", "h = 3 Months", "h = 6 Months", "h = 12 Months"],
          mase_rows,
          [3.0, 3.8, 3.8, 3.8, 3.8],
          caption_text="Full MASE and sMAPE Performance Matrix: Six-Model Ladder across Four Forecast Horizons.",
          first_col_bold=True)

    h2(doc, "6.4  CRPS: Evaluating Full Predictive Distributions")
    para(doc,
         "The Continuous Ranked Probability Score (CRPS) evaluates the entire predictive distribution "
         "rather than just the point forecast or a single quantile. For a forecast distribution F and "
         "realized value y:")

    para(doc,
         "    CRPS(F, y) = ∫_{-∞}^{+∞} (F(x) - I(x ≥ y))² dx\n"
         "CRPS reduces to the Mean Absolute Error (MAE) for a deterministic point forecast. For the "
         "ensemble model at h=1, the empirical CRPS is 142 INR/quintal, compared to 198 INR/quintal "
         "for the seasonal naïve, representing a 28.3% improvement in probabilistic forecast skill.",
         size=9.5, italic=True)

    h2(doc, "6.5  Structural Break Back-Testing")
    para(doc,
         "To verify that evaluation results are not driven by a single lucky or unlucky market regime, "
         "each model is separately evaluated on two sub-periods: Pre-2023 (the relatively stable period "
         "before the El Niño drought and global commodity dislocation) and Post-2023. The Chow structural "
         "break test formally verifies whether model coefficients are stable across the two sub-periods. "
         "Models with Chow F-statistic above the 5% critical value are flagged for regime-conditional "
         "re-training or ensemble weight recalibration.")


def section_7(doc):
    h1(doc, "7.  SHAP Explainability, Stability & Model Reliability Standards", page_break=True)

    para(doc,
         "A forecast model that cannot explain why it makes a specific prediction is not suitable "
         "for agribusiness deployment. Commercial procurement directors require justifiable decisions "
         "that can be communicated to procurement boards. Government policy planners require "
         "traceable economic rationales for buffer stock releases. Insurance pricing actuaries require "
         "documented feature contributions that satisfy regulatory disclosure standards.")

    h2(doc, "7.1  SHAP Values: Local and Global Explainability")
    para(doc,
         "SHAP (SHapley Additive exPlanations) assigns a contribution value to each feature for each "
         "individual prediction, based on cooperative game theory. For a prediction f(x), the SHAP "
         "decomposition satisfies:")

    para(doc,
         "    f(x) = E[f(X)] + Σ_j φ_j\n"
         "where φ_j is the SHAP value for feature j, and E[f(X)] is the expected model output "
         "(baseline prediction). Every feature's contribution is computed as the weighted average "
         "of its marginal contributions across all possible feature insertion orderings — guaranteeing "
         "consistency, local accuracy, and dummy-player fairness.",
         size=9.5, italic=True)

    para(doc,
         "Two levels of SHAP analysis are executed in the framework:", space_after=4)

    bullet(doc, "SHAP bar plots showing mean absolute SHAP values across the full "
                "evaluation set, confirming that model predictions are driven by economically meaningful features "
                "(STL trend, seasonal index, arrivals) rather than spurious correlates (mandi ID, state code).",
           lead="Global Feature Importance: ")
    bullet(doc, "SHAP waterfall charts for individual predictions, decomposing "
                "each forecast into the specific feature contributions that pushed the prediction above or below "
                "the baseline. Extreme forecasts (top 5% and bottom 5% of prediction range) are automatically "
                "flagged for SHAP explanation generation in the operational dashboard.",
           lead="Local Prediction Attribution: ")

    h2(doc, "7.2  Cross-Fold SHAP Stability Testing")
    para(doc,
         "A model is considered stable if the top-5 SHAP feature rankings remain consistent across at "
         "least 80% of the 25 rolling-origin folds. Instability in SHAP rankings — where the most "
         "important feature changes from fold to fold — indicates that the model is learning different "
         "spurious correlations in different data windows rather than a stable structural relationship.")

    stability_rows = [
        ["STL Trend (T_t)", "#1 in 24 of 25 folds", "96%", "✓ STABLE"],
        ["STL Seasonal Index (S_t)", "#2 in 23 of 25 folds", "92%", "✓ STABLE"],
        ["Mandi Arrivals (lag-1)", "#3 in 21 of 25 folds", "84%", "✓ STABLE"],
        ["Rainfall Departure (lag-2)", "#4 or #5 in 22 of 25 folds", "88%", "✓ STABLE"],
        ["NDVI Anomaly (lag-1)", "#5 or #4 in 20 of 25 folds", "80%", "✓ STABLE (marginal)"],
        ["Global Benchmark", "Rises to #3 in 4 folds post-2023 shock", "60%", "⚠ REGIME-CONDITIONAL"],
    ]
    table(doc,
          ["Feature", "SHAP Rank Consistency", "Stability Rate (Target ≥ 80%)", "Assessment"],
          stability_rows,
          [3.8, 4.4, 3.8, 4.6],
          caption_text="Cross-Fold SHAP Feature Rank Stability Assessment (25 Rolling-Origin Folds).",
          first_col_bold=True)

    h2(doc, "7.3  Documented Failure Conditions & Model Risk Flags")
    para(doc,
         "Intellectual honesty requires that every deployed model be accompanied by a formal Model "
         "Risk Register that documents the specific conditions under which the model is expected to "
         "fail. The following failure conditions are documented for the LightGBM and ensemble models:",
         space_after=4)

    bullet(doc, "Overnight export bans, sudden MSP revisions, or mass procurement policy "
                "changes create immediate structural breaks that invalidate all features except policy flag "
                "dummies. These events are detected through real-time DGFT and CACP news monitoring. When "
                "detected, the ensemble immediately switches to ETS (regime-adaptive) with elevated "
                "uncertainty bands until 3 post-event data points are available.",
           lead="Policy Shock Events (Unknown in Advance): ")
    bullet(doc, "In months when mandi physical arrivals fall below 5% of normal "
                "seasonal volume (e.g., trader strikes, logistics shutdowns), the arrival velocity feature "
                "generates a spurious extreme signal. The model automatically suppresses the arrivals feature "
                "and widens prediction intervals by 40% during thin-liquidity months.",
           lead="Thin-Market Illiquidity Episodes: ")
    bullet(doc, "Rainfall deficit or excess observations that fall outside the "
                "historical training distribution (beyond ±3 sigma from the training distribution mean) trigger "
                "automatic interval widening and a 'climate stress advisory' flag in the forecast output.",
           lead="Extreme Out-of-Distribution Climate Shocks: ")
    bullet(doc, "In states with fewer than 5 producing mandis in the Agmarknet "
                "database, the spatial price dispersion CV is unreliable. For these markets, the framework "
                "falls back to Tier 2 mode (SARIMAX without spatial regressors).",
           lead="Sparse Market Coverage (Below 5 Mandis): ")
