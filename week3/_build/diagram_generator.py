# -*- coding: utf-8 -*-
"""Draw publication-grade architectural diagrams for Week 3 EDA Design using Pillow."""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
FIG_DIR.mkdir(exist_ok=True)

# Corporate Agribusiness Palette
BG = "#FFFFFF"
WHITE = "#FFFFFF"
INK = "#1F2421"
MUTED = "#5C6B62"
PRIMARY = "#1B4332"     # Dark Forest Green
SECONDARY = "#2D6A4F"   # Deep Sage
ACCENT = "#B5651D"      # Warm Terracotta
PALE = "#EDF3EE"        # Soft Mint Gray
PALE2 = "#F7F9F6"       # Off-white tinted
RULE = "#C9D6CC"        # Border Rule
ALERT_BG = "#FDF2E9"    # Pale Ochre
ALERT_BORDER = "#D35400"

FONT_DIR = Path("C:/Windows/Fonts")
REG = str(FONT_DIR / "calibri.ttf")
BOLD = str(FONT_DIR / "calibrib.ttf")
ITAL = str(FONT_DIR / "calibrii.ttf")

def get_font(size, bold=False, italic=False):
    path = BOLD if bold else (ITAL if italic else REG)
    return ImageFont.truetype(path, size)

def draw_arrow(d, x1, y1, x2, y2, color=SECONDARY, width=5, arrow_size=16):
    d.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for sign in (1, -1):
        d.line([
            x2, y2,
            x2 - arrow_size * math.cos(ang - sign * 0.45),
            y2 - arrow_size * math.sin(ang - sign * 0.45)
        ], fill=color, width=width)

def draw_box(d, x, y, w, h, fill=PALE, outline=RULE, radius=12, width=2):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=width)

def draw_text(d, x, y, text, size=24, bold=False, color=INK, italic=False, anchor="la"):
    d.text((x, y), text, font=get_font(size, bold, italic), fill=color, anchor=anchor)

