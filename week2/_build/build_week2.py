# -*- coding: utf-8 -*-
"""Assemble the Week 2 data cleaning and preprocessing strategy."""

import sys
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import cover
import sec_a
import sec_b
import sec_c
import sec_d
import sec_e
import sec_f
from docbase import base_document, TABLE_NO, FIG_NO

OUT = "..\\Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2.docx"


def build():
    doc = base_document()

    cover.cover(doc)
    cover.contents(doc)

    sec_a.section_1(doc)
    sec_a.section_2(doc)
    sec_a.section_3(doc)
    sec_a.section_4(doc)

    sec_b.section_5(doc)
    sec_c.section_6(doc)

    sec_d.section_7(doc)
    sec_d.section_8(doc)
    sec_d.section_9(doc)

    sec_e.section_10(doc)
    sec_e.section_11(doc)
    sec_e.section_12(doc)

    sec_f.appendix_a(doc)
    sec_f.appendix_b(doc)
    sec_f.appendix_c(doc)
    sec_f.appendix_d(doc)
    sec_f.appendix_e(doc)
    sec_f.appendix_f(doc)
    sec_f.appendix_g(doc)
    sec_f.appendix_h(doc)

    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)

    cp = doc.core_properties
    cp.title = "Data Cleaning and Preprocessing Strategy"
    cp.subject = "Week 2 task - Junior Data Scientist Internship, Nagpur"
    cp.author = "Data Science Intern"
    cp.keywords = ("data cleaning, preprocessing, agribusiness, missing data, outliers, "
                   "reproducibility, data quality, reference pipeline")
    cp.comments = ("Week 2 strategy: defect taxonomy, ten-step cleaning plan, method "
                   "playbooks, preprocessing framework, workflow, reproducibility and "
                   "worked examples on a seeded hypothetical panel.")
    cp.category = "Internship deliverable"

    doc.save(OUT)
    print(f"saved {OUT}  tables={TABLE_NO[0]}  figures={FIG_NO[0]}")


if __name__ == "__main__":
    build()
