# -*- coding: utf-8 -*-
"""Assemble the Week 3 Exploratory Data Analysis (EDA) Report Design document."""

import sys
from pathlib import Path
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE))

import cover
import sec_a
import sec_b
import sec_c
import sec_d
import sec_e
from docbase import base_document, TABLE_NO, FIG_NO

OUT = HERE.parent / "Agribusiness_EDA_Report_Design_Week3.docx"


def build():
    # Reset counters
    TABLE_NO[0] = 0
    FIG_NO[0] = 0

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

    sec_e.appendix_a(doc)
    sec_e.appendix_b(doc)
    sec_e.appendix_c(doc)
    sec_e.appendix_d(doc)
    sec_e.appendix_e(doc)

    # Enable updateFields in Word settings so TOC updates automatically
    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)

    cp = doc.core_properties
    cp.title = "Exploratory Data Analysis (EDA) Report Design"
    cp.subject = "Week 3 Task - Junior Data Scientist Internship, Nagpur"
    cp.author = "Data Science Intern"
    cp.keywords = ("exploratory data analysis, EDA report design, agribusiness trends, "
                   "data visualization, anomaly detection, feature correlation, market intelligence")
    cp.comments = ("Week 3 deliverable: comprehensive outline for an EDA report focusing on "
                   "agribusiness trends, variable taxonomy, perceptual visualizations, statistical "
                   "outlier protocols, correlation guardrails, and operational decision frameworks.")
    cp.category = "Internship deliverable"

    doc.save(str(OUT))
    print(f"Successfully assembled and saved {OUT}")
    print(f"Total tables: {TABLE_NO[0]} | Total figures: {FIG_NO[0]}")


if __name__ == "__main__":
    build()

