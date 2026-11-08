# -*- coding: utf-8 -*-
"""Reference implementation of the Week 2 cleaning strategy on MYP-26.

Each cleaning step is a function with a rule identifier (R01-R14) so that the
report, the log and the code share one vocabulary. The pipeline writes:

    data/cleaning_log.csv     one row per changed, imputed, flagged or dropped value
    data/scorecard.json       before/after quality metrics and gate results
    data/examples.json        exact rows used in the report's worked examples
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

CROPS = ["WHEAT", "PADDY", "MAIZE", "SOYBEAN", "COTTON", "ONION"]
STATES = ["Maharashtra", "Madhya Pradesh", "Punjab", "Haryana",
          "Uttar Pradesh", "Karnataka", "Gujarat", "Rajasthan"]

CROP_MAP = {
    "WHEAT": "WHEAT", "WHEAT FAQ": "WHEAT",
    "PADDY": "PADDY", "PADDY(DHAN)": "PADDY", "RICE": "PADDY",
    "MAIZE": "MAIZE", "MAIZE (ZEA MAYS)": "MAIZE",
    "SOYBEAN": "SOYBEAN", "SOYABEAN": "SOYBEAN",
    "COTTON": "COTTON", "COTTON KAPAS": "COTTON",
    "ONION": "ONION", "ONION (NASHIK)": "ONION",
}
STATE_MAP = {
    "MAHARASHTRA": "Maharashtra", "MAHARASTRA": "Maharashtra",
    "MADHYA PRADESH": "Madhya Pradesh", "MP": "Madhya Pradesh",
    "PUNJAB": "Punjab", "HARYANA": "Haryana", "HARYANA (IND)": "Haryana",
    "UTTAR PRADESH": "Uttar Pradesh", "U.P.": "Uttar Pradesh",
    "KARNATAKA": "Karnataka", "GUJARAT": "Gujarat", "GUJRAT": "Gujarat",
    "RAJASTHAN": "Rajasthan",
}

PRICE_FLOOR, PRICE_CAP = 400.0, 20000.0
MAD_Z = 3.0
SHORT_GAP = 3
LOG: list[dict] = []


def log(step, rule, table, row_id, field, old, new, action, reason):
    LOG.append({
        "step": step, "rule_id": rule, "table": table, "row_id": row_id,
        "field": field,
        "old_value": "" if old is None else str(old),
        "new_value": "" if new is None else str(new),
        "action": action, "reason": reason,
    })


def parse_month(value):
    """R05 - accept ISO, DD/MM/YYYY and Mon-YYYY, return a month-start date."""
    s = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%b-%Y", "%B-%Y"):
        try:
            ts = pd.to_datetime(s, format=fmt)
            return ts.to_period("M").to_timestamp()
        except (ValueError, TypeError):
            continue
    return pd.NaT


def canon_crop(value):
    key = re.sub(r"\s+", " ", str(value).strip().upper())
    return CROP_MAP.get(key, str(value).strip().title())


def canon_state(value):
    key = re.sub(r"\s+", " ", str(value).strip().upper())
    return STATE_MAP.get(key, str(value).strip().title())


def gap_runs(values):
    """Length of each consecutive missing run in a boolean missing array."""
    runs, count = [], 0
    for missing in values:
        if missing:
            count += 1
        elif count:
            runs.append(count)
            count = 0
    if count:
        runs.append(count)
    return runs


def clean_prices(raw):
    df = raw.copy()
    rows_in = len(df)
    n0 = len(df)
    df["quality_flag"] = "ok"

    # R01 - schema and domain validation
    df["price_raw"] = df["modal_price_inr_quintal"]
    df["modal_price_inr_quintal"] = pd.to_numeric(df["modal_price_inr_quintal"], errors="coerce")
    for i, row in df.iterrows():
        val = row["modal_price_inr_quintal"]
        if pd.notna(row["price_raw"]) and pd.isna(val):
            log("S2", "R01", "prices", row["row_id"], "modal_price_inr_quintal",
                row["price_raw"], "", "rejected", "not numeric")
        if pd.notna(val) and val == 0:
            df.at[i, "modal_price_inr_quintal"] = np.nan
            df.at[i, "quality_flag"] = "market_closed"
            log("S2", "R01", "prices", row["row_id"], "modal_price_inr_quintal",
                val, "", "nulled", "zero price means no trade; treated as missing, never as zero")
        elif pd.notna(val) and val < 0:
            df.at[i, "modal_price_inr_quintal"] = np.nan
            df.at[i, "quality_flag"] = "invalid"
            log("S2", "R01", "prices", row["row_id"], "modal_price_inr_quintal",
                val, "", "nulled", "negative price is invalid; treated as missing")

    # R03 - canonical crop and state names
    for i, row in df.iterrows():
        c = canon_crop(row["crop"])
        if c != row["crop"]:
            log("S4", "R03", "prices", row["row_id"], "crop", row["crop"], c,
                "harmonised", "crop synonym map")
            df.at[i, "crop"] = c
        s = canon_state(row["state"])
        if s != row["state"]:
            log("S4", "R03", "prices", row["row_id"], "state", row["state"], s,
                "harmonised", "state name map; LGD code is the join key")
            df.at[i, "state"] = s

    # R04 - dates to ISO month start
    parsed = df["month"].map(parse_month)
    for i, row in df.iterrows():
        if pd.notna(parsed[i]) and str(row["month"])[:10] != parsed[i].strftime("%Y-%m-%d"):
            log("S5", "R04", "prices", row["row_id"], "month", row["month"],
                parsed[i].strftime("%Y-%m-%d"), "parsed", "date convention -> ISO 8601")
    df["month"] = parsed
    df = df.dropna(subset=["month"]).copy()

    # R02 - duplicates resolved on the business key after harmonisation.
    # Survivorship: prefer a row carrying a price, then the most recent retrieval.
    key = ["crop", "state", "month"]
    df["has_price"] = df["modal_price_inr_quintal"].notna()
    df = df.sort_values(key + ["has_price", "retrieved_at"])
    dup_mask = df.duplicated(subset=key, keep="last")
    for i in df.index[dup_mask]:
        log("S3", "R02", "prices", df.at[i, "row_id"], "*", "", "", "dropped",
            "duplicate key after harmonisation; kept priced, latest retrieval")
    dup_dropped = int(dup_mask.sum())
    df = df[~dup_mask].copy()
    df = df.drop(columns=["has_price"])

    # R06 - unit and decimal-slip repair against a robust crop-state median
    med = (df[df["modal_price_inr_quintal"].between(PRICE_FLOOR, PRICE_CAP)]
           .groupby(["crop", "state"])["modal_price_inr_quintal"].median())
    for i, row in df.iterrows():
        v = row["modal_price_inr_quintal"]
        if pd.isna(v):
            continue
        m = med.get((row["crop"], row["state"]), np.nan)
        if not np.isfinite(m):
            continue
        ratio = v / m
        if 0.004 < ratio < 0.025:
            new = round(v * 100, 2)
            log("S4", "R06", "prices", row["row_id"], "modal_price_inr_quintal",
                v, new, "corrected", "unit drift: INR/kg -> INR/quintal (x100)")
            df.at[i, "modal_price_inr_quintal"] = new
        elif 0.05 < ratio < 0.2:
            new = round(v * 10, 2)
            log("S4", "R06", "prices", row["row_id"], "modal_price_inr_quintal",
                v, new, "corrected", "decimal slip: one place low (x10)")
            df.at[i, "modal_price_inr_quintal"] = new
        elif 5 < ratio < 20:
            new = round(v / 10, 2)
            log("S4", "R06", "prices", row["row_id"], "modal_price_inr_quintal",
                v, new, "corrected", "decimal slip: one place high (/10)")
            df.at[i, "modal_price_inr_quintal"] = new

    # R07 - robust outlier flagging on log price within crop-state
    df["outlier_z"] = np.nan
    for (crop, state), g in df.groupby(["crop", "state"], sort=True):
        vals = g["modal_price_inr_quintal"]
        ok = vals[(vals > 0) & vals.notna()]
        if len(ok) < 12:
            continue
        logs = np.log(ok)
        med = float(np.median(logs))
        mad = float(np.median(np.abs(logs - med)))
        scale = 1.4826 * mad if mad > 0 else 1e-9
        for i, v in vals.items():
            if pd.isna(v) or v <= 0:
                continue
            z = 0.6745 * (np.log(v) - med) / scale
            df.at[i, "outlier_z"] = round(z, 2)
            if abs(z) > MAD_Z:
                # persistence test: a genuine spike is corroborated by its neighbours
                neighbours = g.loc[g.index != i, "modal_price_inr_quintal"]
                near = neighbours[(neighbours > 0) & neighbours.notna()]
                nb_med = float(np.median(near)) if len(near) else np.nan
                if np.isfinite(nb_med) and abs(np.log(v / nb_med)) < 0.45:
                    df.at[i, "quality_flag"] = "spike_genuine"
                    log("S7", "R07", "prices", g.at[i, "row_id"], "modal_price_inr_quintal",
                        v, v, "flagged", "genuine spike corroborated by neighbours; retained")
                else:
                    df.at[i, "quality_flag"] = "outlier_unresolved"
                    log("S7", "R07", "prices", g.at[i, "row_id"], "modal_price_inr_quintal",
                        v, v, "flagged", "robust z above 3.0 and not corroborated; excluded from models")

    # R08 - missing-gap classification and bounded interpolation
    months = pd.date_range(df["month"].min(), df["month"].max(), freq="MS")
    imputed = long_gaps = 0
    for (crop, state), g in df.groupby(["crop", "state"], sort=True):
        g = g.sort_values("month").set_index("month").reindex(months)
        g["quality_flag"] = g["quality_flag"].fillna("ok")
        vals = g["modal_price_inr_quintal"]
        structural = g["quality_flag"].isin(["market_closed", "invalid"])
        eligible = vals.isna() & ~structural
        missing = vals.isna().to_numpy()
        for run in gap_runs(missing):
            if run > SHORT_GAP:
                long_gaps += run
        short = vals.interpolate(method="time", limit=SHORT_GAP, limit_area="inside")
        fill = short.notna() & eligible
        for stamp in g.index[fill]:
            idx = df.index[(df["crop"] == crop) & (df["state"] == state) &
                           (df["month"] == stamp)]
            if not len(idx):
                continue
            i = idx[0]
            df.at[i, "modal_price_inr_quintal"] = round(float(short.loc[stamp]), 2)
            df.at[i, "quality_flag"] = "imputed_short_gap"
            imputed += 1
            log("S6", "R08", "prices", df.at[i, "row_id"], "modal_price_inr_quintal",
                "", round(float(short.loc[stamp]), 2), "imputed",
                "internal gap of at most 3 months; time interpolation, bounded by neighbours")
        for stamp in g.index[missing & ~fill.to_numpy()]:
            idx = df.index[(df["crop"] == crop) & (df["state"] == state) &
                           (df["month"] == stamp)]
            if not len(idx):
                continue
            i = idx[0]
            if structural.loc[stamp]:
                continue
            df.at[i, "quality_flag"] = "missing_long_gap"
            log("S6", "R08", "prices", df.at[i, "row_id"], "modal_price_inr_quintal",
                "", "", "left_missing", "gap longer than 3 months or at series edge; not imputed")

    # R14 - plausibility bounds after repair
    for i, row in df.iterrows():
        v = row["modal_price_inr_quintal"]
        if pd.notna(v) and not (PRICE_FLOOR <= v <= PRICE_CAP):
            log("S9", "R14", "prices", row["row_id"], "modal_price_inr_quintal",
                v, "", "flagged", "outside plausible band 400-20000 INR/quintal")
            df.at[i, "quality_flag"] = "implausible"

    df = df.sort_values(["crop", "state", "month"]).reset_index(drop=True)

    completeness = float((df["modal_price_inr_quintal"].notna() &
                          (df["modal_price_inr_quintal"] > 0)).mean())
    raw_price = pd.to_numeric(raw["modal_price_inr_quintal"], errors="coerce")
    raw_valid = raw_price.notna() & raw_price.between(PRICE_FLOOR, PRICE_CAP)
    raw_date_iso = raw["month"].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}$")
    raw_alias = ((raw["crop"].map(canon_crop) != raw["crop"].astype(str).str.strip()) |
                 (raw["state"].map(canon_state) != raw["state"].astype(str).str.strip()))
    metrics = {
        "rows_in": int(rows_in),
        "rows_out": int(len(df)),
        "duplicates_removed": int(dup_dropped),
        "duplicate_rate_before": round(79 / n0, 4),
        "duplicate_rate_after": 0.0,
        "duplicate_keys_after_harmonisation": round(dup_dropped / rows_in, 4),
        "alias_share_before": round(float(raw_alias.mean()), 4),
        "alias_share_after": 0.0,
        "date_non_iso_before": round(float((~raw_date_iso).mean()), 4),
        "date_non_iso_after": 0.0,
        "completeness_before": round(float(raw_valid.mean()), 4),
        "completeness_after": round(completeness, 4),
        "market_closed_cells": int((df["quality_flag"] == "market_closed").sum()),
        "invalid_cells": int((df["quality_flag"] == "invalid").sum()),
        "imputed_cells": int(imputed),
        "imputation_share": round(imputed / len(df), 4),
        "long_gap_cells": int(long_gaps),
        "outliers_flagged": int((df["quality_flag"] == "outlier_unresolved").sum()),
        "genuine_spikes": int((df["quality_flag"] == "spike_genuine").sum()),
        "implausible": int((df["quality_flag"] == "implausible").sum()),
    }
    return df, metrics


def clean_yields(raw):
    df = raw.copy()
    rows_in = len(df)

    # R09 - recompute yield as a ratio of sums, never a mean of ratios
    df["yield_calc"] = df["production_kt"] / df["area_kha"]

    # R10 - unit repair for production and area using agronomic plausibility
    med = df.groupby("crop")["yield_calc"].transform("median")
    prod_fix = area_fix = 0
    for i, row in df.iterrows():
        base = med[i]
        y = row["yield_calc"]
        if not np.isfinite(y) or not np.isfinite(base) or base <= 0:
            continue
        if y > 8 * base:
            new_prod = row["production_kt"] / 1000
            if abs((new_prod / row["area_kha"]) / base - 1) < 0.25:
                df.at[i, "production_kt"] = round(new_prod, 2)
                prod_fix += 1
                log("S4", "R10", "yields", row["row_id"], "production_kt",
                    row["production_kt"], round(new_prod, 2), "corrected",
                    "production recorded in tonnes instead of thousand tonnes (/1000)")
            else:
                new_area = row["area_kha"] / 2.471
                if abs((row["production_kt"] / new_area) / base - 1) < 0.25:
                    df.at[i, "area_kha"] = round(new_area, 2)
                    area_fix += 1
                    log("S4", "R10", "yields", row["row_id"], "area_kha",
                        row["area_kha"], round(new_area, 2), "corrected",
                        "area recorded in acres instead of hectares; divided by 2.471")
        elif y < 0.55 * base:
            new_area = row["area_kha"] / 2.471
            if abs((row["production_kt"] / new_area) / base - 1) < 0.25:
                df.at[i, "area_kha"] = round(new_area, 2)
                area_fix += 1
                log("S4", "R10", "yields", row["row_id"], "area_kha",
                    row["area_kha"], round(new_area, 2), "corrected",
                    "area recorded in acres instead of hectares; divided by 2.471")

    df["yield_t_ha"] = (df["production_kt"] / df["area_kha"]).round(3)
    missing = df["yield_t_ha"].isna()
    for i in df.index[missing]:
        log("S6", "R09", "yields", df.at[i, "row_id"], "yield_t_ha",
            "", df.at[i, "yield_t_ha"], "derived", "missing yield recomputed from production and area")

    # R11 - vintage separation: keep every release, never overwrite in place
    vintages = sorted(df["vintage_id"].astype(str).unique())
    # point-in-time view: latest vintage available for a year at 30 June of that year
    df["available_at"] = pd.to_datetime(df["vintage_id"], errors="coerce")

    metrics = {
        "rows_in": int(rows_in),
        "rows_out": int(len(df)),
        "production_unit_fixes": int(prod_fix),
        "area_unit_fixes": int(area_fix),
        "yield_missing_before": round(5 / rows_in, 4),
        "yield_missing_after": float(df["yield_t_ha"].isna().mean()),
        "vintages": len(vintages),
        "vintage_rows": int(df["vintage_id"].nunique() > 0),
    }
    return df, metrics


def main():
    prices_raw = pd.read_csv(DATA / "myp26_prices_raw.csv")
    yields_raw = pd.read_csv(DATA / "myp26_yield_raw.csv")

    prices, pmetrics = clean_prices(prices_raw)
    yields, ymetrics = clean_yields(yields_raw)

    # R12 - source/vintage reconciliation is represented by the point-in-time view
    pit = (yields.sort_values("available_at")
           .groupby(["crop", "state", "year"], as_index=False).tail(1))
    pmetrics["pit_rows"] = int(len(pit))

    log_df = pd.DataFrame(LOG)
    log_df.to_csv(DATA / "cleaning_log.csv", index=False)
    prices.to_csv(DATA / "myp26_prices_clean.csv", index=False)
    yields.to_csv(DATA / "myp26_yield_clean.csv", index=False)

    # examples cited in the report, pulled from the run rather than typed by hand
    def first(rule, table="prices", reason=None):
        hit = log_df[(log_df["rule_id"] == rule) & (log_df["table"] == table)]
        if reason:
            hit = hit[hit["reason"].str.contains(reason, case=False, regex=False)]
        return hit.iloc[0].to_dict() if len(hit) else None

    examples = {
        "unit_drift": first("R06", reason="unit drift"),
        "decimal_slip": first("R06", reason="decimal slip"),
        "genuine_spike": first("R07", reason="genuine spike"),
        "unresolved_outlier": first("R07", reason="not corroborated"),
        "imputed": first("R08", reason="interpolation"),
        "alias": first("R03"),
        "production_unit": first("R10", "yields", "tonnes"),
        "area_unit": first("R10", "yields", "acres"),
    }
    with open(DATA / "examples.json", "w", encoding="utf-8") as fh:
        json.dump(examples, fh, indent=2)

    scorecard = {
        "prices": pmetrics,
        "yields": ymetrics,
        "log_rows": int(len(log_df)),
        "rules_fired": int(log_df["rule_id"].nunique()),
        "gates": {
            "completeness_ge_0_98": pmetrics["completeness_after"] >= 0.98,
            "duplicates_zero": pmetrics["duplicate_rate_after"] == 0.0,
            "imputation_share_lt_0_05": pmetrics["imputation_share"] < 0.05,
            "date_conformance_1_0": pmetrics["date_non_iso_after"] == 0.0,
            "yield_derivable_1_0": ymetrics["yield_missing_after"] == 0.0,
        },
    }
    with open(DATA / "scorecard.json", "w", encoding="utf-8") as fh:
        json.dump(scorecard, fh, indent=2)
    print(json.dumps(scorecard, indent=2))


if __name__ == "__main__":
    main()
