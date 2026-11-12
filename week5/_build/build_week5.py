# -*- coding: utf-8 -*-
"""Assemble the Week 5 Model Evaluation and Reporting Strategy document."""

import sys
from pathlib import Path

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE))

import cover
import sec_a
import sec_b
import sec_c
import sec_d
from compact_docx import compact_docx
from docbase import base_document, TABLE_NO, FIG_NO

OUT = HERE.parent / "Agribusiness_Model_Evaluation_Reporting_Strategy_Week5.docx"


def build():
    TABLE_NO[0] = 0
    FIG_NO[0] = 0

    doc = base_document()

    cover.cover(doc)
    cover.contents(doc)

    sec_a.section_1(doc)
    sec_a.section_2(doc)

    sec_b.section_3(doc)
    sec_b.section_4(doc)

    sec_c.section_5(doc)
    sec_c.section_6(doc)

    sec_d.section_7(doc)
    sec_d.section_8(doc)

    sec_d.appendix_a(doc)
    sec_d.appendix_b(doc)
    sec_d.appendix_c(doc)
    sec_d.appendix_d(doc)
    sec_d.appendix_e(doc)
    sec_d.appendix_f(doc)

    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)

    cp = doc.core_properties
    cp.title = "Model Evaluation and Reporting Strategy for Agribusiness Forecasting"
    cp.subject = "Week 5 Task – Junior Data Scientist Internship, Nagpur"
    cp.author = "Data Science Intern"
    cp.keywords = ("model evaluation, forecast evaluation, MASE, RMSE, MAE, R-squared, "
                   "prediction intervals, conformal prediction, calibration, visualisation, "
                   "executive reporting, agribusiness, limitations, refinement roadmap")
    cp.comments = ("Week 5 strategy: metric suite and failure modes, rolling-origin evaluation, "
                   "executed scorecard, stakeholder visualisation system, executive summary "
                   "template, limitation register and refinement roadmap.")
    cp.category = "Internship deliverable"

    doc.save(str(OUT))
    before, after = compact_docx(OUT)
    print(f"Saved {OUT}")
    print(f"Tables: {TABLE_NO[0]} | Figures: {FIG_NO[0]}")
    print(f"Size: {before:,} -> {after:,} bytes ({after / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    build()
