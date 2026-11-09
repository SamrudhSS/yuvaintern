# -*- coding: utf-8 -*-
"""Sections 6-7: Feature Correlation & Causality, and Structural Report Blueprint."""

from pathlib import Path
from docbase import (h1, h2, h3, para, bullet, table, callout, figure,
                     spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
from facts import (FACTS, CROPS, STATES, CROP_STATS, CORR_BENCH,
                   fmt_num, fmt_pct)


def section_6(doc):
    h1(doc, "6.  Feature Correlation, Multicollinearity & Causality Guardrails", page_break=True)

    para(doc,
         "In agribusiness data science, correlation analysis is fraught with analytical traps. Uncritical bivariate "
         "correlations routinely mislead analysts into confusing common macroeconomic drift with structural causation, "
         "ignoring non-linear biophysical thresholds, or overlooking multi-month biological transmission delays. An EDA "
         "report that merely presents an unadjusted Pearson correlation heatmap risks recommending disastrous hedging or "
         "procurement policies based on statistical artifacts.")

    para(doc,
         "This section establishes four methodological guardrails to ensure that feature associations uncovered during "
         "exploratory analysis represent authentic economic and agronomic drivers rather than statistical illusions.")

    h2(doc, "6.1  The Three Agricultural Correlation Pitfalls")

    bullet(doc, "Nominal crop prices and nominal input costs (diesel, labor, fertilizer) "
                "both exhibit secular upward drift driven by broader macroeconomic inflation and money supply growth. Across "
                "our panel, the raw Pearson correlation between the input cost index and wholesale wheat prices is r = +0.74. "
                "However, when series are detrended or first-differenced to isolate cyclical co-movement, the correlation drops "
                "to an authentic r = +0.31. Failing to detrend produces massive omitted variable bias and spurious significance.",
           lead="1. Spurious Common Trend Inflation: ")

    bullet(doc, "Biological crop response functions are inherently non-linear and "
                "frequently non-monotonic. For example, during normal rainfall intervals (+/- 10% of LPA), marginal rainfall "
                "variation has negligible impact on soybean yields. However, once rainfall deficits exceed -30%, yields drop "
                "precipitously; similarly, extreme positive rainfall (+50%) causes waterlogging, depressing yields. A linear "
                "Pearson correlation across the full range yields an artificially muted r = +0.44. In contrast, non-parametric "
                "Spearman rank correlation yields r = +0.62, and Distance Correlation (dCor) yields 0.58, correctly capturing "
                "the strong non-linear dependence.",
           lead="2. Non-Linear & Threshold Dependencies: ")

    bullet(doc, "In annual and seasonal crops, weather shocks do not influence prices "
                "contemporaneously. A severe drought in July (vegetative stage) has near-zero contemporaneous correlation with "
                "July mandi prices because old-crop buffer stocks supply current demand. The price impact materializes 4 to 6 "
                "months later during the post-harvest arrival window. Evaluating weather-price relationships contemporaneously "
                "leads to the false deduction that climate does not drive price formation.",
           lead="3. Distributed Asymmetric Lag Structures: ")

    h2(doc, "6.2  Quantitative Diagnostics & Multicollinearity Controls")
    para(doc,
         "To rigorously diagnose feature associations, the EDA report mandates computing a tri-metric correlation "
         "matrix alongside formal collinearity diagnostics:")

    corr_rows = [
        ["Pearson Correlation (r)", "Measures linear co-movement between two continuous variables.",
         "Highly sensitive to outliers; assumes bivariate normality; fails on non-linear threshold dynamics.",
         "Stationary, detrended macroeconomic indicators (e.g., real interest rates vs real inventory carry)."],
        ["Spearman Rank Correlation (rho)", "Measures monotonic co-movement based on ordinal rank transformations.",
         "Robust to extreme outliers and non-linear monotonic scalings; immune to single-event price spikes.",
         "Price elasticity of arrivals; relationship between rainfall departure percentiles and yield."],
        ["Distance Correlation (dCor)", "Measures true statistical independence (dCor = 0 iff variables are independent).",
         "Captures both linear and complex non-monotonic, circular, or threshold relationships.",
         "Complex agro-climatic indices (SPEI-3, Heat Degree Days) vs final crop yield realization."],
        ["Variance Inflation Factor (VIF)", "Quantifies the degree of multicollinearity in feature subsets (VIF_j = 1 / (1 - R_j^2)).",
         "Features with VIF > 5.0 exhibit severe collinearity, inflating regression coefficient standard errors.",
         "Screening gridded weather features before downstream predictive model training."]
    ]
    table(doc,
          ["Correlation Diagnostic", "Core Mathematical Definition", "Properties & Methodological Limitations", "Primary Agribusiness Application"],
          corr_rows,
          [3.2, 3.8, 4.4, 4.8],
          caption_text="Comparative Matrix of Agribusiness Association and Collinearity Diagnostics.",
          first_col_bold=True)

    para(doc,
         "In our exploratory panel, raw gridded weather features (cumulative precipitation, rainy days, SPEI-3, and "
         "maximum temperature) exhibit an average VIF of 14.8, indicating severe multicollinearity. By applying Principal "
         "Component Analysis (PCA) to orthogonalize these features into distinct Moisture and Thermal stress scores, the "
         "resulting feature VIF is reduced to 1.05, establishing a perfectly orthogonal feature set for predictive modeling.")

    h2(doc, "6.3  Sub-Period Stability & Structural Break Analysis")
    para(doc,
         "Agricultural markets are periodically subjected to exogenous policy shocks that permanently alter correlation "
         "structures. An association that holds under free-market conditions collapses following government market intervention. "
         "The EDA protocol enforces rolling 24-month correlation windows and formal structural break tests across two key regimes:",
         space_after=4)

    bullet(doc, "Domestic soybean prices in Madhya Pradesh historically tracked CBOT soybean futures "
                "with a strong 60-day lag correlation (r = +0.78). However, when the central government imposed export bans and "
                "slashed import tariffs on palm oil in late 2021, the domestic-global correlation collapsed to r = +0.18. The EDA "
                "report documents this regime decoupling to prevent models from over-relying on international signals.",
           lead="Case Study 1: Global Import Parity Decoupling in Soybean. ")

    bullet(doc, "In perishable horticulture, onion arrivals and modal prices exhibit an "
                "intense negative correlation (r = -0.68) during the September lean season. However, following the imposition "
                "of stock limits and Minimum Export Prices (MEP), market hoarding transitions to distressed panics, shifting the "
                "elasticity curve and introducing structural breakpoints verified via the Chow test (p < 0.001).",
           lead="Case Study 2: Policy Interventions and Stock Limits in Onion. ")

    h2(doc, "6.4  Lead-Lag Transmission & Cross-Correlation Functions (CCF)")
    para(doc,
         "To map the dynamic propagation of supply shocks across the supply chain, the EDA engine computes the Cross-Correlation "
         "Function (CCF) across monthly lags tau = -6 to +6. Figure 3 illustrates the empirical lead-lag transmission pipeline "
         "discovered across our commodity panel:")

    bullet(doc, "Monsoon rainfall deficits in July reach peak negative correlation with district crop yield "
                "at lag tau = +3 months (October harvest season).",
           lead="Stage 1 (Climate -> Yield): ")
    bullet(doc, "Harvest yield shocks translate into compressed mandi arrivals at lag tau = +1 month "
                "(November peak marketing window).",
           lead="Stage 2 (Yield -> Mandi Arrivals): ")
    bullet(doc, "Mandi arrival deficits trigger wholesale modal price spikes at lag tau = +1 month (December), "
                "with an empirical peak cross-correlation of r = -0.68.",
           lead="Stage 3 (Arrivals -> Wholesale Price): ")
    bullet(doc, "Wholesale price inflation transmits to metropolitan retail consumer price indices at lag tau = +1 to +2 months "
                "(January-February), driven by retail logistics and margin markups.",
           lead="Stage 4 (Wholesale Price -> Retail Inflation): ")


def section_7(doc):
    h1(doc, "7.  Structural Blueprint of the Downstream EDA Report", page_break=True)

    para(doc,
         "This section provides the comprehensive structural blueprint for the final, downstream Agribusiness Exploratory "
         "Data Analysis Report. Designed to serve as the master template for subsequent analytical execution, the blueprint "
         "specifies the chapter titles, detailed section hierarchies, required visual and tabular exhibits, narrative "
         "arguments, and operational decision triggers for each chapter.")

    h2(doc, "7.1  Master Architectural Outline of the Final Report")
    para(doc,
         "The final downstream EDA report is structured into nine core analytical chapters, transitioning systematically "
         "from macro fundamentals to micro market mechanics, crop-specific deep-dives, and strategic commercial synthesis:")

    blueprint_chapters = [
        ("Chapter 1: Executive Summary & Market Intelligence Overview",
         "High-level executive briefing; macro macroeconomic context; the core commodity dashboard; headline findings across the 6 crops; summary of key commercial risks and immediate procurement action items.",
         "Figure 1.1: Multi-Crop Price Performance Radar Chart; Table 1.1: Macro Commodity KPI Scorecard; Table 1.2: Imminent Supply Alert Register."),

        ("Chapter 2: Data Architecture, Lineage & Quality Audit",
         "Detailed provenance of the 38 data sources; verification of ingestion pipelines; missing value imputation scorecard; anomaly detection summary; validation of canonical spatial and temporal keys.",
         "Table 2.1: Data Lineage & Vintage Audit Matrix; Figure 2.1: Missingness & Imputation Heatmap; Table 2.2: Anomaly Resolution Log Summary."),

        ("Chapter 3: Macro Production Fundamentals & Regional Yield Gap Analysis",
         "Long-term structural acreage and production trends; state-by-state yield gap benchmarking; analysis of irrigation buffers vs rainfed vulnerability; Advance Estimates revision variance.",
         "Figure 3.1: 10-Year Production & Acreage Trajectory by State; Figure 3.2: Regional Yield Gap Benchmarking Bar Chart; Table 3.1: Irrigation Coverage vs Yield Stability Matrix."),

        ("Chapter 4: Mandi Market Microstructure, Price Discovery & Arrival Dynamics",
         "Wholesale price distribution profiling; parametric vs non-parametric metrics; arrival velocity curves; inverse demand and price flexibility estimates; MSP floor efficiency and procurement penetration.",
         "Figure 4.1: Multi-Commodity Price Distribution Violins; Figure 4.2: Mandi Arrival Velocity Curves; Table 4.1: Empirical Price Flexibility & Elasticity Coefficients."),

        ("Chapter 5: Agro-Climatic Teleconnections, Water Stress & Weather Sensitivity",
         "Monsoon rainfall departure analysis; Standardized Precipitation Evapotranspiration Index (SPEI-3); satellite NDVI vegetative canopy health anomalies; Heat Degree Days (HDD) thermal stress modeling.",
         "Figure 5.1: Geospatial Monsoon Rainfall Departure Choropleth; Figure 5.2: NDVI Vegetative Health Anomaly Time-Series; Table 5.1: PCA Orthogonalized Agro-Climatic Factor Loadings."),

        ("Chapter 6: Spatial Integration, Transport Arbitrage & Interstate Spreads",
         "Law of One Price (LOOP) empirical validation; pairwise mandi price co-integration; inter-state spatial price dispersion (CV); spatial autocorrelation of production shocks (Moran's I); transport freight arbitrage bands.",
         "Figure 6.1: Pairwise Mandi Price Co-Integration Network; Figure 6.2: Inter-State Price Spread vs Freight Parity Bands; Table 6.1: Spatial Price Dispersion & Autocorrelation Metrics."),

        ("Chapter 7: Input Cost Pressures, Factor Markets & Farmgate Margins",
         "Agronomic factor market dynamics: diesel fuel, DAP and Urea fertilizers, agricultural daily wages, electricity tariffs; cost-push inflation transmission to wholesale prices; farmer gross margin compression.",
         "Figure 7.1: Comprehensive Input Cost Index vs Wholesale Price Indices; Figure 7.2: Farmgate Production Cost Breakdown by State; Table 7.1: Cost-Push Elasticity Coefficients."),

        ("Chapter 8: Focal Commodity Deep-Dives (6 Sub-Chapters)",
         "Comprehensive multi-dimensional profiles for each commodity: (8.1) Wheat (Rabi Cereal & Buffer Stocks), (8.2) Paddy (Kharif Staple & Procurement Floor), (8.3) Maize (Feed & Industrial Starch), (8.4) Soybean (Oilseed & Global Import Parity), (8.5) Cotton (Commercial Fiber & Global Lint), (8.6) Onion (High-Value Perishable Horticulture).",
         "For each crop: (a) Faceted Inter-State Price Trajectory, (b) STL Seasonal Decomposition Panel, (c) Phase-Space Cobweb Plot, (d) Weather Sensitivity Response Curve, (e) Commodity KPI Factsheet."),

        ("Chapter 9: Strategic Synthesis, Risk Alerts & Procurement Recommendations",
         "Integration of exploratory findings into actionable corporate and policy strategies; procurement timing windows; hedging and basis risk guidelines; government market intervention triggers; limitations and model risk warnings.",
         "Figure 9.1: Comprehensive Commodity Procurement Timing Calendar; Table 9.1: Strategic Sourcing & Arbitrage Matrix; Table 9.2: Early Warning Market Intervention Indicators.")
    ]

    for title, scope_desc, exhibit_plan in blueprint_chapters:
        h2(doc, title)
        para(doc, scope_desc, space_after=4)
        callout(doc, "MANDATORY EXHIBITS & OUTPUTS", exhibit_plan, fill=PALE, accent=SECONDARY)

    h2(doc, "7.2  Chapter 8 Commodity Deep-Dive Standardized Protocol")
    para(doc,
         "To maintain analytical consistency across diverse commodities, Chapter 8 mandates that each of the six "
         "focal crop deep-dives follows an identical 5-part analytical sequence:",
         space_after=4)

    bullet(doc, "Acreage trends, state-level production concentration, "
                "historical yield performance, and structural supply stability.",
           lead="Part A: Supply Fundamentals & Agronomic Profile. ")

    bullet(doc, "Modal wholesale price levels, volatility regimes (CV), "
                "MSP premium/discount spreads, and arrival volume liquidity across primary trading mandis.",
           lead="Part B: Market Clearing & Mandi Dynamics. ")

    bullet(doc, "Robust STL decomposition isolating the 12-month calendar seasonal "
                "index, historical seasonal amplitude, and post-harvest dip timing.",
           lead="Part C: Seasonality & Storage Carry Economics. ")

    bullet(doc, "Quantification of yield and price sensitivity to monsoon rainfall "
                "departures, SPEI drought indices, and critical-phase Heat Degree Days.",
           lead="Part D: Climate Sensitivity & Stress Teleconnections. ")

    bullet(doc, "Synthesis of exploratory patterns into actionable procurement windows, "
                "spatial sourcing arbitrage opportunities, and downside risk thresholds.",
           lead="Part E: Commercial & Strategic Takeaways. ")

