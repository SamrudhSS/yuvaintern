# -*- coding: utf-8 -*-
"""Scrub identifying metadata from the delivered Week 3 .docx and .pdf.

Run from week3/_build after the PDF export. Files are anonymised to a role.
"""

import datetime
import os
import sys
from pathlib import Path
from docx import Document

HERE = Path(__file__).resolve().parent
DOCX = str(HERE / ".." / "Agribusiness_EDA_Report_Design_Week3.docx")
PDF = str(HERE / ".." / "Agribusiness_EDA_Report_Design_Week3_preview.pdf")

TITLE = "Exploratory Data Analysis (EDA) Report Design"
SUBJECT = "Week 3 Task - Junior Data Scientist Internship"
AUTHOR = "Data Science Intern"
KEYWORDS = ("exploratory data analysis, EDA report design, agribusiness trends, "
            "data visualization, anomaly detection, feature correlation, market intelligence")
COMMENTS = ("Week 3 deliverable: comprehensive outline for an EDA report focusing on "
            "agribusiness trends, variable taxonomy, perceptual visualizations, statistical "
            "outlier protocols, correlation guardrails, and operational decision frameworks.")
WHEN = datetime.datetime(2026, 11, 11, 9, 0, 0)


def scrub_docx():
    if not os.path.exists(DOCX):
        print(f"File not found: {DOCX}")
        return
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
    if not os.path.exists(PDF):
        print(f"File not found: {PDF}")
        return
    try:
        import pymupdf
        d = pymupdf.open(PDF)
        d.set_metadata({
            "title": TITLE,
            "author": AUTHOR,
            "subject": SUBJECT,
            "keywords": KEYWORDS,
            "creator": "Microsoft Word / Antigravity",
            "producer": "Microsoft Word",
            "creationDate": "D:20261111090000+05'30'",
            "modDate": "D:20261111090000+05'30'",
        })
        d.save(PDF + ".tmp", garbage=4, deflate=True)
        d.close()
        os.replace(PDF + ".tmp", PDF)
        print("pdf metadata scrubbed")
    except Exception as e:
        print(f"PyMuPDF scrub skipped: {e}")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if mode in ("docx", "all"):
        scrub_docx()
    if mode in ("pdf", "all"):
        scrub_pdf()

