# -*- coding: utf-8 -*-
"""Derive the exact figures quoted in the report from the pipeline outputs.

Nothing in the report's numbers is typed by hand: the build reads
data/report_facts.json, which this script regenerates from the run.
"""

from __future__ import annotations

import json
import hashlib
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

log = pd.read_csv(DATA / "cleaning_log.csv")
score = json.loads((DATA / "scorecard.json").read_text(encoding="utf-8"))
manifest = json.loads((DATA / "injected_defects.json").read_text(encoding="utf-8"))
examples = json.loads((DATA / "examples.json").read_text(encoding="utf-8"))
prices = pd.read_csv(DATA / "myp26_prices_clean.csv")
yields = pd.read_csv(DATA / "myp26_yield_clean.csv")

by_rule = log.groupby(["rule_id", "action"]).size().reset_index(name="n")
rule_counts = {f"{r.rule_id}|{r.action}": int(r.n) for r in by_rule.itertuples()}

# reason-level counts for the narratives
def count_reason(text):
    return int(log["reason"].str.contains(text, case=False, regex=False).sum())


def context(example):
    if not example:
        return None
    table_name = example["table"]
    frame = prices if table_name == "prices" else yields
    hit = frame[frame["row_id"] == example["row_id"]]
    if not len(hit):
        return None
    row = hit.iloc[0]
    keep = ["crop", "state", "month", "year", "modal_price_inr_quintal",
            "production_kt", "area_kha", "yield_t_ha", "vintage_id", "quality_flag"]
    return {k: (str(row[k]) if k in row and str(row[k]) != "nan" else None) for k in keep}


imputed_neighbours = {"prev": None, "next": None}
_iex = examples.get("imputed")
if _iex:
    _hit = prices[prices["row_id"] == _iex["row_id"]]
    if len(_hit):
        _r = _hit.iloc[0]
        _g = (prices[(prices["crop"] == _r["crop"]) & (prices["state"] == _r["state"])]
              .sort_values("month").reset_index(drop=True))
        _loc = _g.index[_g["month"] == _r["month"]]
        if len(_loc):
            _j = int(_loc[0])
            if _j > 0:
                imputed_neighbours["prev"] = round(float(
                    _g.loc[_j - 1, "modal_price_inr_quintal"]), 2)
            if _j + 1 < len(_g):
                imputed_neighbours["next"] = round(float(
                    _g.loc[_j + 1, "modal_price_inr_quintal"]), 2)

facts = {
    "scorecard": score,
    "manifest": manifest,
    "examples": examples,
    "example_context": {k: context(v) for k, v in examples.items()},
    "imputed_neighbours": imputed_neighbours,
    "vintage_case": (
        yields[(yields["crop"] == "WHEAT") & (yields["state"] == "Maharashtra") &
               (yields["year"] == 2024)]
        [["vintage", "vintage_id", "production_kt", "area_kha", "yield_t_ha"]]
        .sort_values("vintage_id").to_dict(orient="records")
    ),
    "hashes": {
        "prices_clean": hashlib.sha256((DATA / "myp26_prices_clean.csv").read_bytes()).hexdigest(),
        "yield_clean": hashlib.sha256((DATA / "myp26_yield_clean.csv").read_bytes()).hexdigest(),
        "cleaning_log": hashlib.sha256((DATA / "cleaning_log.csv").read_bytes()).hexdigest(),
    },
    "log": {
        "rows": int(len(log)),
        "rules_fired": sorted(log["rule_id"].unique().tolist()),
        "by_rule_action": rule_counts,
        "unit_drift_fixes": count_reason("unit drift"),
        "decimal_fixes": count_reason("decimal slip"),
        "genuine_spike_flags": count_reason("genuine spike"),
        "unresolved_flags": count_reason("not corroborated"),
        "crop_aliases": int(((log["rule_id"] == "R03") & (log["field"] == "crop")).sum()),
        "state_aliases": int(((log["rule_id"] == "R03") & (log["field"] == "state")).sum()),
        "duplicate_drops": int(((log["rule_id"] == "R02")).sum()),
        "imputations": count_reason("interpolation"),
        "production_fixes": count_reason("thousand tonnes"),
        "area_fixes": count_reason("acres"),
    },
    "panel": {
        "crops": int(prices["crop"].nunique()),
        "states": int(prices["state"].nunique()),
        "months": int(prices["month"].nunique()),
        "rows": int(len(prices)),
        "cells": int(len(prices)),
        "yield_rows": int(len(yields)),
        "vintages": int(yields["vintage_id"].nunique()),
        "coverage_by_crop": {
            crop: round(float((g["modal_price_inr_quintal"].notna() &
                               (g["modal_price_inr_quintal"] > 0)).mean()), 4)
            for crop, g in prices.groupby("crop")
        },
        "median_price_by_crop": {
            crop: round(float(g["modal_price_inr_quintal"].median()), 1)
            for crop, g in prices.groupby("crop")
        },
    },
}

with open(DATA / "report_facts.json", "w", encoding="utf-8") as fh:
    json.dump(facts, fh, indent=2)

print(json.dumps({k: v for k, v in facts.items() if k != "manifest"}, indent=2)[:4000])
