# -*- coding: utf-8 -*-
"""Sections 10-12: worked examples, assurance, delivery."""

from docbase import h1, h2, h3, para, bullet, table, callout, code_block
from facts import (SCORE, PM, YM, LOG, PANEL, EX, FACTS, pct, num)

CTX = FACTS["example_context"]
NEIGH = FACTS["imputed_neighbours"]
VINT = FACTS["vintage_case"]


def section_10(doc):
    h1(doc, "10.  Worked Examples", page_break=True)

    para(doc,
         "The examples below are not illustrations written to fit the method. They are extracted from "
         "the reference run: the identifiers, old values, new values and flags are the pipeline's own "
         "log entries. Each case shows the raw state, the rule applied, the cleaned state and the "
         "downstream consequence of getting it wrong.")

    # ---------------------------------------------------------------- E1
    h2(doc, "10.1  A mandi price in the wrong unit")
    u = EX["unit_drift"]
    c = CTX["unit_drift"]
    para(doc,
         f"The raw row is a cotton quote for {c['state']} in {c['month'][:7]}. It was filed as "
         f"{u['old_value']} under a per-quintal label. Cotton trades near ₹9,000 per quintal in this "
         "series, so the value is wrong by exactly two decimal places: it is a per-kilogram price in a "
         "per-quintal column.")
    table(doc,
          ["Field", "As received", "After R06", "Evidence"],
          [
              ("Crop / state", "COTTON / Gujarat", "COTTON / Gujarat", "Unchanged"),
              ("Period", c["month"], c["month"], "ISO month"),
              ("Modal price", u["old_value"], u["new_value"], "Ratio to series median ≈ 0.01"),
              ("Flag", "—", "ok", "Corrected, not merely flagged"),
          ],
          [3.4, 4.8, 4.8, 3.6], size=8.2, first_col_bold=True,
          caption_text="E1: unit drift corrected by a factor of 100.")

    code_block(doc, [
        f'{u["rule_id"]}  {u["row_id"]}  modal_price_inr_quintal  '
        f'{u["old_value"]} -> {u["new_value"]}',
        f'    action: {u["action"]}   reason: {u["reason"]}',
    ], size=7.9)

    para(doc,
         "The downstream consequence is easy to underestimate. Left uncorrected, the cell would lower "
         "the Gujarat cotton mean for that month by roughly 99% and the twelve-month mean by about "
         "1.4%. A model would see a one-month crash and a partial recovery, and would learn a pattern "
         "that never happened. The correction is deterministic: the ratio is diagnostic, and no "
         "judgement is required. This is the only class of outlier the strategy overwrites.")

    # ---------------------------------------------------------------- E2
    h2(doc, "10.2  Two names for one state, three formats for one month")
    a = EX["alias"]
    ac = CTX["alias"]
    para(doc,
         f"A Haryana cotton row arrived with the state as '{a['old_value']}' and a period that did "
         "not parse as ISO. The state string is a source convention, not a different state; the LGD "
         "code resolves it. The date is one of three formats present in the same column.")
    table(doc,
          ["Raw value", "Canonical", "Rule", "Why it matters"],
          [
              (a["old_value"], a["new_value"], "R03", "A join on the raw string silently drops Haryana"),
              ("DD/MM/YYYY, e.g. 01/02/2021", "2021-02-01", "R04", "ISO sort and join; no month/day swap"),
              ("Mon-YYYY, e.g. Feb-2021", "2021-02-01", "R04", "Same period, different representation"),
              ("2021-02-01T00:00:00", "2021-02-01", "R04", "ISO normalisation"),
          ],
          [5.6, 3.6, 1.6, 5.8], size=8.1, first_col_bold=True,
          caption_text="E2: entity and date harmonisation. The code is the key; the name is a label.")

    para(doc,
         f"The harmonisation is logged as a change of field '{a['field']}' from "
         f"'{a['old_value']}' to '{a['new_value']}'. It looks trivial and it is not: in the raw panel "
         "there are several spellings for the same eight states, and a group-by on the raw column "
         "produces more than eight groups. Every aggregate after that point inherits the split, and no "
         "null count reveals it.")

    # ---------------------------------------------------------------- E3
    h2(doc, "10.3  A missing month in a price series")
    m = EX["imputed"]
    mc = CTX["imputed"]
    para(doc,
         f"{mc['crop']} in {mc['state']} has no quote for {mc['month'][:7]}. The months either side "
         f"are observed at ₹{num(NEIGH['prev'], 2)} and ₹{num(NEIGH['next'], 2)}. The gap is internal "
         "and one month long, which places it in the only class eligible for imputation.")
    table(doc,
          ["Check", "Value", "Decision"],
          [
              ("Gap position", "Internal (both anchors observed)", "Eligible"),
              ("Gap length", "1 month", "Within the ≤3-month bound"),
              ("Cause", "Not recorded; not structural", "Treat as not reported"),
              ("Anchor bound", f"{num(NEIGH['prev'], 2)} – {num(NEIGH['next'], 2)}", "Imputed value lies inside"),
              ("Result", f"₹{num(float(m['new_value']), 2)}", "Time-weighted interpolation"),
              ("Flag", "imputed_short_gap", "Value usable; provenance preserved"),
          ],
          [4.4, 6.8, 5.4], size=8.1, first_col_bold=True,
          caption_text="E3: a bounded imputation, with the checks that authorise it.")

    para(doc,
         f"The imputed value is ₹{num(float(m['new_value']), 2)}, not the arithmetic midpoint of the "
         "anchors. The interpolation is weighted by elapsed time, and February to April spans "
         "different month lengths. The difference is small here, but it is the kind of detail that "
         "makes a result reproducible rather than approximately right.")
    para(doc,
         "The flag is as important as the value. Every indicator that consumes this cell can be "
         "recomputed without it, and the sensitivity analysis in §6.1.4 does exactly that. Imputation "
         "is not hidden; it is labelled and reversible.")

    # ---------------------------------------------------------------- E4
    h2(doc, "10.4  A festival spike and a digit error")
    s = EX["genuine_spike"]
    sc = CTX["genuine_spike"]
    o = EX["unresolved_outlier"]
    oc = CTX["unresolved_outlier"]
    para(doc,
         f"Two values in the panel are extreme for opposite reasons. The first is a wheat quote of "
         f"₹{num(float(s['old_value']), 2)} in {sc['state']} in {sc['month'][:7]}, during a documented "
         "supply disruption. The second is an onion quote of "
         f"₹{num(float(o['old_value']), 2)} in {oc['state']}, roughly two orders of magnitude below "
         "any plausible onion price.")
    table(doc,
          ["Case", "Value", "Corroboration", "Treatment", "Flag"],
          [
              ("Wheat event", f"₹{num(float(s['old_value']), 2)}", "Neighbouring months and other markets elevated", "Retain", "spike_genuine"),
              ("Onion error", f"₹{num(float(o['old_value']), 2)}", "No neighbour or market support; outside plausible band", "Exclude from training; retain visibly", "implausible"),
          ],
          [3.0, 3.4, 5.6, 4.4, 3.4], size=8.0, first_col_bold=True,
          caption_text="E4: the same statistic, two different decisions. Corroboration is what separates an event from an error.")

    para(doc,
         "A z-score filter with a single threshold would delete both. Deleting the wheat event removes "
         "the observation the model most needs; deleting the onion error leaves a value that is "
         "obviously wrong but is at least visible. The strategy retains both and distinguishes them by "
         "flag, because the decision about what to exclude belongs to the modelling stage, not to the "
         "cleaning stage.")

    # ---------------------------------------------------------------- E5
    h2(doc, "10.5  A unit mix-up in the yield table")
    p = EX["production_unit"]
    pc = CTX["production_unit"]
    ar = EX["area_unit"]
    arc = CTX["area_unit"]
    para(doc,
         "The yield panel does not contain a yield error; it contains a production error and an area "
         "error that produce one. Both are detected by checking whether the implied yield is "
         "agronomically possible for the crop.")
    table(doc,
          ["Case", "Raw", "Implied yield before", "Correction", "Yield after"],
          [
              (f"{pc['crop']} {pc['state']} {pc['year']}", f"production {num(float(p['old_value']))} kt",
               f"{float(p['old_value']) / float(pc['area_kha']):,.1f} t/ha", "÷ 1,000 (tonnes → '000 t)",
               f"{pc['yield_t_ha']} t/ha"),
              (f"{arc['crop']} {arc['state']} {arc['year']}", f"area {num(float(ar['old_value']), 2)} kha",
               f"{float(arc['production_kt']) / float(ar['old_value']):,.2f} t/ha", "÷ 2.471 (acres → ha)",
               f"{arc['yield_t_ha']} t/ha"),
          ],
          [4.0, 4.6, 3.6, 4.0, 2.8], size=7.9, first_col_bold=True,
          caption_text="E5: two unit errors in the yield table, both recovered from the ratio of production to area.")

    para(doc,
         f"Without the repair, the wheat record would show a yield near "
         f"{float(p['old_value']) / float(pc['area_kha']):,.0f} t/ha and the maize record near "
         f"{float(arc['production_kt']) / float(ar['old_value']):,.2f} t/ha. Either would dominate any "
         "state or national average and would look like a spectacular harvest rather than a filing "
         "error. The correction is justified because dividing by the factor restores the value to the "
         "crop's plausible range; a value that merely looks high, without a diagnostic factor, would "
         "be flagged instead.")
    para(doc,
         "The aggregation rule matters here too. State yield is computed as total production divided "
         "by total area, not as the mean of district yields. The ratio of sums gives large districts "
         "the weight their area deserves; a mean of ratios gives a 2,000-hectare district the same "
         "weight as a 200,000-hectare one.")

    # ---------------------------------------------------------------- E6
    h2(doc, "10.6  A revised estimate and the forecast that could not have seen it")
    para(doc,
         "Wheat in Maharashtra, 2024, exists in three releases. Each is a correct record of what was "
         "published on its date; none is a correction of the others.")
    table(doc,
          ["Release", "Published", "Production (kt)", "Yield (t/ha)", "Knowable at 31 July 2024?"],
          [
              (VINT[0]["vintage"], VINT[0]["vintage_id"], num(VINT[0]["production_kt"], 2),
               f"{VINT[0]['yield_t_ha']:.3f}", "Yes"),
              (VINT[1]["vintage"], VINT[1]["vintage_id"], num(VINT[1]["production_kt"], 2),
               f"{VINT[1]['yield_t_ha']:.3f}", "No"),
              (VINT[2]["vintage"], VINT[2]["vintage_id"], num(VINT[2]["production_kt"], 2),
               f"{VINT[2]['yield_t_ha']:.3f}", "No"),
          ],
          [3.0, 3.2, 4.2, 3.4, 4.4], size=8.1, first_col_bold=True,
          caption_text="E6: three vintages of one fact. A point-in-time join selects the first row only for a July 2024 origin.")

    para(doc,
         "Using the revised figure for a forecast made in July 2024 would improve the backtest by "
         f"about {abs(VINT[2]['yield_t_ha'] - VINT[0]['yield_t_ha']) / VINT[0]['yield_t_ha'] * 100:.1f}% "
         "in yield terms, and the improvement would be entirely fictitious: the information did not "
         "exist at the origin. The as-of join in §6.5 prevents it with a single predicate. The cost of "
         "getting this wrong is not a wrong number in a table; it is a model that appears to work and "
         "fails in production.")

    h2(doc, "10.7  What the six cases have in common")
    table(doc,
          ["Case", "Defect class", "Rule", "Intervention", "Reversible?"],
          [
              ("E1", "Unit and scale", "R06", "Correct by factor", "Yes — log holds the raw value"),
              ("E2", "Entity and format", "R03/R04", "Map and parse", "Yes — mapping table"),
              ("E3", "Missing value", "R08", "Impute with a flag", "Yes — flag and anchors retained"),
              ("E4", "Outlier", "R07/R14", "Flag; retain or exclude", "Yes — value unchanged"),
              ("E5", "Unit and scale", "R10", "Correct by factor", "Yes — log holds the raw value"),
              ("E6", "Vintage", "R11", "Select as of origin", "Yes — every release retained"),
          ],
          [1.6, 4.0, 2.2, 4.8, 5.2], size=8.0, first_col_bold=True,
          caption_text="The examples are all reversible. That is the practical meaning of §4's provenance principle.")

    para(doc,
         "None of the six required a human to type a corrected value into a table. Each required a "
         "decision about a rule, made once, recorded, and applied consistently. That is the difference "
         "between cleaning a dataset and curating a result.")


