# -*- coding: utf-8 -*-
"""Draw the cleaning-and-preprocessing workflow diagram at readable print size."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures" / "workflow.png"
OUT.parent.mkdir(exist_ok=True)

W, H = 2300, 1400
BG = "#FFFFFF"
INK = "#1F2421"
MUTED = "#5C6B62"
PRIMARY = "#1B4332"
SECONDARY = "#2D6A4F"
ACCENT = "#B5651D"
PALE = "#EDF3EE"
PALE2 = "#F7F9F6"
RULE = "#C9D6CC"

FONT_DIR = Path("C:/Windows/Fonts")
REG = str(FONT_DIR / "calibri.ttf")
BOLD = str(FONT_DIR / "calibrib.ttf")
ITAL = str(FONT_DIR / "calibrii.ttf")


def f(size, bold=False, italic=False):
    path = BOLD if bold else (ITAL if italic else REG)
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def text(x, y, s, size=28, bold=False, color=INK, italic=False, anchor="la"):
    d.text((x, y), s, font=f(size, bold, italic), fill=color, anchor=anchor)


def box(x, y, w, h, fill=PALE, outline=RULE, radius=16, width=3):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill,
                        outline=outline, width=width)


def arrow(x1, y1, x2, y2, color=SECONDARY, width=6):
    import math
    d.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    L, s = 20, 0.45
    for sign in (1, -1):
        d.line([x2, y2,
                x2 - L * math.cos(ang - sign * s),
                y2 - L * math.sin(ang - sign * s)], fill=color, width=width)


def gate(cx, cy, label):
    r = 21
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
              fill="#FFFFFF", outline=ACCENT, width=4)
    text(cx, cy, label, size=15, bold=True, color=ACCENT, anchor="mm")


# header
text(60, 34, "FROM RAW PULL TO MODEL-READY PANEL", size=26, bold=True, color=ACCENT)
text(60, 68, "Eight stages, seven gates, three controls", size=48, bold=True, color=PRIMARY)
text(60, 126, "Cleaning is loss-aware and logged; preprocessing is contract-driven. No stage runs until its gate passes.",
     size=25, color=MUTED)

# lanes
LANE_X, LANE_W = 40, 2220
CLEAN_Y, LANE_H = 176, 410
PRE_Y = 636

box(LANE_X, CLEAN_Y, LANE_W, LANE_H, fill="#FBFCFA", outline=RULE, width=3)
box(LANE_X, PRE_Y, LANE_W, LANE_H, fill="#FBFCFA", outline=RULE, width=3)
text(66, CLEAN_Y + 14, "CLEANING LAYER  ·  S0–S9", size=30, bold=True, color=PRIMARY)
text(66, PRE_Y + 14, "PREPROCESSING LAYER  ·  P0–P6", size=30, bold=True, color=PRIMARY)

BW, BH, GAP = 490, 300, 68
XS = [70 + i * (BW + GAP) for i in range(4)]
TOP = CLEAN_Y + 64
PTOP = PRE_Y + 64

cleaning = [
    ("1", "Freeze & profile", "S0–S1",
     ["Immutable snapshot", "SHA-256 manifest", "Full column profile"]),
    ("2", "Validate & dedupe", "S2–S3",
     ["Types and ranges", "Business-key dedupe", "Survivorship rule"]),
    ("3", "Harmonise", "S4–S5",
     ["Crop and state masters", "Units and currency", "ISO 8601 dates"]),
    ("4", "Repair & freeze", "S6–S9",
     ["Classify every gap", "Flag, never guess", "Reconcile vintages"]),
]

pre = [
    ("5", "Transform", "P0",
     ["Real vs nominal", "Log or level", "Declared per series"]),
    ("6", "Derive & aggregate", "P1–P2",
     ["Ratio of sums", "Lags and windows", "No target features"]),
    ("7", "Encode & scale", "P3–P4",
     ["Fit inside each fold", "Robust scaling", "Controlled vocabulary"]),
    ("8", "Contract", "P5–P6",
     ["As-of joins only", "Leakage assertions", "Signed matrix"]),
]

for i, (num, title, steps, bullets) in enumerate(cleaning):
    x = XS[i]
    box(x, TOP, BW, BH)
    d.ellipse([x + 22, TOP + 20, x + 82, TOP + 80], fill=PRIMARY)
    text(x + 52, TOP + 50, num, size=32, bold=True, color="#FFFFFF", anchor="mm")
    text(x + 98, TOP + 20, title, size=40, bold=True, color=PRIMARY)
    text(x + 98, TOP + 68, steps, size=26, bold=True, color=ACCENT)
    for j, b in enumerate(bullets):
        yy = TOP + 128 + j * 54
        d.ellipse([x + 28, yy + 11, x + 40, yy + 23], fill=SECONDARY)
        text(x + 54, yy, b, size=30, color=INK)

for i, (num, title, steps, bullets) in enumerate(pre):
    x = XS[i]
    box(x, PTOP, BW, BH, fill=PALE2)
    d.ellipse([x + 22, PTOP + 20, x + 82, PTOP + 80], fill=SECONDARY)
    text(x + 52, PTOP + 50, num, size=32, bold=True, color="#FFFFFF", anchor="mm")
    text(x + 98, PTOP + 20, title, size=40, bold=True, color=SECONDARY)
    text(x + 98, PTOP + 68, steps, size=26, bold=True, color=ACCENT)
    for j, b in enumerate(bullets):
        yy = PTOP + 128 + j * 54
        d.ellipse([x + 28, yy + 11, x + 40, yy + 23], fill=SECONDARY)
        text(x + 54, yy, b, size=30, color=INK)

for i in range(3):
    x1 = XS[i] + BW + 6
    x2 = XS[i + 1] - 6
    y = TOP + BH / 2
    arrow(x1, y, x2, y)
    gate((x1 + x2) / 2, y - 52, f"G{i + 1}")

for i in range(3):
    x1 = XS[i] + BW + 6
    x2 = XS[i + 1] - 6
    y = PTOP + BH / 2
    arrow(x1, y, x2, y)
    gate((x1 + x2) / 2, y - 52, f"G{i + 5}")

cx4 = XS[3] + BW / 2
arrow(cx4, TOP + BH + 4, cx4, PTOP - 4)
gate(cx4, (TOP + BH + PTOP) / 2, "G4")

# controls band
CY = 1104
text(60, CY - 36, "CROSS-CUTTING CONTROLS", size=24, bold=True, color=MUTED)
controls = [
    ("IMMUTABLE RAW", "Written once; URL, time, rows and SHA-256 in the manifest"),
    ("CHANGE LOG", "Every change has a rule, a reason and a row identifier"),
    ("TESTS & REBUILD", "Clean clone plus sealed seed reproduces the panel hash"),
]
CW = 720
for i, (label, body) in enumerate(controls):
    x = 40 + i * (CW + 30)
    box(x, CY, CW, 108, fill=PALE, outline=SECONDARY, radius=14, width=3)
    text(x + 22, CY + 16, label, size=22, bold=True, color=PRIMARY)
    text(x + 22, CY + 50, body, size=21, color=INK)

text(60, 1288, "Gates", size=22, bold=True, color=ACCENT)
text(142, 1289,
     "G1 profile  Â·  G2 schema  Â·  G3 entities  Â·  G4 clean frozen  Â·  G5 transforms  Â·  G6 features  Â·  G7 leakage",
     size=21, color=MUTED)

img.save(OUT, dpi=(300, 300))
print(f"saved {OUT}  {img.size[0]}x{img.size[1]}")

