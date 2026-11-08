# -*- coding: utf-8 -*-
"""Sections 1-4: summary, test panel, quality taxonomy, principles."""

from docbase import (h1, h2, h3, para, bullet, table, callout, kpi_cards,
                     code_block, spacer)
from facts import SCORE, PM, YM, LOG, PANEL, MANIFEST, EX, pct, num


def section_1(doc):
    h1(doc, "1.  Executive Summary", page_break=True)

    para(doc,
         "This document sets out how a messy agribusiness dataset is turned into an analysis-ready "
         "panel without quietly changing what the data says. It is written for the dataset described "
         "in Week 1: six crops, eight Indian states, monthly wholesale prices and annual yields, with "
         "weather and trade series attached later. The strategy is generic where it can be and "
         "specific where specificity prevents error — unit conversion, geography mapping and vintage "
         "handling are all agricultural problems before they are statistical ones.")

    para(doc,
         "The central claim is simple. Cleaning is not a preliminary chore that happens before the "
         "analysis; it is the part of the analysis that determines whether the later results mean "
         "anything. A forecast built on a price series that silently mixes rupees per kilogram with "
         "rupees per quintal will have a plausible shape and a wrong level. A yield model trained on "
         "revised production estimates that were not available at the forecast origin will look "
         "accurate and be unusable. The methods below are designed to make those failures visible, "
         "measurable and hard to repeat.")

    para(doc, "The strategy rests on five commitments:", space_after=4)
    bullet(doc, "one canonical grain, one canonical unit and one canonical key per fact, defined "
                "before any cleaning begins.", lead="One shape — ")
    bullet(doc, "a gap caused by a market holiday is not the same as a gap caused by a missing file, "
                "and neither is the same as a value withheld by the publisher. Treatment follows cause.",
           lead="Classify, then repair — ")
    bullet(doc, "every intervention is a named, parameterised function with a test, not an edit in a "
                "notebook. The rule can be reviewed, versioned and re-run.", lead="Rules, not edits — ")
    bullet(doc, "the count of corrected, imputed, flagged and dropped values is published beside the "
                "clean table, so the effect of cleaning is part of the result rather than hidden "
                "behind it.", lead="Measure the change — ")
    bullet(doc, "a clean clone, a pinned environment and a sealed seed reproduce the panel hash "
                "exactly. If they do not, the pipeline is not finished.", lead="Rebuild or it is not done — ")

    h2(doc, "1.1  What the reference implementation demonstrates")
    para(doc,
         "The strategy is not left as an intention. A seeded generator builds the hypothetical "
         "Mandi–Yield Panel 2026 with known defects planted at documented rates, and a reference "
         "pipeline applies the cleaning rules in order. The report quotes the pipeline's own output, "
         "not numbers typed into the prose. The headline result is small enough to state plainly: "
         "usable price cells rise from "
         f"{pct(PM['completeness_before'])} to {pct(PM['completeness_after'])}, duplicate business "
         f"keys fall from {pct(PM['duplicate_rate_before'])} to zero, and every one of the "
         f"{num(LOG['rows'])} logged interventions carries a rule identifier and a reason.")

    kpi_cards(doc, [
        ("Completeness", pct(PM["completeness_after"]),
         f"from {pct(PM['completeness_before'])} before cleaning"),
        ("Duplicates", "0",
         f"{PM['duplicates_removed']} rows removed on the business key"),
        ("Imputed", pct(PM["imputation_share"]),
         f"{PM['imputed_cells']} cells, all gaps of 3 months or less"),
        ("Log rows", num(LOG["rows"]),
         f"{len(LOG['rules_fired'])} rules fired; every change attributable"),
    ], cols=4)

    para(doc,
         "Two results deserve emphasis because they cut against the instinct to clean aggressively. "
         f"First, {PM['market_closed_cells']} zero prices were reclassified as closed markets rather "
         "than imputed: a zero is information about trading, not a missing number, and filling it "
         "would invent a transaction that never happened. Second, "
         f"{PM['genuine_spikes']} spike was flagged and deliberately retained — a documented price "
         "event that a naive outlier filter would have deleted, taking the most informative part of "
         "the series with it.")

    callout(doc, "The strategy in one sentence",
            "Freeze the raw data, classify every defect by cause, repair only what can be repaired "
            "with evidence, flag the rest, log every intervention, and prove the whole chain rebuilds "
            "from a clean clone.",
            space_after=10)

    h2(doc, "1.2  How this document is organised")
    table(doc,
          ["Part", "Sections", "Question answered"],
          [
              ("Problem", "2–4", "What does the data look like, how does it fail, and what rules govern the response?"),
              ("Method", "5–7", "What exactly is done, in what order, with which method and why?"),
              ("Evidence", "8–10", "What does the sequence look like, how is it reproduced, and what happens to six real cases?"),
              ("Delivery", "11–12", "How is quality signed off, and how does the work land in five days?"),
              ("Reference", "A–H", "Schemas, registers, checklists, glossary, statistical notes and tests."),
          ],
          [2.6, 2.4, 11.6], size=8.6, first_col_bold=True,
          caption_text="Document map. Sections 5–7 carry the method; the appendices carry the operational detail.")

    para(doc,
         "The document assumes no particular software stack, but the reference pipeline uses Python, "
         "pandas and NumPy. Nothing in the method depends on that choice. Where a rule needs a "
         "threshold, the threshold is stated with the reasoning behind it, so that a team using a "
         "different tool can still implement the same decision.")


