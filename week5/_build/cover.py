# -*- coding: utf-8 -*-
"""Cover and contents pages for the Week 5 evaluation strategy."""

from docx.shared import Pt, Cm
from docx.oxml import OxmlElement

from docbase import (PRIMARY, SECONDARY, ACCENT, PALE, RULE, INK, MUTED, WHITE,
                     CONTENT_W, run_font, spacing, shade, no_borders, cell_margins,
                     fixed_layout, para, spacer, callout, field, el, write_cell,
                     plain_title)


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
    p.paragraph_format.space_before = Pt(64)
    p.paragraph_format.space_after = Pt(22)

    kick = doc.add_paragraph()
    kick.paragraph_format.space_after = Pt(16)
    r = kick.add_run("WEEK 5 OF 5   ·   MODEL EVALUATION AND REPORTING DELIVERABLE")
    run_font(r, size=8.5, bold=True, color=ACCENT)
    spacing(r, 60)

    t = doc.add_paragraph()
    t.paragraph_format.space_after = Pt(2)
    t.paragraph_format.line_spacing = 0.95
    r = t.add_run("Model Evaluation")
    run_font(r, size=31, bold=True, color=PRIMARY)

    t2 = doc.add_paragraph()
    t2.paragraph_format.space_after = Pt(2)
    t2.paragraph_format.line_spacing = 0.95
    r = t2.add_run("& Reporting Strategy")
    run_font(r, size=31, bold=True, color=PRIMARY)

    _rule(doc)

    s = doc.add_paragraph()
    s.paragraph_format.space_after = Pt(0)
    s.paragraph_format.line_spacing = 1.25
    r = s.add_run(
        "A decision-grade framework for judging whether an agribusiness forecast is any good — "
        "and for saying so plainly. It defines the metric suite and the conditions under which each "
        "metric misleads, executes a rolling-origin evaluation on real World Bank price data, "
        "specifies the charts each audience needs, provides an executive-summary template that "
        "survives scrutiny, names the limitations, and sets a prioritised refinement roadmap."
    )
    run_font(r, size=12.0, color=MUTED)

    doc.add_paragraph().paragraph_format.space_after = Pt(82)

    meta = doc.add_table(rows=0, cols=2)
    no_borders(meta)
    cell_margins(meta, top=30, bottom=30, left=0, right=80)
    for k, v in [
        ("Prepared by", "Data Science Intern"),
        ("Programme", "Junior Data Scientist Internship, Nagpur"),
        ("Internship period", "22 October – 26 November 2026"),
        ("Submission date", "25 November 2026"),
        ("Document version", "1.0 (Evaluation Strategy and Executed Audit)"),
        ("Evidence base", "World Bank Pink Sheet, 2000-01 to 2026-10"),
    ]:
        cells = meta.add_row().cells
        write_cell(cells[0], k.upper(), size=7.6, bold=True, color=MUTED)
        write_cell(cells[1], v, size=9.5, color=INK)
    fixed_layout(meta, [3.4, 9.0])


def contents(doc):
    doc.add_paragraph().paragraph_format.page_break_before = True
    plain_title(doc, "Contents", size=18, rule=True, space_after=12)
    para(doc,
         "The document is organised as a working strategy, not a literature review. Part I sets the "
         "evaluation doctrine and the metric definitions. Part II turns the metrics into pictures that "
         "non-specialists can act on. Part III specifies the reporting system and the executive summary. "
         "Part IV states what the evaluation cannot prove, and what to build next. Six appendices carry "
         "the formulae, checklists, templates, reproduction steps and glossary. Refresh page numbers in "
         "Microsoft Word with Ctrl+A → F9.",
         size=9.5, color=MUTED, space_after=10)
    tp = doc.add_paragraph()
    tp.paragraph_format.space_before = Pt(4)
    tp.paragraph_format.space_after = Pt(10)
    field(tp, 'TOC \\o "1-3" \\h \\z \\u', "Table of contents — update on document open.")
    spacer(doc, 10)
    callout(doc, "GOVERNING RULE",
            "Report the range, not only the point. Report the benchmark, not only the raw error. "
            "Report the failure, not only the pass. A number that cannot change a decision is "
            "decoration; a failure that is hidden is a liability.",
            fill=PALE, accent=ACCENT)