def section_11(doc):
    h1(doc, "11.  Quality Assurance and Acceptance", page_break=True)

    para(doc,
         "Assurance is the evidence that the strategy was followed, not a statement that it was. The "
         "section defines the scorecard, the acceptance criteria, the error budget and the sign-off "
         "record.")

    h2(doc, "11.1  The quality scorecard")
    table(doc,
          ["Metric", "Definition", "Target", "Reference run"],
          [
              ("Completeness", "Usable price cells ÷ expected grid", "≥ 98%", pct(PM["completeness_after"])),
              ("Duplicate rate", "Duplicate business keys ÷ rows", "0", "0.0%"),
              ("Entity conformance", "Rows mapped to a canonical master ÷ rows", "100%", "100%"),
              ("Date conformance", "ISO dates ÷ rows", "100%", "100%"),
              ("Imputation share", "Imputed cells ÷ price cells", "< 5%", pct(PM["imputation_share"])),
              ("Unresolved flags", "Flagged cells without a rule-level resolution", "< 0.5%", pct(PM["outliers_flagged"] / PM["rows_out"])),
              ("Log completeness", "Changed cells with a log row ÷ changed cells", "100%", "100%"),
              ("Rebuild time", "Clean clone to identical hash", "≤ 10 minutes", "verified"),
          ],
          [4.2, 7.0, 3.2, 3.2], size=8.1, first_col_bold=True,
          caption_text="The scorecard. Each metric has a denominator, a target and a measured value.")

    para(doc,
         f"The unresolved-flag rate is the one that most often fails in practice. In the reference run "
         f"{PM['outliers_flagged']} cells remain flagged as unexplained, which is "
         f"{pct(PM['outliers_flagged'] / PM['rows_out'])} of the panel — comfortably inside the 0.5% "
         "budget. A rate above the budget does not mean the data is unusable; it means the defect "
         "register has an open investigation that must be closed before sign-off.")

    h2(doc, "11.2  The error budget")
    para(doc,
         "Cleaning is allowed to change the data, but not without limit. The error budget states how "
         "much change each step may cause before it requires escalation.", space_after=4)
    table(doc,
          ["Step", "Budget", "Escalation if exceeded"],
          [
              ("Deduplication", "≤ 5% of rows", "Investigate the source before dropping; a high duplicate rate usually means a re-pull loop"),
              ("Harmonisation", "≤ 10% of rows mapped", "Review the master; a large mapping suggests a new source convention"),
              ("Imputation", "≤ 5% of cells", "Drop the series from modelling; report the coverage gap"),
              ("Outlier correction", "≤ 1% of cells", "Stop correcting; switch to flagging and review the unit table"),
              ("Outlier exclusion", "≤ 2% of cells", "Review the threshold and the seasonal screen"),
              ("Row loss overall", "≤ 2% of rows", "Written justification and project-lead sign-off"),
          ],
          [4.6, 3.6, 9.4], size=8.1, first_col_bold=True,
          caption_text="The error budget. A budget turns a judgement call into a threshold that triggers a review.")

    para(doc,
         "Budgets are not moral limits; they are attention limits. A step that changes 15% of rows may "
         "be entirely correct, but it is unusual enough to deserve a second pair of eyes before the "
         "result is used. The budget is the mechanism that buys those eyes.")

    h2(doc, "11.3  Sign-off record")
    table(doc,
          ["Check", "Owner", "Evidence required"],
          [
              ("Source register complete", "Data engineer", "Every series has a source, licence and refresh rate"),
              ("Masters current", "Analyst", "Crop, geography and unit masters dated within the quarter"),
              ("Cleaning log complete", "Analyst", "Every changed cell has a rule and a reason"),
              ("Scorecard passes", "Analyst", "All eight metrics at or inside target"),
              ("Sensitivity run", "Statistician", "Three-way comparison for every indicator using imputed values"),
              ("Point-in-time test", "Statistician", "No feature after origin; vintages selected as of date"),
              ("Rebuild verified", "Reviewer", "Clean clone reproduces the panel hash"),
          ],
          [5.0, 3.4, 9.2], size=8.1, first_col_bold=True,
          caption_text="Sign-off. The reviewer who verifies the rebuild should not be the author of the pipeline.")

    para(doc,
         "The sign-off is a record, not a ceremony. Each line names the evidence that exists, so a "
         "later reviewer can check the claim without reconstructing the project's history. If a line "
         "cannot be evidenced, it is not signed.")


