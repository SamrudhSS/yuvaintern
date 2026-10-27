# Week 2 — Data Cleaning and Preprocessing Strategy

**Dates:** 29 October – 4 November 2026 · **Status:** ⬜ Not started

## Task

Develop a data cleaning and preprocessing strategy for a hypothetical agribusiness dataset: the common
data-quality problems, a step-by-step cleaning plan, and a proposed preprocessing framework, with a
workflow diagram and a discussion of reproducibility.

## Planned content

- Introduction to agribusiness data-quality issues — missing values, inconsistent units and formats,
  duplicates, outliers, revised official estimates, mixed geographic naming.
- A fourteen-rule cleaning workflow, carried forward from Section 6.4 of the [Week 1 plan](../week1/).
- Methods for each defect class: classification of gaps, rule-based imputation bounds, robust outlier
  detection on log prices, canonical unit and geography masters.
- A preprocessing sequence covering validation, harmonisation, transformation, aggregation and
  versioning.
- Reproducibility: immutable raw snapshots, manifest hashes, logged transformations, deterministic runs.
- Worked hypothetical examples — a mangled mandi price row, a district rename, a unit mix-up.

## Files

Added on submission. Report will be `.docx`; supporting notebooks, if any, will sit beside it.

## Links

- Extends: Week 1, Section 6.4 (cleaning rules) and Section 6.5 (data dictionary).
