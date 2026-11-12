# Week 5 — Model Evaluation and Reporting Strategy

**Dates:** 19–26 November 2026 · **Status:** ✅ Complete (v1.0, ready to submit)

## Deliverables

| File | Purpose |
|---|---|
| [`Agribusiness_Model_Evaluation_Reporting_Strategy_Week5.docx`](Agribusiness_Model_Evaluation_Reporting_Strategy_Week5.docx) | Official Word deliverable (48 pages, 19,861 words, 40 numbered tables, 12 figures; 1.05 MB / 1,104,717 bytes) |
| [`Agribusiness_Model_Evaluation_Reporting_Strategy_Week5_preview.pdf`](Agribusiness_Model_Evaluation_Reporting_Strategy_Week5_preview.pdf) | Rendered PDF preview with refreshed contents, header and footer fields |
| [`Submission_Description_Week5.txt`](Submission_Description_Week5.txt) | Submission-ready description (300+ words) with the GitHub project URL |
| [`data/README.md`](data/README.md) | Executed evidence, source window, metric conventions and regeneration steps |

Week 5 is the evaluation and reporting layer for the forecasting work built in Weeks 1–4. It does
not add another model for its own sake. It asks a harder question: **what can this forecast
legitimately be used for, and what evidence would change that answer?**

The report defines a decision-grade metric suite, executes a rolling-origin audit on real World
Bank price data, quantifies uncertainty with paired bootstrap intervals and Diebold–Mariano tests,
stress-tests calibration across regimes and crops, specifies a visual system for non-specialists,
provides a four-box executive summary template, records what the evaluation cannot establish, and
sets a prioritised twelve-month refinement roadmap.

---

## What the strategy commits to

- **A metric hierarchy, not a metric pile.** Accuracy, calibration, direction, stability and
  decision value are separate claims with separate evidence. No single number promotes a model.
- **A benchmark-relative primary metric.** MASE against the random walk on the same folds and
  horizon is the gate. Absolute MASE is reported but cannot override the benchmark comparison.
- **A conservative promotion rule.** A candidate must pass an integrity check and four gates in
  order: accuracy, significance, calibration and decision value.
- **Uncertainty on every claim.** Paired bootstrap intervals, Diebold–Mariano tests, a minimum
  detectable effect and a Bonferroni-adjusted threshold for twenty candidate-horizon comparisons.
- **Online conformal intervals.** Fold *k* uses only residuals from folds before *k*. No future
  outcome enters the band, so coverage is a testable promise rather than a modelling assumption.
- **Segment-first reporting.** Results are shown by crop, horizon, regime and volatility bucket,
  not only as a pooled average that can hide offsetting failures.
- **A visual ladder for three audiences.** One fan chart and one verdict for the board; error by
  horizon and a threshold curve for operations; scorecard, calibration and residual diagnostics
  for the technical reviewer.
- **A limitation register with owners and triggers.** Every limitation has evidence, a severity,
  a mitigation and a condition that forces a review.

---

## Executed evidence on real data

The audit uses 322 monthly World Bank Pink Sheet observations (2000-01 to 2026-10), a 310-month
design matrix with 31 predictors, 60 expanding-window origins at a three-month step, four
horizons, and six models. It produces **1,440 fold-level forecasts with zero model failures** and
reproduces the Week 4 ensemble MAE exactly.

| Horizon | Best candidate | MAE (USD/MT) | MASE vs RW | 90% coverage | Directional accuracy | Verdict |
|---:|---|---:|---:|---:|---:|---|
| 1 month | **Ensemble** | 12.09 | **0.979** | 90.4% | 50.0% | Passes accuracy; parity with random walk |
| 3 months | SARIMAX | 21.94 | 1.031 | 82.7% | 46.7% | **Fails the accuracy gate** |
| 6 months | SARIMAX | 33.79 | **0.991** | 84.6% | 55.0% | Passes accuracy; parity with random walk |
| 12 months | **Ensemble** | 50.57 | **0.945** | 78.8% | 55.0% | Passes accuracy; interval under-covers |

### What the numbers actually say

- **No improvement is statistically separable from zero.** At h=1 the ensemble is 2.1% closer
  than the random walk, but the paired 95% interval on the MAE difference is **−1.30 to +0.75
  USD/MT** (p = 0.615). The minimum detectable effect is 11.8% of the random-walk MAE, so the
  design cannot resolve a 2% edge.
- **Direction is not a usable signal.** Directional accuracy sits between 46.7% and 55.0% across
  horizons, inside the binomial noise band around a coin flip.
- **Calibration degrades with horizon.** The h=12 interval covers 78.8% of outcomes against a
  nominal 90%, despite an average width of 155 USD/MT. The interval is not too narrow; the error
  distribution changed after the calibration window.
- **The result does not transfer uniformly.** At h=3 the same ladder clears the gate for maize,
  soybeans and cotton but not for wheat or rice.
