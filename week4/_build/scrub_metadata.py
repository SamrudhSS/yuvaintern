# -*- coding: utf-8 -*-
"""Scrub metadata from Week 4 DOCX and PDF."""
import datetime, sys
from pathlib import Path
from docx import Document

HERE = Path(__file__).resolve().parent
DOCX = str(HERE / ".." / "Agribusiness_Predictive_Modelling_Framework_Week4.docx")
PDF  = str(HERE / ".." / "Agribusiness_Predictive_Modelling_Framework_Week4_preview.pdf")

TITLE    = "Predictive Modelling Framework for Agribusiness Yield and Price Forecasting"
SUBJECT  = "Week 4 Task – Junior Data Scientist Internship"
AUTHOR   = "Data Science Intern"
KEYWORDS = ("predictive modelling, machine learning, crop yield forecasting, "
            "LightGBM, SARIMAX, ETS, ensemble, SHAP, agribusiness, feature engineering")
COMMENTS = ("Week 4 framework: six-rung model ladder, rolling-origin cross-validation, "
            "118 engineered features, SHAP explainability, universal portability tiers.")
WHEN = datetime.datetime(2026, 11, 18, 9, 0, 0)

def scrub_docx():
    if not Path(DOCX).exists():
        print(f"Not found: {DOCX}"); return
    d = Document(DOCX)
    cp = d.core_properties
    cp.author = cp.last_modified_by = AUTHOR
    cp.revision = 1
    cp.created = cp.modified = WHEN
    cp.title = TITLE; cp.subject = SUBJECT
    cp.keywords = KEYWORDS; cp.comments = COMMENTS
    cp.category = "Internship deliverable"
    d.save(DOCX); print("docx scrubbed")

def scrub_pdf():
    if not Path(PDF).exists():
        print(f"Not found: {PDF}"); return
    try:
        import pymupdf
        d = pymupdf.open(PDF)
        d.set_metadata({"title": TITLE, "author": AUTHOR, "subject": SUBJECT,
                        "keywords": KEYWORDS, "creator": "Microsoft Word",
                        "producer": "Microsoft Word",
                        "creationDate": "D:20261118090000+05'30'",
                        "modDate":      "D:20261118090000+05'30'"})
        tmp = PDF + ".tmp"
        d.save(tmp, garbage=4, deflate=True); d.close()
        import os; os.replace(tmp, PDF); print("pdf scrubbed")
    except Exception as e:
        print(f"pdf scrub skipped: {e}")

if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if mode in ("docx", "all"): scrub_docx()
    if mode in ("pdf",  "all"): scrub_pdf()