def section_2(doc):
    h1(doc, "2.  The Hypothetical Dataset")

    para(doc,
         "A strategy document that discusses missing values in the abstract is easy to write and hard "
         "to test. This one works against a defined panel, so every rule can be demonstrated and every "
         "claim measured. The panel is hypothetical, but its defects are modelled on the ones that "
         "actually appear in Indian agricultural statistics: Agmarknet price pulls, DES production "
         "estimates, and the state and district nomenclature that changes around them.")

    h2(doc, "2.1  Panel design")
    para(doc,
         "The Mandi–Yield Panel 2026 (MYP-26) is a crop–state–month price panel with an annual "
         "production and yield panel attached. The grain is deliberate: monthly state-level modal "
         "price for the price table, annual crop–state record for the yield table. Daily mandi quotes "
         "sit below this grain and are aggregated up; district yields sit below it and are aggregated "
         "with a ratio of sums. Fixing the grain first is what makes the duplicate key unambiguous.")

    table(doc,
          ["Property", "Price panel", "Yield panel"],
          [
              ("Grain", "crop × state × month", "crop × state × year × release"),
              ("Crops", "6 — wheat, paddy, maize, soybean, cotton, onion", "same six"),
              ("States", "8 — Maharashtra, Madhya Pradesh, Punjab, Haryana, Uttar Pradesh, Karnataka, Gujarat, Rajasthan", "same eight"),
              ("Period", "January 2020 – December 2025, 72 months", "2020–2025, six years"),
              ("Rows", f"{num(PANEL['rows'])} clean rows; {num(PM['rows_in'])} raw rows", f"{num(PANEL['yield_rows'])} rows across {PANEL['vintages']} release dates"),
              ("Key", "crop_code + state_lgd + period", "crop_code + state_lgd + crop_year + vintage_id"),
              ("Target use", "monthly modal price, 1/3/6/12-month horizons", "annual yield, t/ha"),
          ],
          [2.8, 7.2, 6.6], size=8.4, first_col_bold=True,
          caption_text="MYP-26 at a glance. The clean price panel is a complete 6 × 8 × 72 grid.")

    para(doc,
         f"The clean grid is {num(PANEL['cells'])} cells — six crops, eight states, seventy-two "
         "months. That completeness is a design decision, not an accident: a full grid makes a missing "
         "cell an explicit row with a null and a flag, rather than a row that silently does not exist. "
         "Row-absence is the most expensive kind of missingness in a panel, because every join after "
         "it quietly loses observations and no null count ever reveals the loss.")

    h2(doc, "2.2  Schema")
    para(doc,
         "Every fact table carries the same control columns. The schema is the contract that makes the "
         "cleaning log joinable back to the data: a log entry names a row, a field, an old value and a "
         "new value, and the row identifier is stable across the run.", space_after=4)

    table(doc,
          ["Field", "Type", "Example", "Purpose"],
          [
              ("row_id", "text", "P02786", "Stable identifier for the raw row; the log's foreign key"),
              ("crop", "text", "MAIZE", "Canonical crop code after harmonisation"),
              ("state", "text", "Maharashtra", "Canonical state name; LGD code in the production build"),
              ("month", "date", "2023-07-01", "ISO month start; never a formatted string"),
              ("modal_price_inr_quintal", "float", "2,410.00", "Canonical unit: rupees per quintal"),
              ("source_id", "text", "AGMARKNET", "Foreign key to the source register"),
              ("vintage_id", "text", "2026-10-27", "Publication date of the release used"),
              ("retrieved_at", "timestamp", "2026-10-27T09:14:00Z", "When the snapshot was taken"),
              ("quality_flag", "enum", "imputed_short_gap", "Never null; drives model inclusion"),
              ("outlier_z", "float", "1.84", "Robust z on log price; diagnostic, not a filter"),
          ],
          [4.2, 2.2, 4.4, 5.8], size=8.0, first_col_bold=True,
          caption_text="Core fields. The full dictionary extends this with crop-year, unit and indicator fields.")

    h2(doc, "2.3  How the defects are planted")
    para(doc,
         "The generator injects defects at known rates and records what it did in a manifest that the "
         "cleaning pipeline never reads. That separation matters. If the pipeline were told where the "
         "errors were, it could achieve a perfect score by looking up the answer, and the recovery "
         "rates in this report would be worthless. The pipeline has to find the defects with the same "
         "rules it would use on real data.", space_after=4)

    table(doc,
          ["Defect", "Mechanism", "Rate", "Cells / rows"],
          [
              ("Duplicate retrieval", "Same business key re-pulled and appended", pct(MANIFEST["prices"]["injected"]["rates"]["duplicate_rows"], 2), f"{MANIFEST['prices']['injected']['indices']['duplicate_rows']} rows"),
              ("Missing price", "Cell blank in the source extract", pct(MANIFEST["prices"]["injected"]["rates"]["missing_price"], 2), f"{MANIFEST['prices']['injected']['indices']['missing_price']} cells"),
              ("Zero price", "Market closed or no trade", pct(MANIFEST["prices"]["injected"]["rates"]["zero_price"], 2), f"{MANIFEST['prices']['injected']['indices']['zero_price']} cells"),
              ("Unit drift", "Rupees per kg recorded under a per-quintal label", pct(MANIFEST["prices"]["injected"]["rates"]["unit_drift"], 2), f"{MANIFEST['prices']['injected']['indices']['unit_drift']} cells"),
              ("Decimal slip", "One-place transcription error", pct(MANIFEST["prices"]["injected"]["rates"]["outlier_typo"], 2), f"{MANIFEST['prices']['injected']['indices']['outlier_typo']} cells"),
              ("Digit error", "A digit changed with no clean factor", pct(MANIFEST["prices"]["injected"]["rates"]["outlier_unresolved"], 2), f"{MANIFEST['prices']['injected']['indices']['outlier_unresolved']} cells"),
              ("Date format", "DD/MM/YYYY and Mon-YYYY mixed into ISO", pct(MANIFEST["prices"]["injected"]["rates"]["date_format"], 2), f"{MANIFEST['prices']['injected']['indices']['date_format']} rows"),
              ("Crop alias", "Paddy(Dhan), Rice, Soyabean, Wheat FAQ", pct(MANIFEST["prices"]["injected"]["rates"]["crop_alias"], 2), f"{MANIFEST['prices']['injected']['indices']['crop_alias']} rows"),
              ("State alias", "Maharastra, MP, U.P., Gujrat", pct(MANIFEST["prices"]["injected"]["rates"]["state_alias"], 2), f"{MANIFEST['prices']['injected']['indices']['state_alias']} rows"),
              ("Negative price", "Impossible value from a sign error", pct(MANIFEST["prices"]["injected"]["rates"]["negative_price"], 2), f"{MANIFEST['prices']['injected']['indices']['negative_price']} cells"),
              ("Production unit", "Tonnes filed as thousand tonnes", pct(MANIFEST["yields"]["injected"]["rates"]["production_unit_error"], 2), f"{MANIFEST['yields']['injected']['indices']['production_unit_error']} rows"),
              ("Area unit", "Acres filed as hectares", pct(MANIFEST["yields"]["injected"]["rates"]["area_unit_error"], 2), f"{MANIFEST['yields']['injected']['indices']['area_unit_error']} rows"),
              ("Missing yield", "Yield not reported for a record", pct(MANIFEST["yields"]["injected"]["rates"]["missing_yield"], 2), f"{MANIFEST['yields']['injected']['indices']['missing_yield']} rows"),
          ],
          [3.4, 6.6, 2.3, 3.3], size=7.9, first_col_bold=True,
          caption_text="Planted defects and their rates. Every rate is computable from the manifest, not assumed.")

    para(doc,
         "The defects are not independent. A unit-drift cell that also falls in a missing block is "
         "only a missing cell; a duplicate row that also received an alias is a duplicate only after "
         "the alias is resolved. That overlap is realistic, and it is why the rules have a fixed "
         "order. Applying outlier detection before unit repair, for example, would flag perfectly "
         "valid prices as extreme because they are expressed in a different unit.")

    h2(doc, "2.4  Generator extract")
    para(doc,
         "The generator is short enough to show the mechanism. The point is not the price model; it is "
         "that every defect is written deliberately, with a recorded index, so the strategy can be "
         "scored against ground truth that the cleaner cannot see.", space_after=4)

    code_block(doc, [
        "rng = np.random.default_rng(20261104)          # sealed seed, reported in the manifest",
        "idx = take(38)                                 # 38 unit-drift cells",
        "df.loc[idx, \"modal_price\"] = df.loc[idx, \"modal_price\"] / 100.0",
        "log[\"rates\"][\"unit_drift\"] = len(idx) / n",
        "",
        "idx = take(31)                                 # 31 one-place slips",
        "df.loc[idx[:21], \"modal_price\"] *= 10",
        "df.loc[idx[21:], \"modal_price\"] /= 10",
        "",
        "manifest = {\"seed\": SEED, \"panel\": \"MYP-26\", \"injected\": log}",
        "json.dump(manifest, open(\"injected_defects.json\", \"w\"), indent=2)",
    ], size=8.2)

    para(doc,
         "The yield panel is planted differently. Its errors are not in the yield column at all; they "
         "are in the production and area columns that produce it. A production figure filed in tonnes "
         "rather than thousand tonnes multiplies the implied yield by a thousand, which is "
         "unmistakable; an area filed in acres rather than hectares divides it by 2.471, which is "
         "subtle enough to survive a casual glance. Both are recoverable because the yield is a ratio "
         "of two quantities whose plausible range is known for each crop.")

    h2(doc, "2.5  Why this panel is a fair test")
    para(doc,
         "Three properties make MYP-26 useful as a test bed. It has a complete target grid, so "
         "completeness can be measured against a known denominator. Its defects are of the kinds that "
         "occur in the named public sources, not arbitrary corruption. And its true values are "
         "generated before the defects are applied, so precision and recall of the cleaning rules can "
         "both be computed. A strategy that only reports what it changed, without knowing what it "
         "should have changed, cannot distinguish diligence from over-cleaning.")
    para(doc,
         "The panel is still hypothetical, and Section 12 and Appendix F are explicit about where real "
         "data would differ: irregular publication calendars, PDF-only tables, retrospective revisions "
         "that change history, and suppression rules that vary by state. The method is designed for "
         "those complications; the test panel is simply the cleanest way to prove the mechanics.")


