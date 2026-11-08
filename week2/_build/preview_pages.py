# -*- coding: utf-8 -*-
"""Render selected PDF pages for visual review."""

import sys
from pathlib import Path

import pymupdf

pdf = Path(__file__).resolve().parent.parent / "Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2_preview.pdf"
out = Path(__file__).resolve().parent / "figures" / "pages"
out.mkdir(exist_ok=True)

pages = [int(x) for x in sys.argv[1:]] or [1, 2, 3, 5, 9, 14, 20, 26, 32, 38, 43]
doc = pymupdf.open(pdf)
for p in pages:
    if 1 <= p <= len(doc):
        pix = doc[p - 1].get_pixmap(dpi=105)
        target = out / f"p{p:02d}.png"
        pix.save(target)
        print(target)