# -------------------------------------------------------------
# Diagram 1: Agribusiness EDA Transformation Pipeline
# -------------------------------------------------------------
def make_eda_workflow():
    W, H = 2200, 1250
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    draw_text(d, 50, 40, "END-TO-END AGRIBUSINESS EXPLORATORY DATA ANALYSIS FRAMEWORK", size=22, bold=True, color=ACCENT)
    draw_text(d, 50, 72, "From Heterogeneous Agricultural Signals to Actionable Commercial Insights", size=38, bold=True, color=PRIMARY)
    draw_text(d, 50, 125, "Systematic multi-stage pipeline: transforming messy raw agricultural indicators into validated analytical foundations and procurement decisions.", size=20, color=MUTED)

    stages = [
        ("STAGE 1: DATA INGESTION", "Heterogeneous Sources", [
            "- Mandi Prices & Arrivals (Agmarknet)",
            "- Gridded Weather & IMD Rainfall",
            "- Satellite Vegetation (NDVI / EVI)",
            "- Input Costs (Diesel, DAP, Urea, Labor)",
            "- Trade, Tariffs & Buffer Stocks (FCI)"
        ], 50),
        ("STAGE 2: QUALITY AUDIT", "Defect Triaging & Prep", [
            "- ISO Standardization & Canonical Keys",
            "- Unit Harmonization (Rs/qtl, kg/ha)",
            "- Reporting Lag & Vintage Alignment",
            "- Gap Analysis & Censoring Audits",
            "- Reference Quality Scorecard"
        ], 480),
        ("STAGE 3: EXPLORATORY LENSES", "Multi-Dimensional Analysis", [
            "- Univariate: Heavy tails, Skew, Outliers",
            "- Bivariate: Price-Arrival Elasticity",
            "- Temporal: Robust STL Seasonality",
            "- Spatial: Interstate LOOP & Dispersion",
            "- Multivariate: Agro-Climatic PCA"
        ], 910),
        ("STAGE 4: RIGOR CONTROLS", "Anomaly & Correlation Guards", [
            "- Hampel Filter & SA-IQR Detection",
            "- Outlier Triage (Type A vs B vs C)",
            "- Detrending & VIF Collinearity Checks",
            "- Rolling Sub-Period Stability Tests",
            "- Cross-Correlation Lead-Lag (CCF)"
        ], 1340),
        ("STAGE 5: ACTIONABLE INSIGHTS", "Decision Frameworks", [
            "- Sourcing & Procurement Timing",
            "- Basis Risk & Hedging Allocations",
            "- Government Buffer Stock Alerts",
            "- Interstate Arbitrage Scheduling",
            "- Downstream Forecasting Inputs"
        ], 1770)
    ]

    col_w = 380
    top_y = 190
    box_h = 780

    for title, subtitle, bullets, x in stages:
        draw_box(d, x, top_y, col_w, box_h, fill=PALE, outline=SECONDARY, radius=14, width=3)
        draw_box(d, x, top_y, col_w, 80, fill=PRIMARY, outline=PRIMARY, radius=14, width=1)
        # square bottom corners for header bar
        d.rectangle([x, top_y + 40, x + col_w, top_y + 80], fill=PRIMARY)

        draw_text(d, x + 20, top_y + 15, title, size=15, bold=True, color="#A3D9C9")
        draw_text(d, x + 20, top_y + 42, subtitle, size=19, bold=True, color=WHITE)

        by = top_y + 115
        for b in bullets:
            draw_text(d, x + 25, by, b, size=18, bold=False, color=INK)
            by += 85

        # Small bottom highlight badge
        draw_box(d, x + 20, top_y + box_h - 75, col_w - 40, 50, fill=WHITE, outline=RULE, radius=8, width=1)
        stage_num = title.split(":")[0]
        draw_text(d, x + col_w // 2, top_y + box_h - 52, f"Verified Milestone: {stage_num}", size=15, bold=True, color=SECONDARY, anchor="mm")

    # Connectors between stages
    for i in range(len(stages) - 1):
        x1 = stages[i][3] + col_w
        x2 = stages[i + 1][3]
        ym = top_y + box_h // 2
        draw_arrow(d, x1 + 6, ym, x2 - 6, ym, color=ACCENT, width=6, arrow_size=20)
        # Small circle gate
        d.ellipse([x1 + 18, ym - 16, x1 + 50, ym + 16], fill=WHITE, outline=ACCENT, width=3)
        draw_text(d, x1 + 34, ym, f"G{i+1}", size=14, bold=True, color=ACCENT, anchor="mm")

    # Bottom Governance Bar
    draw_box(d, 50, 1020, 2100, 160, fill=ALERT_BG, outline=ALERT_BORDER, radius=12, width=2)
    draw_text(d, 80, 1045, "CROSS-CUTTING GOVERNANCE & METHODOLOGICAL GUARDRAILS", size=18, bold=True, color=ALERT_BORDER)
    draw_text(d, 80, 1080, "• Zero Data snooping: Statistical tests and transformations strictly observe historical vintage availability; no lookahead leakage.", size=17, bold=False, color=INK)
    draw_text(d, 80, 1115, "• Genuine Shock Preservation: Extreme weather disruptions and trade bans flagged as structural shifts rather than naively discarded.", size=17, bold=False, color=INK)
    draw_text(d, 80, 1150, "• Downstream Pipeline Feed: Outputs directly parameterize Week 4 predictive model ladders (naive benchmarks, ARIMA, LightGBM).", size=17, bold=False, color=INK)

    out_path = FIG_DIR / "eda_workflow.png"
    img.save(out_path, quality=95)
    print(f"Saved {out_path}")

# -------------------------------------------------------------
# Diagram 2: Agribusiness Visual Selection Decision Tree
# -------------------------------------------------------------
def make_visual_selection_tree():
    W, H = 2200, 1200
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    draw_text(d, 50, 35, "DECISION MATRIX FOR AGRIBUSINESS DATA VISUALIZATION", size=22, bold=True, color=ACCENT)
    draw_text(d, 50, 68, "Matching Agricultural Question Typology to Optimal Perceptual Encodings", size=36, bold=True, color=PRIMARY)
    draw_text(d, 50, 118, "Selecting chart forms that minimize cognitive load, prevent axis distortion, and directly support commercial decision triggers.", size=20, color=MUTED)

    # Root
    root_x, root_y, root_w, root_h = 850, 180, 500, 90
    draw_box(d, root_x, root_y, root_w, root_h, fill=PRIMARY, outline=PRIMARY, radius=14)
    draw_text(d, root_x + root_w // 2, root_y + 25, "ANALYTICAL OBJECTIVE", size=16, bold=True, color="#A3D9C9", anchor="mm")
    draw_text(d, root_x + root_w // 2, root_y + 58, "What agribusiness pattern is being interrogated?", size=20, bold=True, color=WHITE, anchor="mm")

    branches = [
        ("TEMPORAL & CYCLICAL", [
            ("Multi-year price trends", "Small-Multiples Faceted Lines", "Prevents multi-crop 'spaghetti' confusion across 8 states"),
            ("Calendar harvest dips", "Seasonal Subseries / Cycle Plots", "Isolates month-of-year seasonality from macro drift"),
            ("Supply-price feedback", "Phase-Space Cobweb Trajectories", "Plots log-arrivals vs log-price to expose cobweb dynamics")
        ], 60),
        ("SPATIAL & INTEGRATION", [
            ("Regional yield gaps", "Geospatial Choropleths (Binned)", "Avoids pseudo-continuous gradients; highlights deficit zones"),
            ("Inter-mandi arbitrage", "Interstate Box & Strip Plots", "Visualizes price dispersion and freight parity bounds"),
            ("Spatial clustering", "Moran Scatterplots & Maps", "Exposes geographical clusters of severe rainfall deficit")
        ], 580),
        ("DISTRIBUTION & TAILS", [
            ("Price shock & skewness", "Violin Plots + Jittered Points", "Exposes asymmetric fat-tails and multi-modal distributions"),
            ("Arrivals zero-inflation", "Histogram with Kernel Density", "Reveals off-season truncation and peak market gluts"),
            ("Mandi fee distortions", "Cumulative Distribution (ECDF)", "Detects regulatory price floors and procurement clustering")
        ], 1100),
        ("MULTIVARIATE & DRIVERS", [
            ("Cross-factor correlation", "Hierarchically Clustered Heatmap", "Groups mutually collinear climate and input indicators"),
            ("Non-linear climate yield", "Binned Scatter + LOESS Spline", "Captures thermal/moisture damage thresholds without bias"),
            ("Lead-lag transmission", "Cross-Correlation Function (CCF)", "Identifies months of delay from rainfall shock to price peak")
        ], 1620)
    ]

    col_w = 510
    top_y = 350

    # Draw lines from root to 4 branch headers
    for cat_title, items, bx in branches:
        cx = bx + col_w // 2
        d.line([root_x + root_w // 2, root_y + root_h, cx, top_y - 20], fill=SECONDARY, width=3)
        draw_arrow(d, cx, top_y - 20, cx, top_y, color=SECONDARY, width=3, arrow_size=12)

        # Category Header Box
        draw_box(d, bx, top_y, col_w, 75, fill=SECONDARY, outline=SECONDARY, radius=10)
        draw_text(d, bx + col_w // 2, top_y + 38, cat_title, size=21, bold=True, color=WHITE, anchor="mm")

        # 3 Child cards per category
        card_y = top_y + 105
        for q_text, viz_name, why_note in items:
            draw_box(d, bx, card_y, col_w, 215, fill=PALE, outline=RULE, radius=10, width=2)
            draw_box(d, bx + 15, card_y + 15, col_w - 30, 42, fill=WHITE, outline=RULE, radius=6)
            draw_text(d, bx + 25, card_y + 35, f"Question: {q_text}", size=16, bold=True, color=PRIMARY, anchor="lm")

            draw_box(d, bx + 15, card_y + 68, col_w - 30, 46, fill=ACCENT, outline=ACCENT, radius=6)
            draw_text(d, bx + col_w // 2, card_y + 91, f"Recommended: {viz_name}", size=16, bold=True, color=WHITE, anchor="mm")

            draw_text(d, bx + 20, card_y + 130, "Perceptual Rationale:", size=14, bold=True, color=MUTED)
            draw_text(d, bx + 20, card_y + 155, why_note, size=15, bold=False, color=INK)

            card_y += 240

    out_path = FIG_DIR / "visual_selection_tree.png"
    img.save(out_path, quality=95)
    print(f"Saved {out_path}")

# -------------------------------------------------------------
# Diagram 3: Anomaly & Outlier Triage Protocol
# -------------------------------------------------------------
def make_anomaly_triage_flow():
    W, H = 2200, 1150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    draw_text(d, 50, 35, "AGRIBUSINESS ANOMALY TRIAGE & OUTLIER RESOLUTION ARCHITECTURE", size=22, bold=True, color=ACCENT)
    draw_text(d, 50, 68, "Tripartite Classification and Rigorous Handling Protocols", size=36, bold=True, color=PRIMARY)
    draw_text(d, 50, 118, "Differentiating clerical transcription errors from authentic market shocks and liquidity microstructure artifacts.", size=20, color=MUTED)

    # Ingestion box
    draw_box(d, 700, 175, 800, 75, fill=PRIMARY, outline=PRIMARY, radius=12)
    draw_text(d, 1100, 212, "RAW AGRIBUSINESS TICK (Price, Arrival, Yield, Weather)", size=22, bold=True, color=WHITE, anchor="mm")

    # Multi-Stage Detection Bar
    draw_box(d, 200, 300, 1800, 95, fill=PALE, outline=SECONDARY, radius=12, width=3)
    draw_text(d, 230, 325, "DETECTION ENSEMBLE:", size=18, bold=True, color=SECONDARY)
    draw_text(d, 460, 325, "1. Rolling Hampel Filter (k=7, 3-sigma MAD)   |   2. Robust SA-IQR on STL Remainder   |   3. Bivariate Isolation Forest", size=18, bold=False, color=INK)
    draw_text(d, 230, 360, "Threshold Trigger:", size=16, bold=True, color=ACCENT)
    draw_text(d, 460, 360, "Observation violates statistical expectation (|e_t| > 3.0 sigma or Mahalanobis D^2 > chi^2_crit)", size=16, italic=True, color=MUTED)

    draw_arrow(d, 1100, 250, 1100, 300, color=SECONDARY, width=4)

    # Three Outlier Classification Buckets
    buckets = [
        ("TYPE A: CLERICAL / DEFECT", "Data Entry & Measurement Artifacts", [
            "- 10x / 100x unit errors (Rs/kg vs Rs/qtl)",
            "- Misplaced decimal points or trailing zeros",
            "- Duplicate trade reporting on market holidays",
            "- Zero reported when mandi was closed"
        ], [
            "ACTION: REPAIR OR PURGE",
            "- Cross-validate with neighbouring mandis",
            "- If ratio ~10 or ~100, apply unit rescale",
            "- If corrupt/unresolvable, mark NaN & impute",
            "- Log in Central Data Cleaning Audit Trail"
        ], 60, "#C0392B"),
        ("TYPE B: AUTHENTIC SHOCK", "Severe Agro-Ecological & Policy Events", [
            "- Unseasonal hailstorms / flash flood ruin",
            "- Sudden export bans (e.g., onion MEP, wheat ban)",
            "- Severe El Nino drought crop failure",
            "- Panic arrivals preceding port lockdown"
        ], [
            "ACTION: PRESERVE & DUMMY CODE",
            "- NEVER delete or windsorize authentic shocks",
            "- Tag with binary Shock Indicator variable",
            "- Retain for tail-risk & Value-at-Risk modeling",
            "- Split modeling: Baseline vs Stress Scenarios"
        ], 760, "#D35400"),
        ("TYPE C: THIN ILLIQUIDITY", "Market Microstructure Censoring", [
            "- Off-season residual lot (<5 quintals)",
            "- Single distressed farmer lot sold below cost",
            "- Mandi trading halted mid-session due to strike",
            "- Highly localized quality downgrade"
        ], [
            "ACTION: VOLUME-WEIGHT & WINDSORIZE",
            "- Filter out transactions below min volume threshold",
            "- Re-aggregate to weekly volume-weighted price",
            "- Soft windsorization at 1st / 99th percentile",
            "- Exclude from baseline price discovery index"
        ], 1460, "#2980B9")
    ]

    top_by = 460
    b_w = 680
    b_h = 620

    draw_arrow(d, 1100, 395, 400, top_by, color=SECONDARY, width=4)
    draw_arrow(d, 1100, 395, 1100, top_by, color=SECONDARY, width=4)
    draw_arrow(d, 1100, 395, 1800, top_by, color=SECONDARY, width=4)

    for title, subtitle, bullets, actions, bx, header_color in buckets:
        draw_box(d, bx, top_by, b_w, b_h, fill=PALE, outline=RULE, radius=12, width=2)
        # Header Box
        draw_box(d, bx, top_by, b_w, 80, fill=header_color, outline=header_color, radius=12)
        d.rectangle([bx, top_by + 40, bx + b_w, top_by + 80], fill=header_color)

        draw_text(d, bx + 20, top_by + 16, title, size=18, bold=True, color=WHITE)
        draw_text(d, bx + 20, top_by + 46, subtitle, size=15, bold=False, color="#FADBD8")

        # Typical Manifestations
        draw_text(d, bx + 25, top_by + 105, "TYPICAL MANIFESTATIONS:", size=15, bold=True, color=PRIMARY)
        cy = top_by + 135
        for b in bullets:
            draw_text(d, bx + 30, cy, b, size=16, color=INK)
            cy += 48

        # Action Box
        draw_box(d, bx + 20, top_by + 360, b_w - 40, 230, fill=WHITE, outline=RULE, radius=8, width=2)
        draw_text(d, bx + 35, top_by + 380, actions[0], size=16, bold=True, color=header_color)
        ay = top_by + 415
        for a in actions[1:]:
            draw_text(d, bx + 40, ay, a, size=15, color=INK)
            ay += 46

    out_path = FIG_DIR / "anomaly_triage_flow.png"
    img.save(out_path, quality=95)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    make_eda_workflow()
    make_visual_selection_tree()
    make_anomaly_triage_flow()
