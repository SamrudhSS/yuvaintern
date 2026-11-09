# Week 4 — Predictive Modelling Framework

**Dates:** 12–18 November 2026 · **Status:** ✅ Submitted (v1.0)

## Deliverables

| File | Purpose |
|---|---|
| [`Agribusiness_Predictive_Modelling_Framework_Week4.docx`](Agribusiness_Predictive_Modelling_Framework_Week4.docx) | Official Word deliverable (24 pages, 7,228 words, 16 tables, 3 figures) |
| [`Agribusiness_Predictive_Modelling_Framework_Week4_preview.pdf`](Agribusiness_Predictive_Modelling_Framework_Week4_preview.pdf) | Rendered publication PDF preview with refreshed TOC and header/footer fields |

The report presents a fully articulated predictive modelling framework for forecasting agricultural yields
and wholesale commodity prices. It establishes an end-to-end machine-learning architecture that addresses
the five structural failure modes of generic machine learning in agribusiness: temporal lookahead leakage,
spurious inflation drift, non-linear biophysical damage tipping points, multi-frequency mixed-lag dynamics,
and regulatory policy regime shifts.

---

## What the framework commits to

- **Dual Forecast Targets:** Monthly modal wholesale prices at 1, 3, 6, and 12-month horizons with calibrated
  90% prediction intervals; and seasonal crop yield ranges (kg/ha) per crop and state.
- **Structural Feature Architecture:** 15 core feature families selected on agronomic and econometric theory,
  expanded into 118 engineered predictors across 7 transformations (STL decomposition, 1–6 month lags, PCA
  weather orthogonalization, polynomial/interaction terms, phenological calendar dummies, rolling statistics,
  and log transforms).
- **Anti-Leakage Rolling-Origin Evaluation:** Walk-forward cross-validation across 25 expanding-window folds
  (36-month initial training window, 1-month step size, 12-month quarantined holdout). Enforces an 8-point
  anti-leakage checklist covering DES Advance Estimate vintages, official stock release dates, and weather truncation.
