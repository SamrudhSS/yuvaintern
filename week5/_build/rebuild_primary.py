# -*- coding: utf-8 -*-
"""Rebuild the primary 60-fold prediction file without re-running the audit.

The cross-commodity loop writes its own 45-fold wheat file; this script restores
the primary 60-fold artefact used by the figures. It is deterministic and checks
that the rebuilt metrics match the published scorecard.
"""

from pathlib import Path

import numpy as np
import pandas as pd

import evaluation_engine as E

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

prices = E.load_prices()
design, features = E.build_design(prices, "Wheat_HRW_USD_MT")
print(f"design {len(design)} months x {len(features)} predictors")
wheat = E.run_ladder(design, features, E.HORIZONS, label="Wheat")
folds = wheat["folds"]
print("rows", len(folds), "folds", folds["fold"].nunique())
folds.to_csv(DATA / "fold_predictions_wheat.csv", index=False)
folds.to_csv(DATA / "fold_predictions_wheat_primary.csv", index=False)

metrics = E.build_metrics(folds, wheat["scale"])
published = pd.read_csv(DATA / "metrics_by_horizon.csv")
joined = metrics.merge(published, on=["horizon", "model_key"], suffixes=("_new", "_pub"))
delta = float(np.max(np.abs(joined["mae_new"] - joined["mae_pub"])))
print(f"max MAE difference versus published scorecard: {delta:.9f}")
assert delta < 1e-6, "rebuilt predictions do not match the published scorecard"
print("primary fold file rebuilt")
