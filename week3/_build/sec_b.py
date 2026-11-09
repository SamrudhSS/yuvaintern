# -*- coding: utf-8 -*-
"""Sections 4-5: Data Visualization Architecture and Statistical Anomaly Protocols."""

from pathlib import Path
from docbase import (h1, h2, h3, para, bullet, table, callout, figure,
                     spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
from facts import (FACTS, CROPS, STATES, CROP_STATS, ANOMALIES,
                   fmt_num, fmt_pct)

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"


def section_4(doc):
    h1(doc, "4.  Data Visualization Architecture & Graphic Taxonomy", page_break=True)

    para(doc,
         "Data visualization in agribusiness intelligence is not an aesthetic afterthought; it is an active cognitive "
         "tool for pattern discovery, hypothesis testing, and executive decision alignment. In complex panel datasets "
         "spanning multiple commodities, geographies, and phenological seasons, poorly chosen visual encodings produce "
         "severe cognitive errors: multi-line 'spaghetti charts' obscure regional divergence, unadjusted dual-axis plots "
         "create spurious causal illusions, and continuous rainbow color scales distort discrete agro-climatic boundaries.")

    para(doc,
         "The visualization architecture of this EDA blueprint enforces a strict mapping between the analytical "
         "question being interrogated, the underlying dataset dimensionality, the perceptual visual technique employed, "
         "and the target decision outcome. Every graphic must earn its place by accelerating actionable insight.")

    h2(doc, "4.1  The Agribusiness Visual Selection Framework")
    para(doc,
         "Figure 2 illustrates the visual selection decision tree adopted across the EDA report. The selection logic "
         "routes analytical inquiries into four primary branches: (1) Temporal & Cyclical Dynamics, (2) Spatial & Market "
         "Integration, (3) Distributional Profiling & Tail Risk, and (4) Multivariate Drivers & Lead-Lag Transmission.")

    # Visualization Tree Figure
    fig_path = str(FIG_DIR / "visual_selection_tree.png")
    figure(doc, fig_path, width_cm=CONTENT_W,
           caption_text="The Agribusiness Data Visualization Decision Tree: matching analytical questions to cognitive encodings.")

    h2(doc, "4.2  Comprehensive Graphic Mapping Matrix")
    para(doc,
         "Table 4 provides the exhaustive specification for each visualization class included in the EDA report. "
         "For each graphic type, the matrix articulates the target analytical question, the required data inputs, "
         "the specific visual encodings, the perceptual rationale, and the resulting business decision.")

    viz_matrix_rows = [
        ["Small-Multiples Faceted Lines",
         "How do wholesale price trajectories diverge across the 8 producing states over the 72-month horizon?",
         "Monthly modal price by Crop and State (6x8 grid).",
         "X: Time (Date); Y: Price (INR/qtl); Facets: State rows, Crop columns; Reference: National MSP horizontal dashed line.",
         "Eliminates line crossings ('spaghetti effect'); allows instant parallel visual scanning of regional divergence.",
         "Identifies regional price decoupling and pinpoint discount procurement zones."],

        ["Seasonal Subseries / Cycle Plots",
         "Is calendar harvest seasonality stable, or is climate change shifting the timing and depth of post-harvest gluts?",
         "Monthly STL Seasonal Component (S_t) across 72 months.",
         "X: Calendar Month (Jan-Dec); Y: Seasonal Index (% deviation from trend); Lines: Individual historical years (2021-2026).",
         "Separates month-of-year biological cycle from multi-year macro trend; exposes seasonal amplitude drift across years.",
         "Adjusts corporate inventory procurement schedules to reflect shifting harvest arrival peaks."],

        ["Phase-Space Cobweb Trajectories",
         "Does the commodity exhibit classic cobweb market cycles (lagged supply response driving boom-bust cycles)?",
         "Log Monthly Modal Price vs Log Monthly Mandi Arrivals.",
         "X: Log Arrivals; Y: Log Modal Price; Points connected chronologically by directed arrows; Color: Year.",
         "Exposes counter-clockwise cyclical attractor loops, revealing supply-demand elasticity and market overshooting.",
         "Signals the transition from commodity oversupply troughs to imminent structural shortages."],

        ["Geospatial Binned Choropleths",
         "Where are the spatial yield gaps and production deficit clusters located across key agro-climatic zones?",
         "District/State Crop Yield (kg/ha) and Production Deficit vs 5-year average.",
         "Polygons: State/District boundaries; Fill: Binned divergent color palette (Brown = Deficit, Green = Surplus); Overlay: Major Mandi centroid bubbles.",
         "Prevents pseudo-continuous gradient misinterpretations; highlights spatial clustering of agricultural stress.",
         "Directs spatial logistics routing, inter-state grain transit, and regional buffer stock deployments."],

        ["Violin Plots + Jittered Strips",
         "How do price dispersion and tail-risk volatility differ between perishables and buffer-stocked cereals?",
         "Daily / Monthly Modal Price distributions across 6 crops.",
         "X: Commodity Category; Y: Normalized Price (Z-score); Geometry: Mirrored density violin with internal box-plot and jittered outlier points.",
         "Reveals multi-modality, skewness, and heavy-tailed extreme shock frequencies that standard box plots conceal.",
         "Calibrates commodity hedging ratios, options strike bands, and Value-at-Risk limits."],

        ["Lead-Lag Cross-Correlation Heatmap",
         "What is the precise transmission delay between monsoon rainfall deficits, arrival crashes, and wholesale price spikes?",
         "Cross-Correlation Function (CCF) coefficients at lags tau = -6 to +6 months.",
         "X: Lag in Months; Y: Commodity Pair (Rainfall -> Price, Arrivals -> Price); Fill: Divergent color scale (-1.0 to +1.0).",
         "Directly communicates temporal transmission dynamics and identifies the optimal predictive lead time for each driver.",
         "Establishes leading indicator trigger alarms 60 to 90 days before consumer market price escalation."],

        ["Binned Scatter + LOESS Spline",
         "What are the critical temperature and moisture tipping points that trigger non-linear crop yield collapse?",
         "Historical District Yield (kg/ha) vs Heat Degree Days (HDD) and SPEI Drought Index.",
         "X: Weather Stress Index; Y: Realized Yield; Points: Binned district averages; Line: Robust LOESS non-parametric curve with 95% confidence ribbon.",
         "Exposes non-linear agronomic thresholds (tipping points) where marginal weather deterioration causes catastrophic yield drops.",
         "Calibrates weather-indexed parametric crop insurance triggers and climate vulnerability scores."]
    ]
    table(doc,
          ["Visualization Technique", "Analytical Question Interrogated", "Required Data Inputs", "Visual Encodings & Aesthetics", "Perceptual Rationale", "Commercial Decision Action"],
          viz_matrix_rows,
          [2.6, 2.8, 2.2, 3.2, 3.0, 2.8],
          caption_text="Comprehensive Agribusiness Data Visualization Specification Matrix.",
          first_col_bold=True)

    h2(doc, "4.3  Cognitive Design Standards & Accessibility Rules")
    para(doc,
         "To guarantee that the visualizations communicate unambiguous truths to executive decision-makers, the EDA "
         "architecture mandates four strict graphical standards:",
         space_after=4)

    bullet(doc, "Dual-axis charts with disparate numerical scales (e.g., plotting price in INR on the left axis and "
                "arrivals in quintals on the right axis) are strictly prohibited. Such charts are notoriously prone to "
                "visual manipulation, where scaling choices artificially exaggerate or minimize correlation. Instead, the "
                "EDA report uses vertically stacked, aligned two-panel subplots sharing a synchronized time axis.",
           lead="Prohibition of Misleading Dual Y-Axes: ")

    bullet(doc, "Standard rainbow (Jet) and red-green color scales are banned across all agro-climatic "
                "and yield choropleths. In addition to being inaccessible to color-blind stakeholders, red-green gradients "
                "introduce artificial perceptual boundaries. All continuous environmental scales use perceptually uniform, "
                "color-blind-safe palettes (Viridis, Cividis, and Muted Earth Tones).",
           lead="Perceptually Uniform Color Palettes: ")

    bullet(doc, "Visualizations must maximize the 'data-ink ratio' by eliminating decorative 3D effects, "
                "heavy background grids, and redundant legend entries. Gridlines are rendered in faint neutral gray (#E0E0E0) "
                "with 0.5pt stroke, and category labels are directly annotated on the data lines where feasible.",
           lead="Maximizing Data-Ink and Minimizing Chart Junk: ")


def section_5(doc):
    h1(doc, "5.  Statistical Anomaly Triage & Outlier Resolution Protocols", page_break=True)

    para(doc,
         "A defining vulnerability in agribusiness data science is the uncritical application of generic outlier "
         "detection rules. In standard statistical packages, any observation exceeding three standard deviations "
         "(|z| > 3.0) or 1.5 times the Interquartile Range (IQR) is labeled an 'outlier' and frequently deleted or "
         "windsorized. In agricultural markets, blindly deleting extreme observations is disastrous: an unseasonal "
         "hailstorm that destroys 40% of the standing onion crop or an overnight government export ban will produce "
         "dramatic statistical anomalies that represent vital market truths, not data errors.")

    para(doc,
         "Conversely, failing to detect authentic data entry defects (e.g., a data entry operator entering prices in "
         "INR/kg instead of INR/quintal, creating an artificial 100x error) corrupts downstream econometric models. "
         "The EDA report establishes a rigorous Tripartite Anomaly Protocol that separates data defects from authentic "
         "market shocks and microstructure illiquidity.")

    h2(doc, "5.1  The Tripartite Taxonomy of Agribusiness Outliers")
    para(doc,
         "Every statistical anomaly flagged in the agribusiness panel is categorized into one of three structural types:",
         space_after=4)

    bullet(doc, "Measurement, transcription, and processing errors. Examples include unit "
                "confusion (reporting INR 25/kg as INR 25/quintal instead of INR 2,500/quintal), misplaced decimal points, "
                "accidental keypunch repetition (entering 22555 instead of 2255), and duplicate records generated during "
                "batch portal synchronization.",
           lead="Type A: Clerical & Technical Measurement Defects. ")

    bullet(doc, "Authentic, severe real-world disruptions caused by agro-ecological "
                "disasters or government policy interventions. Examples include unseasonal monsoon downpours during rabi harvest, "
                "catastrophic El Nino droughts, sudden announcements of Minimum Export Prices (MEP), export bans, or "
                "nationwide pandemic logistics lockdowns.",
           lead="Type B: Authentic Agro-Ecological & Policy Shocks. ")

    bullet(doc, "Artifacts of thin trading volume or localized trading friction. "
                "Examples include a single distressed farmer lot sold at steep discount at the close of trading, off-season "
                "residual lots (< 5 quintals) that do not reflect commercial clearing prices, or temporary mandi closures "
                "due to trader strikes.",
           lead="Type C: Microstructure Illiquidity & Censoring Artifacts. ")

    # Anomaly Triage Figure
    fig_path = str(FIG_DIR / "anomaly_triage_flow.png")
    figure(doc, fig_path, width_cm=CONTENT_W,
           caption_text="The Agribusiness Anomaly Triage and Outlier Resolution Architecture: detection, classification, and dual-track resolution.")

    h2(doc, "5.2  Multi-Stage Detection Protocols")
    para(doc,
         "To identify anomalies without introducing seasonal bias, the EDA engine implements a multi-stage detection pipeline:",
         space_after=4)

    bullet(doc, "For high-frequency time-series price data, traditional moving-mean "
                "filters fail because extreme outliers distort the rolling mean and standard deviation. The EDA engine deploys "
                "a rolling Hampel filter with a 7-period window (k=7). The filter calculates the rolling median M_t and the "
                "Median Absolute Deviation (MAD_t). A data point P_t is flagged if:\n"
                "    |P_t - M_t| > 3.0 * 1.4826 * MAD_t\n"
                "The 1.4826 scaling factor ensures asymptotic consistency with the standard deviation of a normal distribution.",
           lead="1. Rolling Hampel Filter (Moving Median & MAD): ")

    bullet(doc, "Applying standard IQR thresholds to raw agricultural prices flags "
                "every predictable lean-season price peak as an outlier. To prevent this error, the EDA applies IQR thresholds "
                "exclusively to the Remainder Component (R_t) extracted from the robust STL decomposition. The seasonal-adjusted "
                "bounds are defined as:\n"
                "    Lower Bound = Q1(R_t) - 1.5 * IQR(R_t)\n"
                "    Upper Bound = Q3(R_t) + 1.5 * IQR(R_t)\n"
                "This isolates genuine irregular shocks from predictable harvest-cycle seasonality.",
           lead="2. Seasonality-Adjusted IQR on STL Remainder: ")

    bullet(doc, "To detect multidimensional inconsistencies that appear normal "
                "in univariate projections (e.g., a district reporting record-breaking wheat yields during a severe -45% monsoon "
                "drought), the EDA implements an Isolation Forest ensemble trained on joint bivariate distributions (Rainfall Departure "
                "vs Yield, and Mandi Arrivals vs Price Spreads).",
           lead="3. Bivariate Isolation Forest & Mahalanobis Distance: ")

    h2(doc, "5.3  The Dual-Track Handling & Resolution Strategy")
    para(doc,
         "Once categorized, anomalies are processed according to the Golden Rule of Agribusiness EDA: Never discard authentic "
         "agricultural market shocks. Doing so artificially compresses tail risk and guarantees catastrophic failure when "
         "downstream forecasting models encounter real-world volatility.")

    para(doc,
         "The EDA report establishes a Dual-Track Modeling Architecture:",
         space_after=4)

    bullet(doc, "Retains 100% of authentic Type B shocks, augmented by binary Shock Indicator "
                "dummy variables and interaction terms. This track is used for tail-risk analysis, Value-at-Risk (VaR) estimation, "
                "and extreme weather scenario stress-testing.",
           lead="Track 1: Full-Sample Extreme Risk Track. ")

    bullet(doc, "Type A clerical defects are repaired via deterministic unit-rescaling "
                "(if factor ~100) or imputed via seasonal Kalman smoothing. Type C illiquidity artifacts are volume-weighted "
                "or softly windsorized at the 1st and 99th percentiles. This track provides a stable baseline for underlying "
                "trend-cycle estimation.",
           lead="Track 2: Robust Baseline Econometric Track. ")

    callout(doc, "AUDIT TRAIL COMPLIANCE MANDATE",
            "Every single anomaly identified, classified, and repaired must be logged in the Central Data Cleaning "
            "Audit Trail (cleaning_log.csv established in Week 2), recording the observation timestamp, crop, state, "
            "original value, detection rule ID, anomaly type (A/B/C), and exact mathematical remediation applied. No silent "
            "modifications are permitted.",
            fill=PALE, accent=ACCENT)

