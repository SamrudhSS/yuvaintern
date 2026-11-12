# -*- coding: utf-8 -*-
"""Scrub metadata from the Week 5 DOCX and PDF."""
import datetime
import sys
from pathlib import Path

from docx import Document

HERE = Path(__file__).resolve().parent
DOCX = str(HERE / ".." / "Agribusiness_Model_Evaluation_Reporting_Strategy_Week5.docx")
PDF = str(HERE / ".." / "Agribusiness_Model_Evaluation_Reporting_Strategy_Week5_preview.pdf")

TITLE = "Model Evaluation and Reporting Strategy for Agribusiness Forecasting"
SUBJECT = "Week 5 Task – Junior Data Scientist Internship, Nagpur"
AUTHOR = "Data Science Intern"
KEYWORDS = ("model evaluation, forecast evaluation, MASE, RMSE, MAE, R-squared, "
            "prediction intervals, calibration, visualisation, executive reporting, "
            "agribusiness, limitations, refinement roadmap")
COMMENTS = ("Week 5 strategy: metric suite and failure modes, rolling-origin evaluation, "
            "stakeholder visualisation system, executive summary template, limitation "
            "register and refinement roadmap, executed on real World Bank price data.")
WHEN = datetime.datetime(2026, 11, 25, 9, 0, 0)


def scrub_docx():
    if not Path(DOCX).exists():
        print(f"Not found: {DOCX}")
        return
    d = Document(DOCX)
    cp = d.core_properties
    cp.author = cp.last_modified_by = AUTHOR
    cp.revision = 1
    cp.created = cp.modified = WHEN
    cp.title = TITLE
    cp.subject = SUBJECT
    cp.keywords = KEYWORDS
    cp.comments = COMMENTS
    cp.category = "Internship deliverable"
    d.save(DOCX)
    print("docx scrubbed")


def scrub_pdf():
    if not Path(PDF).exists():
        print(f"Not found: {PDF}")
        return
    try:
        import pymupdf
        d = pymupdf.open(PDF)
        d.set_metadata({"title": TITLE, "author": AUTHOR, "subject": SUBJECT,
                        "keywords": KEYWORDS, "creator": "Microsoft Word",
                        "producer": "Microsoft Word",
                        "creationDate": "D:20261125090000+05'30'",
                        "modDate": "D:20261125090000+05'30'"})
        tmp = PDF + ".tmp"
        d.save(tmp, garbage=4, deflate=True)
        d.close()
        import os
        os.replace(tmp, PDF)
        print("pdf scrubbed")
    except Exception as exc:
        print(f"pdf scrub skipped: {exc}")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if mode in ("docx", "all"):
        scrub_docx()
    if mode in ("pdf", "all"):
        scrub_pdf()
