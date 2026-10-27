# Agribusiness Market Intelligence — Internship Project

Planning and analysis work for the **Junior Data Scientist Internship, Nagpur (22 October – 26 November 2026)**.

The project builds a forecast-ready panel from publicly available Indian and global agricultural data,
computes a documented indicator set, and produces benchmarked price and yield forecasts with a
dashboard and a decision memo.

**Status:** Week 1 submitted · Weeks 2–5 in progress.

---

## Weekly deliverables

| Week | Dates | Task | Deliverable | Status |
|---|---|---|---|---|
| 1 | 22–28 Oct | Agribusiness data analysis planning | [Analysis plan](week1/Agribusiness_Data_Analysis_Plan_Week1.docx) | ✅ Submitted |
| 2 | 29 Oct – 4 Nov | Data cleaning and preprocessing strategy | — | ⬜ Not started |
| 3 | 5–11 Nov | Exploratory data analysis report design | — | ⬜ Not started |
| 4 | 12–18 Nov | Predictive modelling framework | — | ⬜ Not started |
| 5 | 19–26 Nov | Model evaluation and reporting strategy | — | ⬜ Not started |

Each week folder holds the submitted report, its source material, and any supporting code.

---

## The analysis, in one paragraph

Six crops — wheat, paddy, maize, soybean, cotton and onion — across eight Indian states, chosen so that
each crop represents a distinct commercial behaviour rather than a convenient sample. The forecast
target is the monthly modal wholesale price at 1, 3, 6 and 12 months, plus annual yield per state.
Thirty-eight public sources supply the data, thirty indicators carry the signal, and every model must
beat a seasonal naive benchmark before it is reported.

---

## Repository structure

```
week1/   Planning document (report, preview, week notes)
week2/   Data cleaning and preprocessing strategy
week3/   EDA report design
week4/   Predictive modelling framework
week5/   Model evaluation and reporting strategy
```

Deliverables are Word documents, as required by the brief. Where a week produces code, it lives beside
the report in that week's folder.

---

## Data sources

Production: [DES](https://desagri.gov.in/), [FAOSTAT](https://www.fao.org/faostat/en/), [USDA NASS](https://quickstats.nass.usda.gov/api)
Prices: [Agmarknet](https://agmarknet.gov.in/), [data.gov.in](https://data.gov.in/), [World Bank Pink Sheet](https://www.worldbank.org/en/research/commodity-markets)
Climate: [IMD](https://mausam.imd.gov.in/), [NASA POWER](https://power.larc.nasa.gov/), [Copernicus](https://dataspace.copernicus.eu/)
Trade: [UN Comtrade](https://comtradeplus.un.org/), [ITC Trade Map](https://www.trademap.org/)

All sources are public and free at the point of use. Where terms require attribution, the originating
agency is credited in every chart and table.

---

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

---

## Notes

- No proprietary or paid data sits on the critical path.
- Forecasts are reported as intervals; a model that fails to beat the benchmark is reported as a
  failure rather than omitted.
- Analysis is decision support, not investment or agronomic advice.