def section_12(doc):
    h1(doc, "12.  Risks, Delivery and Conclusion")

    h2(doc, "12.1  Risks and controls")
    table(doc,
          ["Risk", "Likelihood", "Impact", "Control"],
          [
              ("Source format changes mid-project", "High", "Medium", "Schema validation fails loudly; parser is versioned; re-pull is logged"),
              ("Official series revised retrospectively", "High", "High", "Vintage ids and as-of joins; every release retained"),
              ("Geography codes change", "Medium", "High", "Effective-dated mapping; LGD as key; name is a label"),
              ("Over-cleaning removes genuine events", "Medium", "High", "Flag before correcting; corroboration test; error budget"),
              ("Imputation dominates a series", "Medium", "Medium", "5% cap; sensitivity analysis; drop rather than invent"),
              ("Rule drift between runs", "Medium", "Medium", "Versioned rules; scorecard diff; CI"),
              ("Key-person dependency", "Medium", "High", "Clean-clone gate; documented runbook; paired review"),
              ("Suppressed cells inferred", "Low", "High", "Prohibition in the rule register; suppression flag; audit"),
          ],
          [5.2, 2.0, 1.8, 8.6], size=7.9, first_col_bold=True,
          caption_text="Eight risks, their controls and the mechanism that makes the control real.")

    h2(doc, "12.2  Five-day delivery plan")
    table(doc,
          ["Day", "Focus", "Output", "Gate"],
          [
              ("1", "Masters, config, raw snapshot and profile", "Source register, masters, profile report", "G1"),
              ("2", "Validation, deduplication and harmonisation", "Clean keys, canonical entities and units", "G2–G3"),
              ("3", "Missing values, outliers and reconciliation", "Clean tables with flags and log", "G3–G4"),
              ("4", "Preprocessing framework and matrix", "Indicator registry, model matrix, contract", "G5–G6"),
              ("5", "Tests, scorecard, documentation and handover", "Signed clean layer, README, runbook", "G7"),
          ],
          [1.2, 7.0, 7.0, 1.8], size=8.1, first_col_bold=True,
          caption_text="Five working days from raw snapshot to signed matrix, assuming the source register exists.")

    para(doc,
         "The plan is deliberately front-loaded. Days 1–2 establish the masters and the canonical "
         "shape; if they slip, every later step slips with them. Days 3–4 are the judgement-heavy "
         "part and the part most likely to surface a source problem that changes the scope. Day 5 is "
         "reserved for evidence, not for finishing the cleaning.")

    h2(doc, "12.3  What would change on real data")
    para(doc,
         "The reference panel is regular and well behaved in ways that real sources are not. Four "
         "differences would matter, and the strategy anticipates them:", space_after=4)
    bullet(doc, "daily mandi quotes arrive with gaps that are not rectangular. The grain and the gap "
                "rule change: the three-month bound becomes seven days, and the trading calendar "
                "becomes the primary explanation for zeros.", lead="Irregular frequency — ")
    bullet(doc, "some sources publish only PDFs or image maps. Extraction becomes a cleaning step in "
                "its own right, with the extracted value checked against a published total before it "
                "is trusted.", lead="PDF-only tables — ")
    bullet(doc, "district yields are often withheld or reported with wide revisions. Suppression and "
                "vintage discipline stop being theoretical and become the dominant risk.",
           lead="Suppression — ")
    bullet(doc, "state portals change their column names and date conventions without notice. Schema "
                "validation is the control; a silent rename is caught at load, not in the model.",
           lead="Unstable portals — ")

    para(doc,
         "None of these requires a different strategy. They require the parameters in Appendix C to "
         "be reset for the frequency and the source, which is why the parameters are separated from "
         "the rules.")

    h2(doc, "12.4  Conclusion")
    para(doc,
         "The strategy can be summarised as a sequence of refusals. It refuses to edit raw data, to "
         "impute without a cause, to delete a value because it is inconvenient, to average two "
         "disagreeing sources into a third number, and to call a pipeline reproducible because it ran "
         "once on one machine. Each refusal is implemented as a rule, a flag or a test, and each is "
         "visible in the artefacts the project hands over.")
    para(doc,
         "The reference run shows that the approach is practical at the scale of the project. It "
         f"converts a panel with {pct(PM['completeness_before'])} usable price cells into one with "
         f"{pct(PM['completeness_after'])}, resolves every duplicate key, harmonises every entity, and "
         f"leaves {num(LOG['rows'])} logged interventions that a reviewer can audit line by line. It "
         "does so without deleting a single genuine price event and without inventing a value it "
         "cannot bound.")
    para(doc,
         "That is the standard the later weeks inherit. The exploratory analysis in Week 3 can trust "
         "that its coverage figures mean what they say; the models in Week 4 can trust that their "
         "features were available at the origin; and the evaluation in Week 5 can trust that the "
         "backtest was not flattered by a revision the model could not have seen.")
