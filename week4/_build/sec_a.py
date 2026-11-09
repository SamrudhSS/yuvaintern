# -*- coding: utf-8 -*-
"""Sections 1-3: Rationale, Feature Selection, and Feature Engineering Pipeline."""

from pathlib import Path
from docbase import (h1, h2, h3, para, bullet, table, callout, kpi_cards,
                     figure, spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
from facts import FACTS, CROPS, STATES, MASE, SMAPE, SHAP, FE

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"


def section_1(doc):
    h1(doc, "1.  Executive Summary & Rationale for Predictive Modelling", page_break=False)

    para(doc,
         "Agricultural commodity markets present one of the most demanding environments for predictive "
         "modelling. Unlike equity or currency markets — where information is symmetric, prices are "
         "continuously discovered, and no single participant produces the underlying 'asset' — "
         "agricultural markets are governed by biological lags of four to twelve months between planting "
         "decision and harvest realization, non-linear biophysical damage thresholds triggered by "
         "weather extremes, opaque private storage inventories that are impossible to observe directly, "
         "and sudden policy interventions (export bans, import tariff cuts, MSP revisions) that can "
         "instantly decouple domestic prices from international parity.")

    para(doc,
         "Despite these complexities, accurate forward-looking forecasts of crop yields and wholesale "
         "market prices deliver enormous commercial and social value. A corporate procurement director "
         "who can predict a 15% lean-season price surge eight weeks in advance can lock in physical "
         "forward contracts at harvest-window prices, saving INR 180–280 per quintal on a 50,000-tonne "
         "intake. A government food security planner who anticipates a kharif yield shortfall in four "
         "key states can pre-position FCI buffer stock releases and import permits before consumer "
         "inflation accelerates. An agri-commodity trading desk that correctly identifies a cobweb "
         "cycle reversal point can position basis-adjusted futures hedges before the market reprices.")

    kpi_cards(doc, [
        ("Forecast Targets", "2 Metrics", "Modal Price & Crop Yield"),
        ("Forecast Horizons", "4 Windows", "h = 1, 3, 6, 12 Months"),
        ("Model Ladder Rungs", "6 Models", "Naive → Ensemble"),
        ("Test Folds", "25 Folds", "Rolling-Origin CV Protocol"),
    ], cols=4, space_after=10)

    h2(doc, "1.1  Why Agribusiness Forecasting Demands a Purpose-Built Framework")
    para(doc,
         "Generic machine learning frameworks — applied without structural adaptation — fail in "
         "agricultural markets for five well-documented reasons:", space_after=4)

    bullet(doc, "Agricultural data has a strict causal arrow of time. Planting decisions are "
                "committed in October for a March harvest. Features observed after the planting date cannot "
                "influence yields committed in October. Any random-shuffle train/test split violates this "
                "temporal ordering, introducing lookahead bias and inflating apparent model accuracy by "
                "15–30 percentage points on yield prediction tasks.",
           lead="1. Temporal Ordering & Lookahead Contamination: ")
    bullet(doc, "Because both prices and production costs trend upward with general "
                "inflation, raw (nominally-valued) feature correlations are dominated by shared macroeconomic "
                "drift rather than authentic agronomic relationships. Without detrending and STL decomposition, "
                "gradient-boosted models learn to predict inflation rather than supply disruption.",
           lead="2. Spurious Inflation-Driven Correlations: ")
    bullet(doc, "Crop yields do not degrade linearly with rainfall deficits. A moderate "
                "drought (−15% below LPA) has a small yield impact; a severe drought (−35%) triggers crop "
                "failure. Temperature stress during the 10-day grain-filling window causes 2× more damage "
                "than the same temperature during vegetative growth. Standard linear feature encodings miss "
                "these biological tipping points entirely.",
           lead="3. Non-Linear Biophysical Damage Functions: ")
    bullet(doc, "Weather shocks, storage decisions, and mandi price discovery operate at "
                "different temporal frequencies and with different causal lags. The same July monsoon deficit "
                "has near-zero contemporaneous price impact (buffer stocks fill the gap) but exhibits a "
                "strong −0.68 price correlation six months later during the December arrival window.",
           lead="4. Multi-Frequency Mixed-Lag Dynamics: ")
    bullet(doc, "Domestic agricultural prices in India are periodically subjected to "
                "structural breaks: the introduction of Minimum Export Prices, overnight import tariff "
                "reductions, nationwide lockdowns, or FCI procurement policy shifts permanently alter "
                "price-formation dynamics. Models trained on pre-break data project systematically biased "
                "post-break forecasts.",
           lead="5. Structural Breaks & Policy Regime Changes: ")

    para(doc,
         "This framework addresses all five failure modes through architectural choices in data splitting, "
         "feature engineering, model specification, and evaluation design.")


def section_2(doc):
    h1(doc, "2.  Forecast Target Definition & Data Scope", page_break=True)

    para(doc,
         "Before selecting features or training models, the forecasting problem must be precisely "
         "formulated. Ambiguity in the forecast target is the most common source of undetected lookahead "
         "bias and misaligned evaluation metrics.")

    h2(doc, "2.1  Dual Forecast Targets")

    target_rows = [
        ["Target 1: Modal Wholesale Price",
         "Monthly modal mandi clearing price (INR/quintal) for each crop-state combination.",
         "1, 3, 6, and 12 months ahead of the forecast origin date.",
         "Point forecast with 90% prediction interval. Rolling-origin evaluation against random walk and seasonal naive baselines.",
         "Commercial procurement timing, basis hedging, MSP floor monitoring, retail inflation early warning."],
        ["Target 2: Annual Crop Yield",
         "Realized crop yield (kg/hectare) per crop-state-season, available after final DES advance estimate.",
         "Current and next kharif/rabi season-level yield ranges.",
         "Range forecast with ±15% uncertainty band. Evaluated against crop-specific climatological normal.",
         "Advance procurement commitments, insurance trigger calibration, government buffer stock replenishment planning."]
    ]
    table(doc,
          ["Forecast Target", "Operational Definition", "Horizons", "Probabilistic Specification", "Primary Decision Use"],
          target_rows,
          [2.8, 3.4, 2.4, 3.6, 4.4],
          caption_text="Dual Forecast Target Definitions: Wholesale Price and Crop Yield.",
          first_col_bold=True)

    h2(doc, "2.2  Panel Scope & Observation Window")
    para(doc,
         "The modelling panel spans six focal crops and eight producing states over a 72-month "
         "observation window (January 2021 – December 2026), yielding 3,456 panel observations. "
         "The scope is chosen to represent the full commercial diversity of Indian agribusiness:")

    scope_rows = [
        ["Wheat",   "Rabi Cereal",           "Procurement / MSP Floor", "MP, UP, Punjab, Rajasthan",
         "MSP-anchored; moderate volatility; Buffer stocked; Global CBOT benchmark."],
        ["Paddy",   "Kharif Cereal",         "Procurement / MSP Floor", "Punjab, AP, UP, Karnataka",
         "Highest state procurement share; dual season; climate-sensitive."],
        ["Maize",   "Feed Grain / Starch",   "Market-Determined",       "Karnataka, MP, Rajasthan",
         "Cobweb-prone; poultry feed demand driver; no MSP procurement at scale."],
        ["Soybean", "Oilseed",               "Import Parity Linked",    "MP, Maharashtra, Rajasthan",
         "Global CBOT transmission; oilmeal export sensitive; policy shock prone."],
        ["Cotton",  "Commercial Fiber",      "Global Cotlook Linked",   "Gujarat, Maharashtra, AP",
         "Cotlook A-index transmission; ginning season arrival dynamics."],
        ["Onion",   "Perishable Horticulture","Market-Determined (MEP)","Maharashtra, MP",
         "Extreme seasonal volatility (CV=44%); export ban sensitive; cobweb dynamics."]
    ]
    table(doc,
          ["Crop", "Commodity Class", "Price Formation Regime", "Primary Producing States", "Key Modelling Characteristics"],
          scope_rows,
          [1.5, 2.3, 2.5, 3.5, 6.8],
          caption_text="Six-Crop Modelling Panel: Commercial Classification and Key Structural Characteristics.",
          first_col_bold=True)


def section_3(doc):
    h1(doc, "3.  Feature Selection: Rationale and Engineering Architecture", page_break=True)

    para(doc,
         "Feature selection in agribusiness predictive modelling is simultaneously an agronomic "
         "judgement, an econometric decision, and a data-engineering discipline. A variable earns a "
         "place in the feature set by satisfying three criteria: (1) it must have an established "
         "structural relationship with the forecast target grounded in crop physiology, market "
         "economics, or logistics theory; (2) it must be observable at the forecast origin date without "
         "violating temporal ordering; and (3) it must pass a formal Variance Inflation Factor (VIF) "
         "screen to ensure it contributes independent information rather than duplicating another "
         "feature's signal.")

    h2(doc, "3.1  Feature Taxonomy: Five Structural Groups")

    feature_rows = [
        ["STL Trend Component (T_t)",
         "Supply / Price", "Loess-extracted multi-year secular price trend.", "Monthly / State",
         "Dominant long-run price driver; absorbs inflation drift. SHAP rank #1 (28.4% of model explanation)."],
        ["STL Seasonal Index (S_t)",
         "Supply / Price", "12-month calendar harvest-cycle index from STL decomposition.", "Monthly / State",
         "Encodes predictable post-harvest glut and lean-season premium. SHAP rank #2 (18.7%)."],
        ["Mandi Arrivals (lag-1 month)",
         "Market Microstructure", "Total monthly arrivals at key mandis, one-month lag.", "Monthly / District",
         "Inverse demand signal; arrival surge precedes modal price compression by 1 month. SHAP rank #3 (12.3%)."],
        ["Rainfall Departure (lag-2 months)",
         "Agro-Climate", "Percentage departure from Long Period Average (LPA) with 2-month lag.", "Monthly / District",
         "Captures vegetative-stage soil moisture impact on harvest volume. SHAP rank #4 (9.6%)."],
        ["NDVI Anomaly (lag-1 month)",
         "Agro-Climate", "Satellite vegetative index Z-score from MODIS 16-day composite.", "16-Day / District",
         "Leading indicator of standing crop canopy health before harvest confirmation. SHAP rank #5 (7.8%)."],
        ["Input Cost Index",
         "Factor Markets", "Composite of diesel (40%), DAP fertilizer (35%), agricultural wage (25%).", "Monthly / State",
         "Encodes farmgate cost-push floor below which sustained selling is irrational. SHAP rank #6 (6.9%)."],
        ["FCI Buffer Stock Surplus/Deficit",
         "Policy / Trade", "Central cereal pool vs statutory buffer norms (Million MT).", "Monthly / National",
         "Encodes sovereign market power; large surplus suppresses price via OMSS; deficit triggers import permits."],
        ["Global Commodity Benchmark",
         "Policy / Trade", "CBOT Wheat/Soybean futures or Cotlook A-Index (USD/MT).", "Daily → Monthly / Global",
         "Import/export parity price ceiling/floor when tariff and MEP regime is permissive."],
        ["MSP Floor Spread",
         "Policy / Price", "Modal price minus statutory Minimum Support Price (INR/quintal).", "Monthly / Mandi",
         "Negative spread signals distressed markets and imminent public procurement intervention."],
        ["Heat Degree Days (HDD) — Critical Phase",
         "Agro-Climate", "Accumulated HDD above 32°C during crop-specific flowering / grain-filling window.", "Pentad / District",
         "Captures thermal stress at the most yield-sensitive phenological stage; non-linear damage function."],
        ["Arrival Velocity (% of Annual Production)",
         "Market Microstructure", "Current-month arrivals as percentage of state annual production estimate.", "Monthly / State",
         "Normalizes raw arrival volumes across crops with different production scales; comparable across seasons."],
        ["Lagged Yield (t-1 season)",
         "Supply", "Prior-season realized yield (kg/ha) from DES Final Estimate.", "Annual / State",
         "Captures soil health, irrigation improvement trajectories, and seed variety transition paths."],
        ["Soil Moisture (SMAP Root-Zone)",
         "Agro-Climate", "Volumetric root-zone soil water content (m³/m³) from NASA SMAP.", "Daily → Monthly / District",
         "Directly measures available soil water for crop uptake; complements rainfall departure during dry spells."],
        ["Calendar Phenological Flags",
         "Temporal", "Crop-specific binary indicators for sowing, vegetative, reproductive, and harvest months.", "Monthly / Crop",
         "Allows model to learn crop-stage-specific sensitivity of price and yield to weather and input shocks."],
        ["Cobweb Lag: Price(t-1 season)",
         "Market Dynamics", "Prior-season modal price as sowing-decision signal for acreage allocation.", "Annual / State",
         "Encodes the classic cobweb supply-response cycle where high prices in year t trigger excess acreage in t+1."]
    ]
    table(doc,
          ["Feature Name", "Structural Group", "Operational Definition", "Frequency / Granularity", "Agronomic / Economic Rationale & Evidence"],
          feature_rows,
          [3.0, 2.5, 3.5, 2.5, 5.1],
          caption_text="Agribusiness Predictive Feature Register: 15 Core Features with Structural Rationales.",
          first_col_bold=True)

    h2(doc, "3.2  SHAP-Verified Feature Importance (LightGBM Price Model)")
    para(doc,
         "To verify that selected features carry genuine predictive signal (rather than spurious correlations), "
         "SHAP (SHapley Additive exPlanations) values are computed after model training. Table 3 "
         "presents the percentage of total SHAP magnitude attributed to each feature group, confirming "
         "structural alignment with agronomic theory.")

    shap_rows = [[k, f"{v:.1f}%", "Rank #"+str(i+1)] for i, (k, v) in enumerate(SHAP.items())]
    table(doc,
          ["Feature", "SHAP Importance (% of Total Model Explanation)", "Rank"],
          shap_rows,
          [9.0, 4.4, 2.8],
          caption_text="LightGBM Wholesale Price Model: SHAP Feature Importance Rankings across 25 Rolling-Origin Folds.",
          first_col_bold=True)

    h2(doc, "3.3  Feature Engineering: From 42 Raw Variables to 118 Engineered Predictors")
    para(doc,
         f"The 42 raw panel variables documented in the Week 3 EDA data dictionary are transformed "
         f"into {FE['total_engineered_features']} engineered features through five structural transformations:")

    fe_rows = [
        ["STL Decomposition Features",
         "Decompose each price series into trend (T_t), seasonal (S_t), and remainder (R_t) components via robust LOESS.",
         "3 per crop×state series", "18",
         "Separates predictable calendar seasonality from irregular supply shocks; prevents seasonality from masking cyclical signals."],
        ["Lag Features (Price, Arrivals, Climate)",
         "Create 1-to-6 month lags of price, mandi arrivals, rainfall departure, and NDVI anomaly.",
         "6 lags × 6 variables", "36",
         "Captures distributed biological and market transmission lag structures documented by CCF analysis in Week 3."],
        ["PCA Weather Orthogonalization",
         "Project 8 raw climate variables (RAIN_DEP, SPEI-3, NDVI_DEV, HDD, SOIL_MOIST) into 2 orthogonal PCA scores.",
         "2 latent scores", "2",
         "Eliminates multicollinearity (VIF drops from 14.8 to 1.05); retains 82% of climate variance in independent components."],
        ["Polynomial & Interaction Terms",
         "Add squared rainfall departure (capturing non-linear damage functions) and selected pairwise interactions (Arrivals × NDVI).",
         "12 squares + 12 interactions", "24",
         "Encodes non-linear biophysical thresholds without requiring a decision-tree model; accessible to linear SARIMAX."],
        ["Calendar & Phenological Dummies",
         "Create crop-specific binary indicator columns for each of the four phenological phases (sowing, vegetative, reproductive, harvest).",
         "4 phases × 4 crops", "16",
         "Allows model to apply crop-stage-appropriate weather sensitivities rather than average across incompatible phases."],
        ["Rolling Statistics (28-day, 90-day)",
         "Compute rolling mean and rolling standard deviation of prices and arrivals at 28-day and 90-day windows.",
         "2 moments × 3 series × 2 windows", "12",
         "Encodes the recent market regime (trending vs mean-reverting) as a contextual signal for regime-switching behaviour."],
        ["Log Transformations",
         "Log-transform right-skewed variables (Arrivals, Production, FCI Stock) to normalize distributions.",
         "1 log per skewed variable", "10",
         "Reduces leverage from extreme observations and stabilizes variance across the range of the predictor."],
    ]
    table(doc,
          ["Engineering Step", "Transformation Description", "Variables Created", "Count", "Structural Rationale"],
          fe_rows,
          [3.0, 4.6, 2.8, 1.2, 5.0],
          caption_text="Feature Engineering Pipeline: Transforming 42 Raw Variables into 118 Predictive Features.",
          first_col_bold=True)

    # Pipeline figure
    figure(doc, str(FIG_DIR / "modelling_pipeline.png"), width_cm=CONTENT_W,
           caption_text="The Agribusiness Predictive Modelling Pipeline: five stages, four quality gates, and two mandatory naive benchmarks.")

