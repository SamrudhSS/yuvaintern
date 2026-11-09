# -*- coding: utf-8 -*-
"""Facts loader for Week 3 EDA Report Design."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "data" / "eda_facts.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    FACTS = json.load(f)

CROPS = FACTS["crops"]
STATES = FACTS["states"]
CROP_STATS = FACTS["crop_stats"]
STATE_YIELD_STATS = FACTS["state_yield_stats"]
ANOMALIES = FACTS["anomalies"]
CORR_BENCH = FACTS["correlation_benchmarks"]

def fmt_num(val, dec=1):
    if val is None:
        return "—"
    if isinstance(val, (int, float)):
        return f"{val:,.{dec}f}"
    return str(val)

def fmt_pct(val, dec=1):
    if val is None:
        return "—"
    return f"{val:.{dec}f}%"

