# Week 4 — Predictive Modelling Framework

**Dates:** 12–18 November 2026 · **Status:** ⬜ Not started

## Task

Propose a predictive modelling framework for forecasting agricultural yields: the rationale, the
features that influence yield, the training process (splitting, engineering, selection, validation) and
how performance and reliability will be evaluated.

## Planned content

- Rationale for predictive modelling in crop yield and resource optimisation.
- Feature set with a stated reason for each: weather windows by crop stage, vegetation indices, soil,
  input intensity, irrigation, lagged yield, price signals, policy flags.
- Training design: rolling-origin splits for time series, no random shuffling, leakage tests.
- Model ladder: seasonal naive → ETS → SARIMAX → gradient boosting → ensemble, with the promotion rule
  from Section 5.5 of the [Week 1 plan](../week1/).
- Validation: MASE, sMAPE, RMSE, interval coverage, directional accuracy, bias.
- Reliability: explainability with SHAP, stability across folds, documented failure conditions.
- How the framework transfers to other agribusiness settings — different crops, regions and data
  availability.

## Files

Added on submission.

## Links

- Extends: Week 1, Section 5.3 (model ladder), 5.4 (feature rules), 5.5 (evaluation protocol).
