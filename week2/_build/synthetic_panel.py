# -*- coding: utf-8 -*-
"""Generate the hypothetical Mandi-Yield Panel (MYP-26) with known defects.

The generator is seeded, so the same script always produces the same panel and
the same injected-defect manifest. Defects are recorded as they are injected;
the cleaning pipeline never sees the manifest, so recovery rates are honest.

Outputs (in ./data):
    myp26_prices_raw.csv     monthly state-level price panel, defects included
    myp26_yield_raw.csv      annual production / area / yield panel, defects included
    injected_defects.json    what was injected, where, and at what rate
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261104
OUT = Path(__file__).resolve().parent / "data"
OUT.mkdir(exist_ok=True)

CROPS = ["WHEAT", "PADDY", "MAIZE", "SOYBEAN", "COTTON", "ONION"]
STATES = ["Maharashtra", "Madhya Pradesh", "Punjab", "Haryana",
          "Uttar Pradesh", "Karnataka", "Gujarat", "Rajasthan"]

BASE_PRICE = {"WHEAT": 2400, "PADDY": 2100, "MAIZE": 1900,
              "SOYBEAN": 4600, "COTTON": 7000, "ONION": 1800}
BASE_YIELD = {"WHEAT": 3.4, "PADDY": 4.0, "MAIZE": 3.1,
              "SOYBEAN": 1.1, "COTTON": 0.55, "ONION": 19.0}

STATE_MULT = {"Maharashtra": 1.06, "Madhya Pradesh": 0.94, "Punjab": 1.08,
              "Haryana": 1.04, "Uttar Pradesh": 0.97, "Karnataka": 1.02,
              "Gujarat": 1.03, "Rajasthan": 0.99}

# crop-specific seasonal shape, month 1..12
SEASON = {
    "WHEAT": [1.02, 1.01, 0.96, 0.93, 0.95, 1.00, 1.03, 1.04, 1.03, 1.01, 1.01, 1.01],
    "PADDY": [1.01, 1.00, 0.97, 0.96, 0.98, 1.01, 1.03, 1.04, 1.04, 1.02, 0.98, 0.96],
    "MAIZE": [1.03, 1.02, 0.99, 0.96, 0.97, 1.00, 1.02, 1.03, 1.03, 1.00, 0.98, 0.97],
    "SOYBEAN": [1.04, 1.03, 1.00, 0.96, 0.95, 0.97, 1.00, 1.02, 1.04, 1.06, 1.04, 1.01],
    "COTTON": [1.02, 1.01, 1.00, 0.98, 0.97, 0.98, 1.00, 1.01, 1.02, 1.03, 1.02, 1.01],
    "ONION": [1.10, 1.18, 1.22, 1.15, 1.00, 0.86, 0.80, 0.82, 0.90, 1.05, 1.20, 1.14],
}

CROP_ALIASES = {
    "WHEAT": ["Wheat FAQ", "WHEAT"],
    "PADDY": ["Paddy(Dhan)", "Rice", "PADDY"],
    "MAIZE": ["Maize (Zea mays)", "MAIZE"],
    "SOYBEAN": ["Soyabean", "SOYBEAN"],
    "COTTON": ["Cotton Kapas", "COTTON"],
    "ONION": ["Onion (Nashik)", "ONION"],
}
STATE_ALIASES = {
    "Maharashtra": ["Maharastra", "Maharashtra"],
    "Madhya Pradesh": ["MP", "Madhya Pradesh"],
    "Punjab": ["Punjab ", "Punjab"],
    "Haryana": ["Haryana (IND)", "Haryana"],
    "Uttar Pradesh": ["U.P.", "Uttar Pradesh"],
    "Karnataka": ["Karnataka ", "Karnataka"],
    "Gujarat": ["Gujrat", "Gujarat"],
    "Rajasthan": ["Rajasthan ", "Rajasthan"],
}


def monthly_panel(rng):
    months = pd.date_range("2020-01-01", periods=72, freq="MS")
    rows = []
    for crop in CROPS:
        for state in STATES:
            for i, month in enumerate(months):
                trend = (1.0 + 0.04 / 12) ** i
                seasonal = SEASON[crop][month.month - 1]
                noise = float(rng.lognormal(mean=0.0, sigma=0.075))
                price = BASE_PRICE[crop] * STATE_MULT[state] * trend * seasonal * noise
                # a genuine, documented onion spike: Oct-Dec 2023
                if crop == "ONION" and month.year == 2023 and month.month in (10, 11, 12):
                    price *= 1.55
                # a second genuine event in a low-variance series: wheat, Rajasthan, 2022
                if crop == "WHEAT" and state == "Rajasthan" and month.year == 2022 and month.month in (2, 3):
                    price *= 1.55
                rows.append({
                    "crop": crop,
                    "state": state,
                    "month": month.strftime("%Y-%m-%d"),
                    "modal_price_inr_quintal": round(price, 2),
                    "source_id": "AGMARKNET",
                    "retrieved_at": "2026-10-27T09:14:00Z",
                    "vintage_id": "2026-10-27",
                })
    return pd.DataFrame(rows)


def yield_panel(rng):
    rows = []
    for crop in CROPS:
        for state in STATES:
            for year in range(2020, 2026):
                trend = 1.0 + 0.012 * (year - 2020)
                weather = float(rng.normal(1.0, 0.10))
                yld = BASE_YIELD[crop] * STATE_MULT[state] * trend * weather
                area = {"WHEAT": 350, "PADDY": 420, "MAIZE": 300, "SOYBEAN": 480,
                        "COTTON": 610, "ONION": 55}[crop] * (0.6 + 0.4 * STATE_MULT[state])
                area *= float(rng.uniform(0.95, 1.05))
                production = yld * area  # kt, because area is kha
                vintage = "revised" if year < 2024 else "advance"
                rows.append({
                    "crop": crop,
                    "state": state,
                    "year": year,
                    "production_kt": round(production, 2),
                    "area_kha": round(area, 2),
                    "yield_t_ha": round(production / area, 3),
                    "vintage": vintage,
                    "vintage_id": f"{year}-07-14" if vintage == "advance" else f"{year}-12-01",
                    "source_id": "DES",
                    "retrieved_at": "2026-10-27T09:20:00Z",
                })
    # 2024 and 2025 carry three releases each: advance, second, revised
    extra = []
    for row in rows:
        if row["year"] in (2024, 2025):
            for v, factor, date in (("second", 0.98, f"{row['year']}-10-01"),
                                    ("revised", 1.015, f"{row['year'] + 1}-02-15")):
                r = dict(row)
                r["production_kt"] = round(row["production_kt"] * factor, 2)
                r["yield_t_ha"] = round(r["production_kt"] / r["area_kha"], 3)
                r["vintage"] = v
                r["vintage_id"] = date
                extra.append(r)
    return pd.concat([pd.DataFrame(rows), pd.DataFrame(extra)], ignore_index=True)


def inject_prices(df, rng):
    n = len(df)
    log = {"rates": {}, "indices": {}}
    df = df.copy()
    df.insert(0, "row_id", [f"P{i:05d}" for i in range(1, n + 1)])

    def take(k):
        return rng.choice(n, size=k, replace=False)

    # 1. exact duplicates (same payload, later retrieval)
    idx = take(79)
    dup = df.iloc[idx].copy()
    dup["row_id"] = [f"D{i:05d}" for i in range(1, len(dup) + 1)]
    dup["retrieved_at"] = "2026-10-28T06:00:00Z"
    df = pd.concat([df, dup], ignore_index=True)
    log["rates"]["duplicate_rows"] = 79 / (n + 79)
    log["indices"]["duplicate_rows"] = len(idx)

    # 2. missing price
    idx = take(166)
    df.loc[idx, "modal_price_inr_quintal"] = np.nan
    log["rates"]["missing_price"] = len(idx) / n
    log["indices"]["missing_price"] = len(idx)

    # 3. zero price: market closed / no trade
    idx = take(41)
    df.loc[idx, "modal_price_inr_quintal"] = 0.0
    log["rates"]["zero_price"] = len(idx) / n
    log["indices"]["zero_price"] = len(idx)

    # 4. unit drift: rupees per kg instead of per quintal
    idx = take(38)
    df.loc[idx, "modal_price_inr_quintal"] = (
        df.loc[idx, "modal_price_inr_quintal"] / 100.0).round(3)
    log["rates"]["unit_drift"] = len(idx) / n
    log["indices"]["unit_drift"] = len(idx)

    # 5. transcription outliers: decimal slip by one place
    idx = take(31)
    up, down = idx[:21], idx[21:]
    df.loc[up, "modal_price_inr_quintal"] *= 10
    df.loc[down, "modal_price_inr_quintal"] /= 10
    log["rates"]["outlier_typo"] = len(idx) / n
    log["indices"]["outlier_typo"] = len(idx)

    # 5b. non-decimal transcription errors: a digit changed, so no clean factor
    idx = take(7)
    df.loc[idx, "modal_price_inr_quintal"] = (
        df.loc[idx, "modal_price_inr_quintal"] * 3.2).round(2)
    log["rates"]["outlier_unresolved"] = len(idx) / n
    log["indices"]["outlier_unresolved"] = len(idx)

    # 6. date format drift
    idx = take(117)
    for j, i in enumerate(idx):
        ts = pd.Timestamp(df.loc[i, "month"])
        df.loc[i, "month"] = (ts.strftime("%d/%m/%Y") if j % 2 == 0
                              else ts.strftime("%b-%Y"))
    log["rates"]["date_format"] = len(idx) / n
    log["indices"]["date_format"] = len(idx)

    # 7. crop aliases and state name variants
    idx = take(69)
    for i in idx:
        df.at[i, "crop"] = str(rng.choice(CROP_ALIASES[df.at[i, "crop"]]))
    log["rates"]["crop_alias"] = len(idx) / n
    log["indices"]["crop_alias"] = len(idx)

    idx = take(52)
    for i in idx:
        df.at[i, "state"] = str(rng.choice(STATE_ALIASES[df.at[i, "state"]]))
    log["rates"]["state_alias"] = len(idx) / n
    log["indices"]["state_alias"] = len(idx)

    # 8. a handful of impossible negative prices
    idx = take(6)
    df.loc[idx, "modal_price_inr_quintal"] = -abs(df.loc[idx, "modal_price_inr_quintal"])
    log["rates"]["negative_price"] = len(idx) / n
    log["indices"]["negative_price"] = len(idx)

    return df.sample(frac=1.0, random_state=SEED).reset_index(drop=True), log


def inject_yields(df, rng):
    df = df.copy()
    df.insert(0, "row_id", [f"Y{i:05d}" for i in range(1, len(df) + 1)])
    log = {"rates": {}, "indices": {}}
    n = len(df)

    idx = rng.choice(df.index, size=6, replace=False)
    df.loc[idx, "production_kt"] = (df.loc[idx, "production_kt"] * 1000).round(2)
    log["rates"]["production_unit_error"] = len(idx) / n
    log["indices"]["production_unit_error"] = len(idx)

    idx = rng.choice(df.index, size=4, replace=False)
    df.loc[idx, "area_kha"] = (df.loc[idx, "area_kha"] * 2.471).round(2)
    log["rates"]["area_unit_error"] = len(idx) / n
    log["indices"]["area_unit_error"] = len(idx)

    idx = rng.choice(df.index, size=5, replace=False)
    df.loc[idx, "yield_t_ha"] = np.nan
    log["rates"]["missing_yield"] = len(idx) / n
    log["indices"]["missing_yield"] = len(idx)

    return df, log


def main():
    rng = np.random.default_rng(SEED)
    prices = monthly_panel(rng)
    yields = yield_panel(rng)
    prices, price_log = inject_prices(prices, rng)
    yields, yield_log = inject_yields(yields, rng)

    prices.to_csv(OUT / "myp26_prices_raw.csv", index=False)
    yields.to_csv(OUT / "myp26_yield_raw.csv", index=False)
    manifest = {
        "seed": SEED,
        "panel": "MYP-26",
        "prices": {"rows": int(len(prices)),
                   "cells": int(len(prices) * 1),
                   "injected": price_log},
        "yields": {"rows": int(len(yields)), "injected": yield_log},
    }
    with open(OUT / "injected_defects.json", "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"prices {len(prices)} rows, yields {len(yields)} rows -> {OUT}")


if __name__ == "__main__":
    main()
