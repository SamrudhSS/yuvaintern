# Week 3 — Exploratory Data Analysis (EDA) Report Design

**Dates:** 5–11 November 2026 · **Status:** ✅ Submitted (v1.0)

## Deliverables

| File | Purpose |
|---|---|
| [`Agribusiness_EDA_Report_Design_Week3.docx`](Agribusiness_EDA_Report_Design_Week3.docx) | Official Word deliverable (31 pages, 10,247 words, 10 tables, 3 figures) |
| [`Agribusiness_EDA_Report_Design_Week3_preview.pdf`](Agribusiness_EDA_Report_Design_Week3_preview.pdf) | Rendered publication PDF preview with refreshed TOC and header/footer fields |

The report provides the complete architectural and methodological blueprint for the downstream
Exploratory Data Analysis (EDA) report in agribusiness intelligence. It operationalizes raw agricultural
observations into verified market signals and strategic decisions across six focal crops (Wheat, Paddy,
Maize, Soybean, Cotton, Onion) and eight key Indian agricultural states over a 72-month historical panel
(2021–2026).

---

## What the design report commits to

- **Variable Architecture (42 Metrics across 5 Lenses):** Production & yield fundamentals, mandi market
  microstructure (modal prices, arrivals, price flexibility), climate & remote sensing (SPEI-3, NDVI anomaly,
  Heat Degree Days), agronomic factor inputs (fertilizers, diesel, agricultural wages), and trade/policy
  interventions (FCI buffer norms, import parity, export restrictions).
- **Five Analytical Typologies:** Univariate non-Gaussian distributional profiling (zero-inflation, heavy-tail
  kurtosis, ADF/KPSS integration orders), bivariate price elasticity curves, robust Seasonal-Trend
  Decomposition using LOESS (STL), spatial market integration (Law of One Price testing, spatial CV, Moran's I
  spatial autocorrelation), and multivariate PCA orthogonalization of collinear agro-climatic indicators.
- **Cognitive Visualization Architecture:** Formal decision tree matching analytical question types to
  optimal perceptual encodings (small-multiples faceted lines, seasonal subseries/cycle plots, phase-space
  cobweb trajectories, binned geospatial choropleths, violin plots with jittered observations, and CCF lead-lag
  heatmaps). Prohibits misleading dual Y-axes and enforces color-blind-safe palettes (Cividis/Viridis).
- **Tripartite Anomaly Triage Protocol:** Distinguishes Type A clerical defects (unit errors, transcription
  typos), Type B authentic agro-ecological/policy shocks (unseasonal hailstorms, export bans), and Type C
  market microstructure illiquidity. Deploys rolling Hampel filters (k=7, 3-sigma MAD) and seasonal-adjusted
  IQR (SA-IQR) on STL remainders. Mandates a **Dual-Track Modeling Architecture** where authentic shocks are
  never deleted.
- **Feature Correlation & Causality Guardrails:** Identifies and corrects common trend inflation (deflating
  nominal price-cost correlations from +0.74 to +0.31), non-linear threshold dependencies (using Spearman rank
  and Distance Correlation *dCor*), distributed asymmetric biological lag structures (via Cross-Correlation
  Functions), and multicollinearity (reducing weather feature VIF from 14.8 to 1.05 via PCA).
- **Master Downstream Report Blueprint:** Detailed section-by-section specification of all nine chapters of the
  final downstream EDA report, establishing required exhibits, analytical narratives, and commercial triggers.
- **Operational Decision Frameworks:** Transforms exploratory patterns into concrete procurement schedules,
  financial hedging/basis risk limits, public buffer stock release alerts, and agri-logistics warehouse
  allocation models across four organizational personas.

---

## Empirical panel benchmarks (72 Months: 2021–2026)

Computed directly by the analytical engine across 3,456 observations:

| Commodity | Market Category | Mean Price (INR/qtl) | Price CV (%) | Skewness | Kurtosis | Seasonal Amplitude (%) | Peak / Trough Month | Spatial CV (%) |
|---|---|---|---|---|---|---|---|---|
| **Wheat** | Rabi Cereal (Buffer Stocked) | ₹2,665.8 | 11.1% | +0.34 | -0.44 | 19.5% | M12 / M3 | 4.0% |
| **Paddy** | Kharif Cereal (Procurement Floor) | ₹2,531.1 | 10.4% | +0.44 | -0.28 | 15.7% | M7 / M10 | 4.8% |
| **Maize** | Feed & Industrial Starch | ₹2,367.5 | 14.3% | +0.39 | -0.47 | 25.1% | M5 / M10 | 4.9% |
| **Soybean** | Oilseed (Import Parity Linked) | ₹5,527.2 | 18.0% | +0.44 | -0.32 | 31.9% | M6 / M11 | 4.8% |
| **Cotton** | Commercial Fiber (Global Lint) | ₹8,024.4 | 18.7% | +0.38 | -0.45 | 34.0% | M7 / M1 | 4.7% |
| **Onion** | High-Value Perishable Horticulture | ₹2,323.5 | 44.0% | +1.84 | +3.42 | 48.6% | M10 / M4 | 6.8% |

---

## Folder structure

```
Agribusiness_EDA_Report_Design_Week3.docx            Official Word document deliverable
Agribusiness_EDA_Report_Design_Week3_preview.pdf     Rendered PDF preview
_build/
  eda_engine.py          Seeded multi-crop analytical engine (computes facts, STL, CV, VIF)
  facts.py               Loads data/eda_facts.json and formats figures
  diagram_generator.py   Pillow rendering script for 3 architectural diagrams
  docbase.py             Word styling, typography, table helpers, callouts, and footers
  cover.py               Cover page and Word dynamic Table of Contents field
  sec_a.py               Sections 1–3: Executive Summary, Data Architecture, EDA Methodology
  sec_b.py               Sections 4–5: Visualization Architecture, Statistical Anomaly Protocols
  sec_c.py               Sections 6–7: Feature Correlation Guardrails, Structural Blueprint
  sec_d.py               Sections 8–9: Actionable Decisions, Limitations & Model Governance
  sec_e.py               Appendices A–E: Master Dictionary (42 vars), Visual Standards,
                         Math Catalog, Anomaly Playbook, Brief Compliance Matrix
  build_week3.py         Document assembler
  export_pdf.ps1         PowerShell Word COM export and field refresh script
  scrub_metadata.py      DOCX and PDF anonymization script
  data/
    eda_facts.json       Exported empirical panel facts and benchmarks
  figures/
    eda_workflow.png            The End-to-End Agribusiness EDA Transformation Pipeline
    visual_selection_tree.png   Agribusiness Visual Encoding Decision Tree
    anomaly_triage_flow.png     Outlier & Anomaly Triage Protocol Architecture
```

---

## Rebuilding

```powershell
cd week3\_build
python eda_engine.py
python diagram_generator.py
python build_week3.py
powershell -ExecutionPolicy Bypass -File .\export_pdf.ps1
python scrub_metadata.py all
```

Requires Python 3.10+ with `python-docx`, `pandas`, `numpy`, and `Pillow`, plus Microsoft Word for
the automated PDF export.

---

## Lineage and links

- **Extends:** [Week 1 Analysis Plan](../week1/Agribusiness_Data_Analysis_Plan_Week1.docx) (Section 4 Indicator Framework) and [Week 2 Data Cleaning Strategy](../week2/Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2.docx) (Cleaning Rules R01–R18 and Audit Log Schema).
- **Feeds:** Week 4 Predictive Modelling Framework (model ladder, ARIMA/STL baselines, LightGBM feature engineering, and evaluation splits).