def section_3(doc):
    h1(doc, "3.  Data Quality in Agribusiness Datasets")

    para(doc,
         "Agricultural data is not uniquely dirty, but it is dirty in domain-specific ways. A price "
         "series is produced by a market that closes, a crop is named differently in three states, a "
         "yield estimate is revised twice after its first release, and a district is split into two "
         "districts with new codes. None of these is random noise. Each has a cause, and the cause "
         "determines the correct treatment.")

    h2(doc, "3.1  Six structural causes")
    para(doc, "Before listing symptoms, it helps to name the mechanisms that generate them.", space_after=4)
    bullet(doc, "prices are recorded per quintal in one market, per kilogram in another, and per "
                "tonne in a trade series. The same physical quantity arrives in three numbers.",
           lead="Unit plurality — ")
    bullet(doc, "a crop has a botanical name, a notified name, a local name and a trade name. "
                "'Paddy(Dhan)', 'Rice' and 'Paddy' may refer to the same commodity at different "
                "stages of processing.", lead="Nomenclature drift — ")
    bullet(doc, "districts are renamed, split and merged; states were reorganised in 2014. A name is "
                "not a stable identifier, and a join on names silently duplicates or loses history.",
           lead="Administrative change — ")
    bullet(doc, "advance estimates are replaced by second estimates and then revised estimates. The "
                "number for 2024 changes after 2024 ends, so a model trained today on '2024' is "
                "training on information that did not exist in 2024.", lead="Revision and vintage — ")
    bullet(doc, "mandis close for festivals, weekly markets meet on fixed days, and some commodities "
                "trade only seasonally. A blank cell may mean 'no trade', not 'data lost'.",
           lead="Calendar structure — ")
    bullet(doc, "small counts are suppressed, some series are discontinued, and some states report "
                "late. The absence is a publication decision, not a measurement failure.",
           lead="Suppression and latency — ")

    para(doc,
         "These causes produce the eight defect classes below. The classes are not a list of "
         "annoyances; they are a diagnostic vocabulary. Naming the class correctly is most of the "
         "treatment, because each class has a different repair and a different legitimate fallback.")

    h2(doc, "3.2  Eight defect classes")
    table(doc,
          ["Class", "Typical manifestation", "What it breaks", "Primary detection"],
          [
              ("Missing values", "Blank, null, dash, 'NA', or absent row", "Coverage; model sample; comparability", "Null profile by key and period; row-absence check"),
              ("Duplicates", "Re-pulled rows; same key twice with different retrieval times", "Counts, sums and any row-weighted statistic", "Exact and business-key duplicate counts"),
              ("Format and type", "DD/MM/YYYY vs ISO; prices stored as text with commas", "Joins, sorting, arithmetic", "Type inference; parse failure rate; regex conformance"),
              ("Unit and scale", "INR/kg vs INR/quintal; tonnes vs '000 tonnes; acres vs ha", "Levels and elasticities; any cross-series comparison", "Plausibility band against crop-state median"),
              ("Entity naming", "Crop aliases; state and district variants; whitespace", "Joins; group-by totals; panel balance", "Canonical map; unmatched share; cardinality"),
              ("Outliers and typos", "Decimal slip, digit error, genuine festival spike", "Means, variances, model coefficients", "Robust z on logs; neighbour corroboration"),
              ("Inconsistency", "Same fact differs across sources; totals don't add", "Reconciliation; trust in any single source", "Cross-source ratio; sum-of-parts check"),
              ("Revision and vintage", "Advance estimate overwritten by revised estimate", "Point-in-time correctness; backtest honesty", "Vintage id present; as-of join test"),
          ],
          [3.0, 5.6, 4.4, 3.6], size=7.9, first_col_bold=True,
          caption_text="The eight defect classes and the first test that exposes each.")

    para(doc,
         "A ninth class is worth naming separately even though it is not a defect in the data: "
         "documentation drift. The code that cleans a column and the dictionary that describes it "
         "disagree, or the dictionary describes a unit that the source stopped using two years ago. "
         "It does not appear in a null count, and it is the most common reason a pipeline that worked "
         "last quarter produces a wrong answer this quarter.")

    h2(doc, "3.3  Quality dimensions and thresholds")
    para(doc,
         "Quality is not one number. The strategy scores six dimensions, each with an explicit "
         "threshold. The thresholds are deliberately demanding for the must-have series and looser for "
         "the contextual ones; a single global threshold would either block the build on a minor "
         "series or accept a broken critical one.", space_after=4)

    table(doc,
          ["Dimension", "Definition", "Threshold", "Action on failure"],
          [
              ("Completeness", "Share of expected cells with a usable value", "â‰¥ 98% for must-have price series; â‰¥ 90% otherwise", "Block the series from modelling; investigate source"),
              ("Validity", "Share of values inside the plausible domain", "100% after repair, or explicitly flagged", "Repair with evidence, else flag and exclude"),
              ("Uniqueness", "Duplicate business keys", "0", "Resolve before any aggregation"),
              ("Consistency", "Agreement across overlapping sources", "â‰¤ 5% relative difference, or explained", "Reconcile by documented precedence, never average"),
              ("Timeliness", "Lag from reference period to availability", "Within the stated publication calendar", "Mark provisional; do not backfill silently"),
              ("Accuracy", "Agreement with an independent benchmark", "Within the tolerance set per indicator", "Downgrade the indicator; record the discrepancy"),
          ],
          [2.6, 6.0, 4.4, 3.6], size=8.0, first_col_bold=True,
          caption_text="Six quality dimensions with thresholds. Accuracy is measured, not assumed, and is the only dimension that needs an external benchmark.")

    para(doc,
         "Completeness is the dimension most often reported and least often defined. Here it has a "
         "denominator: the full expected grid for the declared grain. A series that is 100% complete "
         "within the rows it happens to contain can still be 60% complete against the grid. The "
         "distinction is the difference between a dataset that looks clean and one that is usable.")

    h2(doc, "3.4  How defects become wrong answers")
    para(doc,
         "It is tempting to treat cleaning as a cosmetic step before the real work. The four failure "
         "modes below show why it is not. Each is a path from a specific defect to a specific kind of "
         "wrong conclusion, and each is addressed by a named rule later in the document.", space_after=4)
    bullet(doc, "a 100× unit error in 1% of cells shifts a crop mean by roughly the error times the "
                "share. A ₹4,000 quintal price entered as ₹40 per kilogram is not an outlier to be "
                "winsorised; it is a unit to be converted. Treating it as noise biases the level "
                "downward.", lead="Bias from unit and scale — ")
    bullet(doc, "if revised production estimates are used to train a model that is then evaluated on "
                "the advance estimates it would have seen, the backtest is optimistic. The model has "
                "been shown the future.", lead="Leakage from vintage — ")
    bullet(doc, "averaging district yields to obtain a state yield gives every district equal weight, "
                "so a district with 2% of the area contributes as much as one with 40%. The state "
                "figure is then not the state's yield.", lead="Aggregation error — ")
    bullet(doc, "aggressive filtering of 'outliers' deletes genuine scarcity events, which are exactly "
                "the observations a price model needs. The remaining series is well behaved and "
                "uninformative.", lead="False precision from over-cleaning — ")

    callout(doc, "The asymmetry that governs the strategy",
            "A missed defect usually adds noise; an over-aggressive repair adds bias and destroys "
            "evidence. Where the two risks conflict, the strategy prefers to flag rather than "
            "overwrite, and to publish the flag rather than hide it.",
            space_after=8)


