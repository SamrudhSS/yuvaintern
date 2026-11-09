# -*- coding: utf-8 -*-
"""Cover page and contents page for the Week 3 EDA Report Design."""

from docx.shared import Pt, Cm
from docx.oxml import OxmlElement
from docbase import (PRIMARY, SECONDARY, ACCENT, PALE, RULE, INK, MUTED, WHITE,
                     CONTENT_W, run_font, spacing, shade, no_borders, cell_margins,
                     fixed_layout, table, para, spacer, callout, field,
                     el, write_cell, plain_title)


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
    r = kick.add_run("WEEK 3 OF 5   ·   EDA REPORT DESIGN DELIVERABLE")
    run_font(r, size=8.5, bold=True, color=ACCENT)
    spacing(r, 60)

    t = doc.add_paragraph()
    t.paragraph_format.space_after = Pt(2)
    t.paragraph_format.line_spacing = 0.95
    r = t.add_run("Exploratory Data Analysis")
    run_font(r, size=31, bold=True, color=PRIMARY)
    t2 = doc.add_paragraph()
    t2.paragraph_format.space_after = Pt(14)
    t2.paragraph_format.line_spacing = 0.95
    r = t2.add_run("Report Design")
    run_font(r, size=31, bold=True, color=PRIMARY)

    _rule(doc)

    s = doc.add_paragraph()
    s.paragraph_format.space_after = Pt(0)
    s.paragraph_format.line_spacing = 1.25
    r = s.add_run(
        "A rigorous architectural blueprint for transforming multi-source agribusiness panels into "
        "actionable market intelligence — establishing variable taxonomies, analytical typologies, "
        "perceptual visual encodings, statistical anomaly protocols, and correlation guardrails "
        "across six focal crops and eight key agricultural states."
    )
    run_font(r, size=12.2, color=MUTED)

    doc.add_paragraph().paragraph_format.space_after = Pt(96)

    meta = doc.add_table(rows=0, cols=2)
    no_borders(meta)
    cell_margins(meta, top=30, bottom=30, left=0, right=80)
    rows = [
        ("Prepared by", "Data Science Intern"),
        ("Programme", "Junior Data Scientist Internship, Nagpur"),
        ("Internship period", "22 October – 26 November 2026"),
        ("Submission date", "11 November 2026"),
        ("Document version", "1.0 (Comprehensive Specification)"),
    ]
    for k, v in rows:
        cells = meta.add_row().cells
        write_cell(cells[0], k.upper(), size=7.6, bold=True, color=MUTED)
        write_cell(cells[1], v, size=9.5, color=INK)
    fixed_layout(meta, [3.4, 9.0])


def contents(doc):
    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = True
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(14)
    plain_title(doc, "Contents", size=18, rule=True, space_after=14)

    para(doc,
         "This design document establishes the structural, methodological, and visual blueprint "
         "for the downstream Exploratory Data Analysis (EDA) Report in agribusiness intelligence. "
         "Page numbers reflect the compiled report; update the table below in Microsoft Word via "
         "Ctrl+A followed by F9.",
         size=9.5, color=MUTED, space_after=14)

    # Word TOC Field
    tp = doc.add_paragraph()
    tp.paragraph_format.space_before = Pt(4)
    tp.paragraph_format.space_after = Pt(12)
    field(tp, 'TOC \\o "1-3" \\h \\z \\u', "Table of contents will update upon document opening.")

    spacer(doc, 14)
    callout(doc, "HOW TO READ THIS BLUEPRINT",
            "This document is organized into two interlocking parts: Part I (Sections 1–6) provides the "
            "foundational methodology, data architecture, visual grammar, anomaly protocols, and correlation "
            "guardrails required to conduct rigorous exploratory analysis without statistical artifacts. Part II "
            "(Sections 7–9 & Appendices) provides the concrete chapter-by-chapter outline of the final downstream "
            "EDA report, operational decision trees for four agribusiness stakeholder personas, and technical "
            "reference appendices.",
            fill=PALE, accent=SECONDARY)