- **Decision value is modest and in-sample.** A buy-now threshold of +0.5% reduces regret to
  1.59%, against 2.49% for always waiting, on an average price near 267 USD/MT. The report treats
  this as a shadow-deployment hypothesis, not a production setting.

The resulting recommendation is deliberately narrow: **use the model as a planning range at one,
six and twelve months; publish the random walk where the gate fails; do not use it as a
directional trading or daily timing signal; recalibrate the twelve-month band before showing it
to a decision-maker.**

The latest October 2026 origin forecast is 306.46 USD/MT at one month, 304.11 at three months,
309.77 at six months and 321.38 at twelve months, with empirical conformal bands.

### Reconciling the design target

Week 4's design-target matrix specified MASE 0.54 at h=1 and 0.74 at h=12. The executed audit
measures 0.979 and 0.945. The report keeps both numbers side by side and explains the gap as a
difference between a specification and an outcome, not a coding error. The target assumed that a
richer feature set would extract signal from global benchmark prices; the evidence says it did
not. Hiding that gap would have been the real failure.

---

## Folder structure

```
Agribusiness_Model_Evaluation_Reporting_Strategy_Week5.docx          Official Word deliverable
Agribusiness_Model_Evaluation_Reporting_Strategy_Week5_preview.pdf   Rendered PDF preview
Submission_Description_Week5.txt                                     Submission text
data/
  README.md                                                          Provenance, conventions, regeneration
  facts.json                                                         Machine-readable fact base
  metrics_by_horizon.csv                                             Primary scorecard
  metrics_by_commodity.csv                                           Cross-commodity scorecard
  calibration.csv                                                    Nominal vs empirical coverage
  significance.csv                                                   Bootstrap intervals, DM tests, MDE
  regime_metrics.csv                                                 Pre/post-2023 regime split
  volatility_metrics.csv                                             Volatility-tercile split
  decision_curve.csv                                                 Threshold and regret grid
  latest_forecast.csv                                                October 2026 forecast and bands
  fold_predictions_*.csv                                             Fold-level forecasts for all five crops
  folds.csv                                                          Fold origins and target dates
  final_weights.csv                                                  Ensemble weights by horizon
_build/
  evaluation_engine.py       Runs the audit and writes every CSV and facts.json
  rebuild_primary.py         Restores the 60-fold wheat file if cross-commodity runs overwrite it
  diagram_generator.py       Renders the 12 report figures
  docbase.py                 Word styling, tables, callouts and footers
  cover.py                   Cover page and dynamic contents field
  facts.py                   Loads and formats the executed facts
  sec_a.py                   Sections 1–2: doctrine and metric suite
  sec_b.py                   Sections 3–4: evaluation design and visualisation
  sec_c.py                   Sections 5–6: reporting system, executive summary, limitations
  sec_d.py                   Sections 7–8 and Appendices A–F
  build_week5.py             Assembles the DOCX and compacts its figures
  compact_docx.py            Re-encodes embedded PNGs to keep the DOCX under 2 MB
  export_pdf.ps1             Word COM PDF export and field refresh
  scrub_metadata.py          DOCX and PDF metadata anonymisation
  figures/                   12 rendered figures
```

---

## Rebuilding

Run from the repository root:

```powershell
python week5\_build\evaluation_engine.py
python week5\_build\diagram_generator.py
python week5\_build\build_week5.py
powershell -ExecutionPolicy Bypass -File week5\_build\export_pdf.ps1
python week5\_build\scrub_metadata.py all
```

The full audit takes roughly 10 minutes on a laptop because it fits ETS and SARIMAX at 60
origins. The figure, document and PDF steps take under a minute. Microsoft Word is required for
the automated PDF export. The build re-encodes the twelve report figures automatically, so the
DOCX lands at about 1.05 MB — below a 2 MB upload ceiling — without changing page layout or text.

Requires Python 3.10+ with `pandas`, `numpy`, `statsmodels`, `scikit-learn`, `matplotlib`,
`python-docx`, `Pillow` and `pymupdf`. LightGBM is not required; the direct learner is
scikit-learn's `HistGradientBoostingRegressor`.

---

## Lineage and links

- **Extends:** [Week 1 Analysis Plan](../week1/Agribusiness_Data_Analysis_Plan_Week1.docx)
  (Section 5.5 evaluation protocol), [Week 2 Cleaning Strategy](../week2/Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2.docx)
  (panel contracts and missing-data rules), [Week 3 EDA Design](../week3/Agribusiness_EDA_Report_Design_Week3.docx)
  (indicator taxonomy and diagnostics), and [Week 4 Modelling Framework](../week4/Agribusiness_Predictive_Modelling_Framework_Week4.docx)
  (six-rung ladder, rolling-origin design and executed scorecard).
- **Carries forward:** the Week 4 executed notebook and its real World Bank price extract, not the
  design-target matrix.
- **Project repository:** <https://github.com/SamrudhSS/yuvaintern>
