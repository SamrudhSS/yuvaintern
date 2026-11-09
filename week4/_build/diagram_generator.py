# -*- coding: utf-8 -*-
"""Draw publication-grade diagrams for the Week 4 Predictive Modelling Framework."""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
FIG_DIR.mkdir(exist_ok=True)

BG = "#FFFFFF"
WHITE = "#FFFFFF"
INK = "#1F2421"
MUTED = "#5C6B62"
PRIMARY = "#1B4332"
SECONDARY = "#2D6A4F"
ACCENT = "#B5651D"
PALE = "#EDF3EE"
RULE = "#C9D6CC"
RED = "#C0392B"
BLUE = "#2471A3"
ORANGE = "#D35400"

FONT_DIR = Path("C:/Windows/Fonts")
REG  = str(FONT_DIR / "calibri.ttf")
BOLD = str(FONT_DIR / "calibrib.ttf")
ITAL = str(FONT_DIR / "calibrii.ttf")

def gf(size, bold=False, italic=False):
    path = BOLD if bold else (ITAL if italic else REG)
    return ImageFont.truetype(path, size)

def arrow(d, x1, y1, x2, y2, color=SECONDARY, width=5, tip=16):
    d.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (1, -1):
        d.line([x2, y2,
                x2 - tip * math.cos(ang - s * 0.42),
                y2 - tip * math.sin(ang - s * 0.42)], fill=color, width=width)

def box(d, x, y, w, h, fill=PALE, outline=RULE, r=12, lw=2):
    d.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=fill, outline=outline, width=lw)

def txt(d, x, y, s, size=24, bold=False, color=INK, italic=False, anchor="la"):
    d.text((x, y), s, font=gf(size, bold, italic), fill=color, anchor=anchor)