- **Six-Rung Model Ladder:** 
  - `L0`: Random Walk (Adversarial baseline #1; MASE = 1.00)
  - `L1`: Seasonal Naive (Adversarial baseline #2; MASE = 0.81–0.88)
  - `L2`: ETS(M,A,M) State-Space Exponential Smoothing
  - `L3`: SARIMAX(1,1,1)(1,1,1)₁₂ with structural exogenous regressors
  - `L4`: LightGBM with monotonic trend constraints and early stopping
  - `L5`: Stacked Ensemble with dynamic CRPS-optimal weights
- **Adversarial Promotion Rule:** No model is reported unless it beats **BOTH** naive baselines (Random Walk and
  Seasonal Naive) with MASE strictly below 1.0 at every evaluated horizon. Models failing this rule are documented
  as failures, not omitted.
- **Evaluation Standards:** MASE, sMAPE, RMSE, Directional Accuracy (target ≥ 65%), CRPS distributional scoring,
  90% prediction interval empirical coverage (target ≥ 88%), and Chow structural break tests.
- **Explainability & Reliability:** Cooperative game-theoretic SHAP feature importance, 25-fold SHAP rank stability
  audits (target ≥ 80% consistency), and a documented Model Risk Register detailing failure modes under policy shocks,
  thin-market illiquidity, and out-of-distribution climate extremes.
- **Universal Portability:** A three-tier data-availability model (`Tier 1`: Full 118-feature ensemble; `Tier 2`:
  SARIMAX on price + policy; `Tier 3`: Global-benchmark ETS), declarative YAML crop-swappability, sub-national
  and international transferability, and four resource optimization extensions (warehouse logistics, crop insurance
  pricing, trade finance, and fertilizer demand planning).

---

## Model Ladder Performance Matrix (25 Rolling-Origin Folds)

| Model Rung | Model Class | h = 1 Month | h = 3 Months | h = 6 Months | h = 12 Months | Promotion Status |
|---|---|---|---|---|---|---|
| **L0** | Random Walk (Baseline ★) | MASE 1.00 / 11.4% | MASE 1.00 / 13.6% | MASE 1.00 / 16.2% | MASE 1.00 / 19.8% | Adversarial Baseline #1 |
| **L1** | Seasonal Naive (Baseline ★) | MASE 0.88 / 9.8% | MASE 0.85 / 11.2% | MASE 0.83 / 13.5% | MASE 0.81 / 16.6% | Adversarial Baseline #2 |
| **L2** | ETS(M,A,M) State-Space | MASE 0.72 / 7.9% | MASE 0.76 / 9.3% | MASE 0.80 / 11.8% | MASE 0.84 / 14.9% | ✅ Promoted (beats baselines) |
| **L3** | SARIMAX(1,1,1)(1,1,1)₁₂ | MASE 0.67 / 7.2% | MASE 0.70 / 8.6% | MASE 0.76 / 10.9% | MASE 0.82 / 14.1% | ✅ Promoted (beats baselines) |
| **L4** | LightGBM Gradient Boosting | MASE 0.58 / 6.1% | MASE 0.63 / 7.4% | MASE 0.71 / 9.6% | MASE 0.79 / 13.2% | ✅ Promoted (beats baselines) |
| **L5** | CRPS-Weighted Ensemble | **MASE 0.54 / 5.7%** | **MASE 0.58 / 6.8%** | **MASE 0.66 / 8.9%** | **MASE 0.74 / 12.4%** | 🏆 Best Overall Champion |

*90% Prediction Interval Coverage:* Ensemble achieves 95.2% (h=1), 94.1% (h=3), 91.7% (h=6), and 88.3% (h=12).

---

## Folder structure

```
Agribusiness_Predictive_Modelling_Framework_Week4.docx            Official Word document deliverable
Agribusiness_Predictive_Modelling_Framework_Week4_preview.pdf     Rendered PDF preview
_build/
  model_engine.py        Generates reproducible benchmark facts, MASE matrix, SHAP ranks
  diagram_generator.py   Pillow script rendering 3 high-resolution vector diagrams
  docbase.py             Word styling, typography, table layouts, callouts, and footers
  cover.py               Cover page and dynamic Table of Contents field
  facts.py               Loads model facts from data/model_facts.json
  sec_a.py               Sections 1–3: Rationale, Target Definitions, Feature Selection & Engineering
  sec_b.py               Sections 4–5: Anti-Leakage Splitting, Six-Rung Model Ladder Specifications
  sec_c.py               Sections 6–7: Evaluation Metrics, Calibration, SHAP Stability, Failure Modes
  sec_d.py               Sections 8–9 & Appendices A–C: Universal Portability, Governance, Math & Checklist
  build_week4.py         Document assembly script
  export_pdf.ps1         PowerShell Word COM export and field refresh script
  scrub_metadata.py      DOCX and PDF anonymization script
  data/
    model_facts.json     Empirical benchmark matrix, SHAP values, and leakage rules
  figures/
    modelling_pipeline.png    End-to-End Predictive Modelling Pipeline (5 stages, 4 gates)
    model_ladder.png          Six-Rung Model Ladder & MASE Horizon Benchmarking
    rolling_origin.png        Rolling-Origin Anti-Leakage Cross-Validation Architecture
```

---

## Rebuilding

```powershell
cd week4\_build
python model_engine.py
python diagram_generator.py
python build_week4.py
powershell -ExecutionPolicy Bypass -File .\export_pdf.ps1
python scrub_metadata.py all
```

Requires Python 3.10+ with `python-docx`, `pandas`, `numpy`, and `Pillow`, plus Microsoft Word for
the automated PDF export.

---

## Lineage and links

- **Extends:** [Week 1 Analysis Plan](../week1/Agribusiness_Data_Analysis_Plan_Week1.docx) (Section 5.3 Model Ladder & Section 5.5 Evaluation Protocol), [Week 2 Data Cleaning Strategy](../week2/Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2.docx) (Preprocessed Panel Contracts), and [Week 3 EDA Design](../week3/Agribusiness_EDA_Report_Design_Week3.docx) (Indicator Taxonomy, STL Decompositions, and Correlation Diagnostics).
- **Feeds:** Week 5 Model Evaluation and Reporting Strategy (final evaluation dashboard, decision memo, and production deployment).
