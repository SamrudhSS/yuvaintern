# Week 4 data — provenance and units

## Source

All series come from the **World Bank Commodity Markets Outlook** historical monthly price
workbook (the "Pink Sheet"):

- Publisher: World Bank Prospects Group
- Workbook: `CMO-Historical-Data-Monthly.xlsx`
- Sheet parsed: `Monthly Prices`
- Current vintage: November 2026 edition, published 3 November 2026
- Live URL used by the notebook:
  `https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx`
- Terms: World Bank open data, CC BY 4.0. Cite *World Bank Commodity Markets Outlook*.

The World Bank rotates the document hash each month. The notebook tries the current edition first
and a long-lived mirror second, then rebuilds the prepared CSV from whichever workbook it obtains.
No synthetic values are inserted.

## Files

| File | Rows | Coverage | Purpose |
|---|---:|---|---|
| `world_bank_commodity_prices_1960_2026.csv` | 802 | 1960-01 to 2026-10 | Full monthly extract used by the notebook |
| `world_bank_agricultural_benchmarks_2000_2026.csv` | 322 | 2000-01 to 2026-10 | Modern benchmark window |
| `agribusiness_commodity_panel_2015_2026.csv` | 710 | 2015-01 to 2026-10 | Long-form five-commodity panel |

The `notebook_*.csv` files are outputs written by the executed notebook. They are regenerated on
every run and should not be edited by hand.

## Columns and units

| Column | World Bank header | Unit |
|---|---|---|
| `Wheat_HRW_USD_MT` | Wheat, US HRW | USD / metric ton |
| `Rice_Thai_USD_MT` | Rice, Thai 5% | USD / metric ton |
| `Maize_USD_MT` | Maize | USD / metric ton |
| `Soybeans_USD_MT` | Soybeans | USD / metric ton |
| `Cotton_AIndex_USD_MT` | Cotton, A Index | USD / metric ton |
| `DAP_Fertilizer_USD_MT` | DAP | USD / metric ton |
| `Urea_Fertilizer_USD_MT` | Urea | USD / metric ton |

**Unit correction:** the Pink Sheet quotes cotton in **USD/kg**. `export_real_data.py` multiplies
that series by 1,000 so the column is genuinely USD/metric ton. Earlier versions of the extract
carried the USD/kg values under a `USD_MT` label; that has been fixed.

## Regenerating

From the repository root:

```powershell
python week4/_build/export_real_data.py
```

The script reads `week1/_build/pink2026.xlsx` (a local snapshot of the World Bank workbook) and
rewrites the three CSVs above. If the snapshot is absent, the notebook downloads the workbook
directly, so the data is never dependent on a single machine.

## Observed data quality

- The monthly date index is complete: no missing months between 1960-01 and 2026-10.
- DAP has 84 missing values in 1960–1966; the modern 2000+ window used for modelling is complete.
- Prices are nominal US dollars, as published. No deflator is applied.
- These are global reference prices, not Indian mandi prices. See the notebook's limitations section.
