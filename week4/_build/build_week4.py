# -*- coding: utf-8 -*-
"""Assemble the Week 4 Predictive Modelling Framework document."""

import sys
from pathlib import Path
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE))

import cover, sec_a, sec_b, sec_c, sec_d
from docbase import base_document, TABLE_NO, FIG_NO

OUT = HERE.parent / "Agribusiness_Predictive_Modelling_Framework_Week4.docx"


def build():
    TABLE_NO[0] = 0
    FIG_NO[0]   = 0

    doc = base_document()

    cover.cover(doc)
    cover.contents(doc)

    sec_a.section_1(doc)
    sec_a.section_2(doc)
    sec_a.section_3(doc)

    sec_b.section_4(doc)
    sec_b.section_5(doc)

    sec_c.section_6(doc)
    sec_c.section_7(doc)

    sec_d.section_8(doc)
    sec_d.section_9(doc)

    sec_d.appendix_a(doc)
    sec_d.appendix_b(doc)
    sec_d.appendix_c(doc)

    # Auto-refresh TOC
    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)

    cp = doc.core_properties
    cp.title   = "Predictive Modelling Framework for Agribusiness Yield and Price Forecasting"
    cp.subject = "Week 4 Task – Junior Data Scientist Internship, Nagpur"
    cp.author  = "Data Science Intern"
    cp.keywords = ("predictive modelling, machine learning, crop yield forecasting, "
                   "LightGBM, SARIMAX, ETS, ensemble, SHAP, agribusiness, feature engineering")
    cp.comments = ("Week 4 framework: six-rung model ladder, rolling-origin cross-validation, "
                   "118 engineered features, SHAP explainability, universal portability tiers.")
    cp.category = "Internship deliverable"

    doc.save(str(OUT))
    print(f"Saved {OUT}")
    print(f"Tables: {TABLE_NO[0]} | Figures: {FIG_NO[0]}")


if __name__ == "__main__":
    build()

