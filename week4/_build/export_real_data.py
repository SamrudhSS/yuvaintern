# -*- coding: utf-8 -*-
"""Extract real World Bank Commodity Pink Sheet data and produce analysis-ready panels."""

import openpyxl
import pandas as pd
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
WB_FILE = REPO_ROOT / "week1" / "_build" / "pink2026.xlsx"
DATA_DIR = HERE.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

wb = openpyxl.load_workbook(WB_FILE, data_only=True)
sheet = wb['Monthly Prices']
data = list(sheet.iter_rows(values_only=True))

target_indices = {
    'Date': 0,
    'Wheat_HRW_USD_MT': 37,
    'Rice_Thai_USD_MT': 32,
    'Maize_USD_MT': 30,
    'Soybeans_USD_MT': 24,
    'Cotton_AIndex_USD_MT': 54,
    'DAP_Fertilizer_USD_MT': 58,
    'Urea_Fertilizer_USD_MT': 60
}

extracted = []
for r in data[6:]:
    date_val = str(r[0]).strip() if r[0] is not None else ''
    if 'M' in date_val:
        row_dict = {'Date_Code': date_val}
        # parse YYYYMmm to YYYY-MM-01
        try:
            yr = int(date_val[:4])
            mo = int(date_val[5:])
            row_dict['Date'] = f"{yr:04d}-{mo:02d}-01"
            row_dict['Year'] = yr
            row_dict['Month'] = mo
        except:
            continue

        for name, col_idx in target_indices.items():
            if name == 'Date': continue
            val = r[col_idx]
            try:
                value = float(val) if val is not None else np.nan
            except:
                value = np.nan
            # The Pink Sheet quotes cotton in US$/kg; the panel is in US$/metric ton.
            if name == 'Cotton_AIndex_USD_MT' and not np.isnan(value):
                value *= 1000.0
            row_dict[name] = value
        extracted.append(row_dict)

df = pd.DataFrame(extracted)
df = df.sort_values('Date').reset_index(drop=True)

# 1. Save the macro World Bank commodity prices (1960 - 2026)
full_csv = DATA_DIR / "world_bank_commodity_prices_1960_2026.csv"
df.to_csv(full_csv, index=False)
print(f"Saved full World Bank prices: {full_csv} ({len(df)} rows)")

# 2. Modern 2000-2026 dataset
df_modern = df[df['Year'] >= 2000].copy().reset_index(drop=True)
modern_csv = DATA_DIR / "world_bank_agricultural_benchmarks_2000_2026.csv"
df_modern.to_csv(modern_csv, index=False)
print(f"Saved modern benchmarks: {modern_csv} ({len(df_modern)} rows)")

# 3. Create a unified multi-commodity panel (2015 - 2026) for ML models
# Melt into long-form time-series panel
commodity_cols = [
    ('Wheat', 'Wheat_HRW_USD_MT'),
    ('Paddy/Rice', 'Rice_Thai_USD_MT'),
    ('Maize', 'Maize_USD_MT'),
    ('Soybean', 'Soybeans_USD_MT'),
    ('Cotton', 'Cotton_AIndex_USD_MT')
]

panel_records = []
for _, row in df[df['Year'] >= 2015].iterrows():
    for c_name, c_col in commodity_cols:
        price = row[c_col]
        dap = row['DAP_Fertilizer_USD_MT']
        urea = row['Urea_Fertilizer_USD_MT']
        panel_records.append({
            'Date': row['Date'],
            'Year': row['Year'],
            'Month': row['Month'],
            'Commodity': c_name,
            'Price_USD_MT': price,
            'DAP_USD_MT': dap,
            'Urea_USD_MT': urea
        })

df_panel = pd.DataFrame(panel_records)
panel_csv = DATA_DIR / "agribusiness_commodity_panel_2015_2026.csv"
df_panel.to_csv(panel_csv, index=False)
print(f"Saved agribusiness panel: {panel_csv} ({len(df_panel)} rows)")