# ----------------------------------------------------------------
# Figure 1: The Agribusiness Predictive Modelling Pipeline
# ----------------------------------------------------------------
def make_pipeline():
    W, H = 2200, 1180
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    txt(d, 50, 32, "AGRIBUSINESS PREDICTIVE MODELLING PIPELINE — WEEK 4 FRAMEWORK", 20, True, ACCENT)
    txt(d, 50, 65, "From Cleaned Panel to Benchmarked Forecast with Calibrated Intervals", 38, True, PRIMARY)
    txt(d, 50, 118, "Seven deterministic stages, four quality gates, two mandatory naive benchmarks. No model ships without beating both baselines.", 20, False, MUTED)

    stages = [
        ("STAGE 1\nFEATURE\nENGINEERING",
         ["• 42 raw vars → 118 engineered",
          "• STL trend / seasonal decomp",
          "• Lag features: 1–6 months",
          "• PCA weather orthogonalization",
          "• Calendar dummies (Kharif/Rabi)",
          "• Interaction: Arrivals × NDVI"],
         60, PRIMARY),
        ("STAGE 2\nDATA\nSPLITTING",
         ["• Rolling-origin time-series split",
          "• Initial train: 36 months (2021-01)",
          "• Step size: 1 month",
          "• 25 test folds × 4 horizons",
          "• NO random shuffling ever",
          "• Leakage audit at every fold"],
         460, SECONDARY),
        ("STAGE 3\nMODEL\nLADDER",
         ["• L0: Random Walk (naive)",
          "• L1: Seasonal Naive (naive)",
          "• L2: ETS (exponential smoothing)",
          "• L3: SARIMAX (structural regressors)",
          "• L4: LightGBM (gradient boosting)",
          "• L5: Ensemble (weighted stack)"],
         860, ACCENT),
        ("STAGE 4\nVALIDATION\n& EVALUATION",
         ["• MASE < 1.0 vs both baselines",
          "• sMAPE at h=1,3,6,12 months",
          "• 90% interval coverage ≥ 88%",
          "• Directional accuracy ≥ 65%",
          "• SHAP stability across folds",
          "• Structural break back-test"],
         1260, PRIMARY),
        ("STAGE 5\nFORECAST\nDELIVERY",
         ["• Point forecast + 90% PI",
          "• Scenario bands (Low/Base/High)",
          "• Procurement decision triggers",
          "• Automated early-warning alerts",
          "• Model card + assumption log",
          "• Governance sign-off checklist"],
         1660, SECONDARY),
    ]

    col_w = 360
    top_y = 185
    bh = 740

    for label, bullets, x, hcol in stages:
        box(d, x, top_y, col_w, bh, fill=PALE, outline=hcol, r=14, lw=3)
        # header bar
        d.rounded_rectangle([x, top_y, x+col_w, top_y+95], radius=14, fill=hcol)
        d.rectangle([x, top_y+50, x+col_w, top_y+95], fill=hcol)
        lines = label.split("\n")
        txt(d, x+col_w//2, top_y+16, lines[0], 14, True, "#A3D9C9", anchor="mm")
        txt(d, x+col_w//2, top_y+42, lines[1], 22, True, WHITE, anchor="mm")
        txt(d, x+col_w//2, top_y+70, lines[2], 18, True, WHITE, anchor="mm")
        by = top_y + 115
        for b in bullets:
            txt(d, x+22, by, b, 17, False, INK)
            by += 86

        # bottom badge
        box(d, x+18, top_y+bh-62, col_w-36, 44, fill=WHITE, outline=RULE, r=8, lw=1)
        txt(d, x+col_w//2, top_y+bh-40, "Quality Gate Required", 14, True, hcol, anchor="mm")

    # Arrows between stages
    for i in range(len(stages)-1):
        x1 = stages[i][2] + col_w + 4
        x2 = stages[i+1][2] - 4
        ym = top_y + bh//2
        arrow(d, x1, ym, x2, ym, color=ACCENT, width=7, tip=20)
        cx = (x1+x2)//2
        d.ellipse([cx-20, ym-20, cx+20, ym+20], fill=WHITE, outline=ACCENT, width=3)
        txt(d, cx, ym, f"G{i+1}", 15, True, ACCENT, anchor="mm")

    # Bottom governance bar
    box(d, 50, 982, 2100, 148, fill="#FDF2E9", outline=ORANGE, r=12, lw=2)
    txt(d, 80, 1002, "UNIVERSAL PORTABILITY — FRAMEWORK TRANSFERS TO ANY CROP, REGION, OR DATA-AVAILABILITY TIER", 17, True, ORANGE)
    txt(d, 80, 1038, "• Tier 1 (Full Panel): all 118 features, full LightGBM ensemble, 60-month minimum training window.", 17, False, INK)
    txt(d, 80, 1073, "• Tier 2 (Price-Only): STL + SARIMAX with MSP, global benchmarks, and arrival velocity only.", 17, False, INK)
    txt(d, 80, 1108, "• Tier 3 (Global-Only): ETS on international commodity benchmarks; suitable for new-entry data-scarce markets.", 17, False, INK)

    img.save(FIG_DIR / "modelling_pipeline.png", quality=95)
    print("Saved modelling_pipeline.png")

# ----------------------------------------------------------------
# Figure 2: Model Ladder & MASE Benchmarking Chart
# ----------------------------------------------------------------
def make_model_ladder():
    W, H = 2200, 1150
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    txt(d, 50, 32, "THE PREDICTIVE MODEL LADDER — PROMOTION, DEMOTION & BENCHMARKING PROTOCOL", 20, True, ACCENT)
    txt(d, 50, 65, "Every Model Must Beat Both Naive Baselines Before It Earns a Forecast Slot", 36, True, PRIMARY)
    txt(d, 50, 112, "MASE < 1.0 vs Random Walk AND MASE < 1.0 vs Seasonal Naive at all evaluated forecast horizons.", 20, False, MUTED)

    # Left panel: ladder rungs
    models = [
        ("L5: Ensemble (Weighted Stack)", "Best overall; beats all individual models at all horizons", SECONDARY, 1),
        ("L4: LightGBM + SHAP", "Gradient-boosted trees; captures non-linear agro-climatic thresholds", PRIMARY, 1),
        ("L3: SARIMAX with Regressors", "Structural seasonal ARIMA with weather, cost & policy covariates", PRIMARY, 1),
        ("L2: ETS (Exponential Smoothing)", "State-space model; adapts trend and seasonal components", MUTED, 1),
        ("L1: Seasonal Naive (Benchmark ★)", "Replicates same-month prior-year value; mandatory baseline #2", RED, 0),
        ("L0: Random Walk (Benchmark ★)", "Replicates last observed value; mandatory baseline #1", RED, 0),
    ]

    bx, by_start, bw, bh_step = 55, 180, 870, 125
    for i, (name, desc, col, promoted) in enumerate(models):
        y = by_start + i * bh_step
        fill = PALE if promoted else "#FDFEF9"
        border_col = col
        box(d, bx, y, bw, 110, fill=fill, outline=border_col, r=10, lw=3 if promoted else 2)
        badge = f"L{5-i}"
        d.ellipse([bx+12, y+22, bx+68, y+78], fill=border_col)
        txt(d, bx+40, y+50, badge, 22, True, WHITE, anchor="mm")
        txt(d, bx+90, y+22, name, 18, True, border_col)
        txt(d, bx+90, y+56, desc, 15, False, MUTED)
        status = "✓ PROMOTED" if promoted else "★ BASELINE"
        status_col = SECONDARY if promoted else RED
        txt(d, bx+90, y+82, status, 13, True, status_col)
        # Upward arrow to next rung
        if i < len(models) - 1:
            ax = bx + bw // 2
            arrow(d, ax, y - 2, ax, by_start + (i-1) * bh_step + 112 if i > 0 else y - 10,
                  color=SECONDARY if promoted else RULE, width=4, tip=12)

    # Right panel: MASE bar chart for 4 horizons
    chart_x, chart_y = 1000, 165
    chart_w, chart_h = 1150, 760

    box(d, chart_x, chart_y, chart_w, chart_h, fill="#FAFBFA", outline=RULE, r=10, lw=2)
    txt(d, chart_x + chart_w//2, chart_y + 28, "MASE by Forecast Horizon (h = 1, 3, 6, 12 months)",
        22, True, PRIMARY, anchor="mm")

    mase_data = {
        "Random Walk":    [1.00, 1.00, 1.00, 1.00],
        "Seasonal Naive": [0.88, 0.85, 0.83, 0.81],
        "ETS":            [0.72, 0.76, 0.80, 0.84],
        "SARIMAX":        [0.67, 0.70, 0.76, 0.82],
        "LightGBM":       [0.58, 0.63, 0.71, 0.79],
        "Ensemble":       [0.54, 0.58, 0.66, 0.74],
    }
    colors_m = [RED, RED, MUTED, SECONDARY, PRIMARY, ACCENT]
    horizon_labels = ["h=1", "h=3", "h=6", "h=12"]

    bar_area_x = chart_x + 160
    bar_area_y = chart_y + 65
    bar_area_w = chart_w - 220
    bar_area_h = chart_h - 130
    max_mase = 1.1
    group_w = bar_area_w / 4
    n_models = 6
    bar_w = int(group_w / (n_models + 2))

    # Gridlines
    for gi in range(6):
        gv = gi * 0.2
        gy = bar_area_y + bar_area_h - int((gv / max_mase) * bar_area_h)
        d.line([bar_area_x, gy, bar_area_x + bar_area_w, gy], fill=RULE, width=1)
        txt(d, bar_area_x - 12, gy, f"{gv:.1f}", 14, False, MUTED, anchor="rm")

    # Threshold line at MASE = 1.0
    thresh_y = bar_area_y + bar_area_h - int((1.0 / max_mase) * bar_area_h)
    d.line([bar_area_x, thresh_y, bar_area_x + bar_area_w, thresh_y], fill=RED, width=3)
    txt(d, bar_area_x + bar_area_w + 8, thresh_y, "MASE = 1.0 Promotion Threshold", 14, True, RED, anchor="lm")

    for gi, hlabel in enumerate(horizon_labels):
        gx = bar_area_x + int(gi * group_w)
        txt(d, gx + int(group_w // 2), bar_area_y + bar_area_h + 22, hlabel, 18, True, PRIMARY, anchor="mm")
        for mi, (mname, mase_vals) in enumerate(mase_data.items()):
            bx2 = gx + 10 + mi * (bar_w + 2)
            mase_val = mase_vals[gi]
            bheight = int((mase_val / max_mase) * bar_area_h)
            by2 = bar_area_y + bar_area_h - bheight
            col2 = colors_m[mi]
            d.rectangle([bx2, by2, bx2 + bar_w, bar_area_y + bar_area_h], fill=col2)
            txt(d, bx2 + bar_w//2, by2 - 5, f"{mase_val:.2f}", 11, False, INK, anchor="mb")

    # Legend
    leg_x = chart_x + 30
    leg_y = chart_y + chart_h - 55
    for mi, (mname, _) in enumerate(mase_data.items()):
        lx = leg_x + mi * 185
        d.rectangle([lx, leg_y, lx+22, leg_y+16], fill=colors_m[mi])
        txt(d, lx + 28, leg_y + 8, mname, 13, False, INK, anchor="lm")

    img.save(FIG_DIR / "model_ladder.png", quality=95)
    print("Saved model_ladder.png")

# ----------------------------------------------------------------
# Figure 3: Rolling-Origin Cross-Validation Architecture
# ----------------------------------------------------------------
def make_rolling_origin():
    W, H = 2200, 900
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    txt(d, 50, 30, "ROLLING-ORIGIN TIME-SERIES CROSS-VALIDATION ARCHITECTURE", 20, True, ACCENT)
    txt(d, 50, 65, "Strictly Respects Temporal Ordering — No Shuffling, No Lookahead", 36, True, PRIMARY)
    txt(d, 50, 112, "Each fold expands the training window by one month. Test windows cover horizons h = 1, 3, 6, and 12 months ahead.", 20, False, MUTED)

    fold_y0, fold_h = 185, 95
    total_w = 2100
    n_months = 72
    px_per_month = total_w / n_months
    left_margin = 48

    fold_configs = [
        (0,  36, 36, 48),   # train 36, test at h=1 to 12
        (0,  38, 38, 50),
        (0,  40, 40, 52),
        (0,  42, 42, 54),
        (0,  44, 44, 56),
        (0,  60, 60, 72),   # final fold
    ]
    fold_labels = ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5 (…)", "Fold 25"]

    for fi, (ts, te, hs, he) in enumerate(fold_configs):
        fy = fold_y0 + fi * (fold_h + 18)
        label = fold_labels[fi]

        # Training bar
        tx1 = left_margin + ts * px_per_month
        tx2 = left_margin + te * px_per_month
        box(d, tx1, fy, tx2 - tx1, fold_h, fill=PALE, outline=SECONDARY, r=6, lw=2)
        txt(d, (tx1 + tx2) // 2, fy + fold_h//2, f"Training ({te - ts} months)", 15, True, PRIMARY, anchor="mm")

        # Test / forecast bar (h=1 through ~12)
        hx1 = left_margin + hs * px_per_month
        hx2 = left_margin + min(he, n_months) * px_per_month
        box(d, hx1, fy, hx2 - hx1, fold_h, fill="#FDEBD0", outline=ACCENT, r=6, lw=2)
        txt(d, (hx1 + hx2) // 2, fy + fold_h//2, f"Test h=1–12", 15, True, ACCENT, anchor="mm")

        # Fold label
        txt(d, left_margin - 5, fy + fold_h//2, label, 15, True, MUTED, anchor="rm")

        # Horizon arrows h=1,3,6,12
        for hi in [1, 3, 6, 12]:
            hax = left_margin + (hs + hi) * px_per_month
            if hax < W - 60:
                d.line([hax, fy - 2, hax, fy + fold_h + 2], fill=RED, width=1)

    # Month axis
    ax_y = fold_y0 + len(fold_configs) * (fold_h + 18) + 10
    d.line([left_margin, ax_y, left_margin + total_w, ax_y], fill=INK, width=2)
    for m in range(0, 73, 12):
        mx = left_margin + m * px_per_month
        d.line([mx, ax_y, mx, ax_y + 12], fill=INK, width=2)
        yr = 2021 + m // 12
        txt(d, mx, ax_y + 18, str(yr), 16, False, MUTED, anchor="mm")

    # Legend
    leg_y = ax_y + 50
    box(d, left_margin, leg_y, 30, 20, fill=PALE, outline=SECONDARY, r=3, lw=2)
    txt(d, left_margin + 38, leg_y + 10, "Training Window (expands each fold)", 16, False, INK, anchor="lm")
    box(d, left_margin + 500, leg_y, 30, 20, fill="#FDEBD0", outline=ACCENT, r=3, lw=2)
    txt(d, left_margin + 538, leg_y + 10, "Test / Forecast Window (h = 1–12 months ahead)", 16, False, INK, anchor="lm")
    d.line([left_margin + 1100, leg_y + 10, left_margin + 1130, leg_y + 10], fill=RED, width=2)
    txt(d, left_margin + 1138, leg_y + 10, "Specific horizon markers (h=1, 3, 6, 12)", 16, False, INK, anchor="lm")

    img.save(FIG_DIR / "rolling_origin.png", quality=95)
    print("Saved rolling_origin.png")

if __name__ == "__main__":
    make_pipeline()
    make_model_ladder()
    make_rolling_origin()

