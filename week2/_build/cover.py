# -*- coding: utf-8 -*-
"""Cover page and contents page for the Week 2 strategy."""

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
    r = kick.add_run("WEEK 2 OF 5   Â·   STRATEGY DELIVERABLE")
    run_font(r, size=8.5, bold=True, color=ACCENT)
    spacing(r, 60)

    t = doc.add_paragraph()
    t.paragraph_format.space_after = Pt(2)
    t.paragraph_format.line_spacing = 0.95
    r = t.add_run("Data Cleaning and")
    run_font(r, size=31, bold=True, color=PRIMARY)
    t2 = doc.add_paragraph()
    t2.paragraph_format.space_after = Pt(14)
    t2.paragraph_format.line_spacing = 0.95
    r = t2.add_run("Preprocessing Strategy")
    run_font(r, size=31, bold=True, color=PRIMARY)

    _rule(doc)

    s = doc.add_paragraph()
    s.paragraph_format.space_after = Pt(0)
    s.paragraph_format.line_spacing = 1.25
    r = s.add_run(
        "How a deliberately messy agribusiness panel is profiled, repaired, "
        "documented and made reproducible — with a ten-step cleaning plan, "
        "a five-layer preprocessing framework and a worked reference pipeline."
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
        ("Submitted", "4 November 2026"),
        ("Document version", "1.0"),
    ]
    for k, v in rows:
        cells = meta.add_row().cells
        write_cell(cells[0], k.upper(), size=7.6, bold=True, color=MUTED)
        write_cell(cells[1], v, size=9.5, color=INK)
    fixed_layout(meta, [3.4, 9.0])

    doc.add_paragraph().paragraph_format.space_after = Pt(52)

    facts = doc.add_table(rows=1, cols=3)
    no_borders(facts)
    cell_margins(facts, top=110, bottom=110, left=130, right=90)
    data = [
        ("TEST PANEL", "3,456 price cells\n6 crops Â· 8 states Â· 72 months"),
        ("DEFECT CLASSES", "Eight\nwith planted, measurable defects"),
        ("EVIDENCE", "550 log rows\nfrom a seeded reference pipeline"),
    ]
    for i, (k, v) in enumerate(data):
        c = facts.rows[0].cells[i]
        shade(c, PALE)
        c.text = ""
        p1 = c.paragraphs[0]
        p1.paragraph_format.space_after = Pt(4)
        r = p1.add_run(k)
        run_font(r, size=7.2, bold=True, color=SECONDARY)
        spacing(r, 30)
        p2 = c.add_paragraph()
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.15
        for j, line in enumerate(v.split("\n")):
            if j:
                p2.add_run().add_break()
            r = p2.add_run(line)
            run_font(r, size=8.8 if j == 0 else 7.8,
                     bold=(j == 0), color=INK if j == 0 else MUTED)
    fixed_layout(facts, [5.53, 5.53, 5.54])

    doc.add_page_break()


def contents(doc):
    plain_title(doc, "Contents")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("Section headings are clickable; page numbers refer to this document. "
                  "Press Ctrl+A then F9 once opened in Word to refresh the contents.")
    run_font(r, size=8.5, italic=True, color=MUTED)

    toc_p = doc.add_paragraph()
    field(toc_p, r'TOC \o "1-1" \h \z \u',
          "The contents table populates when the field is updated (Ctrl+A, then F9).")
    for r in toc_p.runs:
        run_font(r, size=10, color=INK)

    spacer(doc, 10)

    plain_title(doc, "Document control", size=12.5)
    table(
        doc,
        ["Item", "Detail"],
        [
            ("Title", "Data Cleaning and Preprocessing Strategy"),
            ("Deliverable", "Week 2 task — strategy document"),
            ("Version / status", "1.0 — for evaluation"),
            ("Author", "Data Science Intern, Junior Data Scientist Internship, Nagpur"),
            ("Date of issue", "4 November 2026"),
            ("Companion artefacts", "Reference pipeline, cleaning log, scorecard and rule register (week2/_build)"),
            ("Predecessor", "Week 1 analysis plan — §6.4 cleaning rules and §6.5 data dictionary"),
            ("Scope", "Strategy and reference implementation; no confidential or personal data"),
            ("Distribution", "Internship evaluator; internal project repository"),
        ],
        [3.9, 12.7],
        size=8.6, first_col_bold=True,
        caption_text="Document identification and control record.",
    )


