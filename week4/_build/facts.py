# -*- coding: utf-8 -*-
"""Load model facts for Week 4 report sections."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
with open(HERE / "data" / "model_facts.json", "r", encoding="utf-8") as f:
    FACTS = json.load(f)

CROPS   = FACTS["scope"]["crops"]
STATES  = FACTS["scope"]["states"]
MASE    = FACTS["model_ladder"]["mase"]
SMAPE   = FACTS["model_ladder"]["smape"]
COV     = FACTS["model_ladder"]["interval_coverage_90pct"]
SHAP    = FACTS["shap_importances_pct"]
LEAKAGE = FACTS["leakage_rules"]
SPLIT   = FACTS["rolling_origin_split"]
FE      = FACTS["feature_engineering"]