def section_4(doc):
    h1(doc, "4.  Governing Principles")

    para(doc,
         "Seven principles decide the many small judgements that a cleaning strategy cannot enumerate "
         "in advance. They are stated as constraints rather than aspirations, because a principle that "
         "cannot be violated is not useful. Each has a practice that implements it and a test that "
         "shows whether it held.")

    principles = [
        ("P1", "Raw is immutable",
         "Every pull is written once to a dated snapshot and never edited. All repair happens "
         "downstream, so the original evidence survives every later decision.",
         "A hash mismatch on any raw file fails the build."),
        ("P2", "Classify before repairing",
         "A gap is classified by cause — closed market, missing file, suppression, late report — "
         "before any method is chosen. The cause selects the treatment; the symptom does not.",
         "Every null in the clean table carries a non-null quality flag."),
        ("P3", "Rules, not edits",
         "Each intervention is a named function with parameters, a rule identifier and a unit test. "
         "No value is changed by hand in a notebook.",
         "The cleaning log contains only rule identifiers from the register."),
        ("P4", "Measure the change",
         "Row counts, completeness, duplicate counts and imputation shares are reported before and "
         "after every step. A step that changes more than 2% of rows needs a written justification.",
         "The scorecard is regenerated on every run and compared with the previous one."),
        ("P5", "Smallest sufficient intervention",
         "Repair only when the evidence determines the correct value. Otherwise flag, exclude from "
         "the relevant use, and leave the value visible.",
         "Corrections are reversible; flags are not deletions."),
        ("P6", "Preserve provenance",
         "Every fact carries its source, vintage, retrieval time and quality flag. A clean value that "
         "cannot be traced to a source is not clean; it is unattributed.",
         "No fact row has a null source, vintage or flag."),
        ("P7", "Reproducible by construction",
         "The pipeline is deterministic, versioned and runnable from a clean clone. Reproducibility is "
         "a property of the design, not a heroic effort at the end.",
         "A clean clone plus the sealed seed reproduces the panel hash."),
    ]

    for pid, name, body, test in principles:
        h3(doc, f"{pid} — {name}")
        para(doc, body, space_after=2)
        para(doc, f"Test of compliance: {test}", size=9.0, italic=True, color="5C6B62", space_after=6)

    h2(doc, "4.1  The principles in tension")
    para(doc,
         "The principles conflict in predictable places, and the strategy resolves the conflicts in "
         "advance rather than case by case. Completeness pushes toward imputation; smallest "
         "intervention pushes against it. Reproducibility pushes toward freezing rules; accuracy "
         "pushes toward revising them when a source changes. The resolutions are:", space_after=4)

    table(doc,
          ["Tension", "Resolution", "Recorded where"],
          [
              ("Impute vs leave missing", "Impute only short internal gaps where neighbouring values bound the answer; otherwise leave missing and flag.", "R08; §6.1"),
              ("Correct vs flag an outlier", "Correct only when a mechanical cause (unit, decimal place) determines the value; otherwise flag and retain.", "R06–R07; §6.2"),
              ("Reconcile vs choose a source", "Use a documented precedence order; never average disagreeing sources into a number that neither published.", "R12; §6.4"),
              ("Freeze vs update a rule", "Rules are versioned; a change requires a new version, a re-run and a diff of the scorecard.", "§9.3"),
              ("Aggregate vs preserve detail", "Aggregate with a ratio of sums, and keep the detail table so the aggregate can be audited.", "R09; §7.3"),
          ],
          [4.4, 9.6, 2.6], size=8.1, first_col_bold=True,
          caption_text="Five recurring conflicts and their standing resolutions.")

    para(doc,
         "Writing these down matters more than it might appear. In practice, the costly arguments "
         "about data quality happen late, when a result looks wrong and no one remembers why a "
         "particular cell was changed. A standing resolution turns that argument into a lookup: the "
         "rule identifier in the log points to the decision, and the decision points to the principle.")


