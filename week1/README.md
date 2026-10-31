# Week 1 — Agribusiness Data Analysis Planning

**Submitted:** 27 October 2026 · **Gate:** 28 October 2026 · **Status:** ✅ Complete

## Deliverables

| File | Purpose |
|---|---|
| `Agribusiness_Data_Analysis_Plan_Week1.docx` | The report — upload this (37 pages) |
| `Agribusiness_Data_Analysis_Plan_Week1_preview.pdf` | Rendered copy for quick reading |

## What the report commits to

- **Scope:** six crops (wheat, paddy, maize, soybean, cotton, onion) × eight states, India-first with
  global benchmarks rather than pooled data.
- **Target:** monthly modal wholesale price at 1, 3, 6 and 12 months; annual yield per crop and state.
- **Evidence base:** 38 public sources across six families, with access checked on 27 October 2026.
- **Indicators:** 30 across five lenses, ranked into a 12 / 10 / 8 build order.
- **Forecastability:** three tiers — prices get intervals, yields get ranges, policy gets scenarios.
- **Method:** model ladder from two naive forecasts upward — a random walk and a seasonal naive; a model
  is reported only if it beats both, with MASE below 1.0 and calibrated intervals.
- **Execution:** nine phases, fourteen cleaning rules, five dated gates ending 26 November 2026.
- **Evidence:** Appendix F is a pilot run end to end on World Bank monthly commodity prices
  (January 2019 – September 2026, five crops, 2,700 forecast errors per model). It produces the seasonal
  index, the storage-carry calculation and the benchmark backtest on real data, and it is why the
  benchmark rule above is a pair rather than a single series.

## Structure of the report

| Section | Content |
|---|---|
| 1–2 | Executive summary, research rationale, research questions and known failure modes |
| 3 | 38-source data inventory, access verification, gaps and proxies, legal position |
| 4 | 30-indicator framework across supply, price, demand, resource and risk |
| 5 | Panel design, model ladder, feature rules, evaluation protocol, tooling |
| 6 | Nine-phase execution plan, fourteen cleaning rules, data dictionary |
| 7 | Five-week timeline, Gantt schedule, milestones, critical path, contingency |
| 8–12 | Deliverables, risks, governance, budget, project measures |
| Appendices | Glossary, access notes, references, assumptions log, weekly checklist, pilot on real price data |

## Rebuilding

The report is generated with `python-docx` from a set of scripts kept outside version control. The
delivered `.docx` carries a Word contents field: open it and press `Ctrl+A`, then `F9`, to refresh page
numbers if the document is edited.

## Note

This plan is the spine for Weeks 2–5. The cleaning rules (Section 6.4) become the Week 2 strategy, the
indicator framework (Section 4) becomes the Week 3 EDA design, the model ladder (Section 5.3) becomes
the Week 4 framework, and the evaluation protocol (Section 5.5) becomes the Week 5 report.
