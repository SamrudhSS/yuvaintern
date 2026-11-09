# -*- coding: utf-8 -*-
"""Cover page and contents page for the Week 4 Predictive Modelling Framework."""

from docx.shared import Pt, Cm
from docx.oxml import OxmlElement
from docbase import (PRIMARY, SECONDARY, ACCENT, PALE, RULE, INK, MUTED, WHITE,
                     CONTENT_W, run_font, spacing, shade, no_borders, cell_margins,
                     fixed_layout, para, spacer, callout, field, el, write_cell, plain_title)


def _rule(doc, width_cm=5.0, color=ACCENT, thick=18):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.right_indent = Cm(CONTENT_W - width_cm)
    ppr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bdr.append(el("w:bottom", **{"w:val": "single", "w:sz": thick,
                                 "w:space": 1, "w:color": color}))
    ppr.append(bdr)


def cover(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(70)
    p.paragraph_format.space_after = Pt(24)

    kick = doc.add_paragraph()
    kick.paragraph_format.space_after = Pt(18)
    r = kick.add_run("WEEK 4 OF 5   ·   PREDICTIVE MODELLING FRAMEWORK DELIVERABLE")
    run_font(r, size=8.5, bold=True, color=ACCENT)
    spacing(r, 60)

    t = doc.add_paragraph()
    t.paragraph_format.space_after = Pt(2)
    t.paragraph_format.line_spacing = 0.95
    r = t.add_run("Predictive Modelling")
    run_font(r, size=31, bold=True, color=PRIMARY)
    t2 = doc.add_paragraph()
    t2.paragraph_format.space_after = Pt(14)
    t2.paragraph_format.line_spacing = 0.95
    r = t2.add_run("Framework")
    run_font(r, size=31, bold=True, color=PRIMARY)

    _rule(doc)

    s = doc.add_paragraph()
    s.paragraph_format.space_after = Pt(0)
    s.paragraph_format.line_spacing = 1.25
    r = s.add_run(
        "A rigorous, universally portable proposal for forecasting agribusiness performance metrics — "
        "covering feature engineering from 42 raw variables to 118 predictors, rolling-origin "
        "time-series cross-validation, a six-rung model ladder from naive benchmarks through gradient-boosted "
        "ensembles, SHAP explainability, calibrated prediction intervals, and a data-availability tiering "
        "system that adapts the same framework to any crop, region, or data-scarce market."
    )
    run_font(r, size=12.2, color=MUTED)

    doc.add_paragraph().paragraph_format.space_after = Pt(96)

    meta = doc.add_table(rows=0, cols=2)
    no_borders(meta)
    cell_margins(meta, top=30, bottom=30, left=0, right=80)
    for k, v in [
        ("Prepared by",       "Data Science Intern"),
        ("Programme",         "Junior Data Scientist Internship, Nagpur"),
        ("Internship period",  "22 October – 26 November 2026"),
        ("Submission date",    "18 November 2026"),
        ("Document version",  "1.0 (Comprehensive Specification)"),
    ]:
        cells = meta.add_row().cells
        write_cell(cells[0], k.upper(), size=7.6, bold=True, color=MUTED)
        write_cell(cells[1], v, size=9.5, color=INK)
    fixed_layout(meta, [3.4, 9.0])


def contents(doc):
    doc.add_paragraph().paragraph_format.page_break_before = True
    plain_title(doc, "Contents", size=18, rule=True, space_after=14)
    para(doc,
         "This framework document is organized into Part I: the technical machine-learning architecture "
         "(Sections 1–7) and Part II: the final report blueprint and universality guidance (Sections 8–9 "
         "and Appendices A–D). Refresh page numbers in Microsoft Word via Ctrl+A → F9.",
         size=9.5, color=MUTED, space_after=14)
    tp = doc.add_paragraph()
    tp.paragraph_format.space_before = Pt(4)
    tp.paragraph_format.space_after = Pt(12)
    field(tp, 'TOC \\o "1-3" \\h \\z \\u', "Table of contents — update on document open.")
    spacer(doc, 14)
    callout(doc, "GOVERNING RULE",
            "No model is reported unless it beats BOTH naive benchmarks (Random Walk and Seasonal Naive) "
            "at every evaluated forecast horizon. MASE must be strictly below 1.0 against both baselines. "
            "A model that fails this promotion rule is documented as a failure, not silently omitted.",
            fill=PALE, accent=ACCENT)

