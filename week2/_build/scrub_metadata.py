# -*- coding: utf-8 -*-
"""Scrub identifying metadata from the delivered .docx and .pdf.

Run from week2/_build after the PDF export. Files are anonymised to a role.
"""

import datetime
import os
import sys

from docx import Document

DOCX = os.path.join("..", "Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2.docx")
PDF = os.path.join("..", "Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2_preview.pdf")

TITLE = "Data Cleaning and Preprocessing Strategy"
SUBJECT = "Week 2 task - Junior Data Scientist Internship"
AUTHOR = "Data Science Intern"
KEYWORDS = ("data cleaning, preprocessing, agribusiness, data quality, missing data, "
            "outliers, reproducibility")
COMMENTS = ("Week 2 strategy: defect taxonomy, ten-step cleaning plan, method playbooks, "
            "preprocessing framework, workflow, reproducibility and worked examples.")
WHEN = datetime.datetime(2026, 11, 4, 9, 0, 0)


def scrub_docx():
    d = Document(DOCX)
    cp = d.core_properties
    cp.author = AUTHOR
    cp.last_modified_by = AUTHOR
    cp.revision = 1
    cp.created = WHEN
    cp.modified = WHEN
    cp.title = TITLE
    cp.subject = SUBJECT
    cp.keywords = KEYWORDS
    cp.comments = COMMENTS
    cp.category = "Internship deliverable"
    cp.last_printed_by = AUTHOR
    d.save(DOCX)
    print("docx metadata scrubbed")


def scrub_pdf():
    import pymupdf

    d = pymupdf.open(PDF)
    d.set_metadata({
        "title": TITLE,
        "author": AUTHOR,
        "subject": SUBJECT,
        "keywords": KEYWORDS,
        "creator": "Microsoft Word",
        "producer": "Microsoft Word",
        "creationDate": "D:20261104090000+05'30'",
        "modDate": "D:20261104090000+05'30'",
    })
    tmp = PDF + ".tmp"
    d.save(tmp, garbage=3, deflate=True)
    d.close()
    os.replace(tmp, PDF)
    print("pdf metadata scrubbed")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("both", "docx"):
        scrub_docx()
    if which in ("both", "pdf"):
        scrub_pdf()
