# Week 2 — Data Cleaning and Preprocessing Strategy

**Dates:** 29 October – 4 November 2026 · **Status:** ✅ Submitted (v1.0)

## Deliverable

[Data Cleaning and Preprocessing Strategy](Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2.docx) —
42 pages, 17,600 words, 53 tables and one workflow diagram, with a matching
[PDF preview](Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2_preview.pdf).

The report covers the eight defect classes that matter in agribusiness panels, a ten-step
cleaning plan (S0–S9), method playbooks for missing data, outliers, entities, units,
duplicates, revisions and suppression, a five-layer preprocessing framework, a workflow
diagram plus a seventeen-step executable sequence, ten reproducibility controls, six worked
examples and appendices A–H (log schema, flags and dictionary, rule register, checklist,
glossary, assumptions and brief compliance, statistical notes, test catalogue).

It extends Week 1: the fourteen cleaning rules from §6.4 become a register of eighteen
(`R01`–`R18`, including the preprocessing guards), and the §6.5 data dictionary is extended
with quality, vintage and availability fields.

## Reference pipeline

The strategy is demonstrated, not asserted. A seeded generator builds the hypothetical
**Mandi–Yield Panel 2026** (6 crops × 8 states × 72 months, plus annual yields) with defects
planted at documented rates. A separate reference pipeline applies the rules in order and
writes the cleaning log, scorecard and worked examples. The report quotes the pipeline's own
numbers.

Measured on the reference run:

| Metric | Before | After |
|---|---|---|
| Usable price cells | 92.3% | 98.5% |
| Duplicate business keys | 2.2% | 0 |
| Non-ISO dates | 3.3% | 0 |
| Unmapped entity names | 1.6% | 0 |
| Imputation share | — | 4.5% (156 cells, all gaps ≤ 3 months) |
| Logged interventions | — | 550 rows across 9 rules |

The pipeline deliberately does *not* read the defect manifest, so recovery rates are not
inflated by knowing where the errors are.

## Folder contents

```
Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2.docx    submitted report
Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2_preview.pdf
_build/
  synthetic_panel.py      seeded MYP-26 generator (writes raw data + defect manifest)
  cleaning_pipeline.py    rules R01–R14 and yield rules; writes log, scorecard, examples
  derive_facts.py         derives every figure quoted in the report -> report_facts.json
  diagram_workflow.py     draws the workflow figure with Pillow
  docbase.py, cover.py    styling and cover
  sec_a.py … sec_f.py     report sections 1–12 and appendices A–H
  build_week2.py          assembles the DOCX
  export_pdf.ps1          refreshes fields and exports the PDF via Word
  scrub_metadata.py       anonymises DOCX/PDF metadata
  data/                   committed: cleaning_log.csv, scorecard.json,
                          injected_defects.json, examples.json, report_facts.json
                          (raw and clean panels are regenerated, not committed)
  figures/workflow.png
```

## Rebuild

```powershell
cd week2\_build
python synthetic_panel.py
python cleaning_pipeline.py
python derive_facts.py
python diagram_workflow.py
python build_week2.py
python scrub_metadata.py docx
powershell -ExecutionPolicy Bypass -File .\export_pdf.ps1
python scrub_metadata.py pdf
```

Requires Python 3.14 with pandas, NumPy and Pillow, plus Microsoft Word for the PDF export.
Two consecutive pipeline runs produce identical clean-panel hashes
(`c0a070b878b301f5…` for prices, `49cbf0d0e6fa38c5…` for yields).

## Links

- Extends: Week 1, §6.4 (cleaning rules) and §6.5 (data dictionary).
- Feeds: Week 3 exploratory analysis, Week 4 modelling, Week 5 evaluation.
