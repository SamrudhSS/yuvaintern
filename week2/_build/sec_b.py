# -*- coding: utf-8 -*-

"""Section 5: the ten-step cleaning plan."""



from docbase import h1, h2, h3, para, bullet, table, callout, code_block, spacer

from facts import PM, YM, LOG, PANEL, pct, num





def section_5(doc):

    h1(doc, "5.  Step-by-Step Cleaning Plan", page_break=True)



    para(doc,

         "The plan has ten steps, S0 to S9. They run in a fixed order because the output of each is "

         "the precondition of the next: a duplicate cannot be resolved until its key is canonical, a "

         "unit error cannot be detected until the entity is identified, and an outlier cannot be "

         "judged until the unit is right. Reordering the steps is not a stylistic choice; it changes "

         "which values are flagged.")



    para(doc,

         "Each step below states its purpose, its inputs, the actions it takes, the decision rule "

         "that governs ambiguous cases, its output and its gate. The rule identifiers refer to the "

         "register in Appendix C, which also carries the parameter values and the test for each rule.")



    h2(doc, "5.1  The ten steps at a glance")

    table(doc,

          ["Step", "Name", "Core action", "Rules", "Gate"],

          [

              ("S0", "Intake and freeze", "Write an immutable snapshot, capture provenance and hash", "—", "Snapshot hash recorded"),

              ("S1", "Profile and score", "Profile every column and score six quality dimensions", "—", "G1: defect register complete"),

              ("S2", "Schema and domain validation", "Enforce types, ranges, enums and cross-field logic", "R01", "G2: zero unexplained type failures"),

              ("S3", "Deduplicate", "Resolve exact and business-key duplicates with a survivorship rule", "R02", "G2: zero duplicate keys"),

              ("S4", "Harmonise entities and units", "Map crops, geographies, mandis, units and currency", "R03, R06, R10", "G3: zero unmapped entities"),

              ("S5", "Dates and calendars", "Parse to ISO, derive crop/fiscal year, attach trading calendar", "R04, R05", "G3: zero unparsed dates"),

              ("S6", "Missing values", "Classify every gap by cause and apply the bounded treatment", "R08", "Completeness â‰¥ 98%"),

              ("S7", "Outliers", "Flag robust outliers and separate errors from genuine events", "R07, R14", "G4: every flag has a reason"),

              ("S8", "Reconcile sources and vintages", "Apply precedence, keep every release, build as-of views", "R11, R12, R13", "G4: point-in-time test passes"),

              ("S9", "Validate and freeze", "Run the suite, publish the scorecard, sign off and hash", "R14", "G4: clean layer frozen"),

          ],

          [1.2, 3.6, 7.0, 2.8, 2.0], size=7.9, first_col_bold=True,

          caption_text="The ten cleaning steps. The four gates are the same gates shown in the workflow diagram.")



    para(doc,

         f"On MYP-26 the plan fires {num(LOG['rows'])} logged interventions across "

         f"{len(LOG['rules_fired'])} rules. The distribution is informative: most interventions are "

         "harmonisation and gap treatment, not correction of values. That is the normal shape of "

         "cleaning a real panel. Corrections are rare and consequential; harmonisation is frequent "

         "and mechanical; imputation sits in between.")



    h2(doc, "5.2  S0 — Intake and freeze")

    para(doc,

         "The first step is to make the raw data impossible to lose and impossible to alter. Each pull "

         "is written to a dated file under an immutable path, and a manifest row records the source, "

         "the endpoint, the retrieval timestamp, the record count, the licence and the SHA-256 hash. "

         "The raw file is never opened in edit mode again.")

    bullet(doc, "one row per pull, not one row per source. A monthly series pulled twelve times has "

                "twelve manifest rows, because the twelve snapshots are different evidence.",

           lead="Manifest granularity — ")

    bullet(doc, "the manifest is append-only. A failed or partial pull is recorded as failed, not "

                "deleted, so the coverage gap can be explained later.", lead="Failures are data — ")

    bullet(doc, "the source's own identifier, title, unit label and footnote are captured beside the "

                "data. They are often the only clue to a unit change.", lead="Capture the context — ")

    para(doc,

         "Output: a raw folder containing dated files and a manifest. Gate: every file in the folder "

         "has a manifest row and a hash that matches on re-computation.", size=9.5, italic=True,

         color="5C6B62")



    h2(doc, "5.3  S1 — Profile and score")

    para(doc,

         "Profiling answers three questions for every column: what is in it, what is missing from it, "

         "and what cannot be parsed. The profile is generated, not inspected by eye, because the "

         "interesting failures are usually in the tail of a distribution or the edge of a period "

         "range.")

    bullet(doc, "row count, distinct keys, period range, null share, zero share, minimum, maximum, "

                "median and the five most common values, per column and per series.",

           lead="Column profile — ")

    bullet(doc, "the expected grid is generated from the scope (crops × states × months), then "

                "left-joined to the data. Rows that do not exist are counted as missing. This single "

                "check catches more real problems than every other profile combined.",

           lead="Row-absence check — ")

    bullet(doc, "each defect is entered in the defect register with a class, a severity, an example "

                "row and the rule expected to resolve it. The register is the work queue for S2–S8.",

           lead="Defect register — ")

    para(doc,

         f"Baseline scorecard for MYP-26: completeness {pct(PM['completeness_before'])}, exact "

         f"duplicate rate {pct(PM['duplicate_rate_before'])}, non-ISO dates "

         f"{pct(PM['date_non_iso_before'])}, alias share {pct(PM['alias_share_before'])}. These are "

         "the numbers the later steps must improve, and the numbers the final report quotes.",

         size=9.5, italic=True, color="5C6B62")

    para(doc,

         "Output: a profiling report and a prioritised defect register. Gate G1: every column has a "

         "profile, every expected series has a coverage figure, and every critical defect has an "

         "owner and a rule.", size=9.5, italic=True, color="5C6B62")



    h2(doc, "5.4  S2 — Schema and domain validation")

    para(doc,

         "Validation is where the pipeline refuses to guess. A price stored as text with a thousands "

         "separator is coerced to a number and logged; a price stored as 'not available' is nulled and "

         "logged; a price of âˆ’40 is rejected and logged. Silent coercion is forbidden because it "

         "converts a visible source problem into an invisible analytical one.")

    table(doc,

          ["Check", "Rule", "On failure"],

          [

              ("Type", "Numeric field parses as a number", "Coerce if unambiguous; else null and log"),

              ("Domain", "Price > 0, production â‰¥ 0, area > 0, share in [0, 1]", "Null invalid values; never clip silently"),

              ("Enum", "Crop, state, unit, flag drawn from a controlled list", "Reject the row and route to the mapping queue"),

              ("Cross-field", "Production and area imply a plausible yield", "Flag for S4 unit repair"),

              ("Referential", "Every source_id exists in the source register", "Block the load; a missing source is a governance failure"),

              ("Key", "Business key is unique after harmonisation", "Route to S3; never aggregate a duplicated key"),

          ],

          [2.8, 7.6, 6.2], size=8.0, first_col_bold=True,

          caption_text="Validation checks and the response to failure. The default response is to null and log, not to coerce.")



    para(doc,

         "The domain check is not cosmetic. A negative price is impossible, and leaving it in the data "

         "would distort every mean and every log transform downstream. A zero price is possible but "

         "means something different from a price of zero rupees: it means no trade. S2 distinguishes "

         "the two, because S6 will treat them differently.")



    h2(doc, "5.5  S3 — Deduplicate")

    para(doc,

         "There are three kinds of duplicate, and conflating them is a common source of error.",

          space_after=4)

    bullet(doc, "byte-identical rows from a repeated load. Safe to drop after keeping the latest "

                "retrieval.", lead="Exact — ")

    bullet(doc, "the same business key with different values, usually because the source was "

                "re-pulled or revised. Requires a survivorship decision, not a blind drop.",

           lead="Key — ")

    bullet(doc, "the same entity with slightly different names or numbers, often after harmonisation. "

                "Requires fuzzy matching and manual review.", lead="Near — ")

    para(doc,

         "The survivorship rule for MYP-26 is stated once and applied everywhere: prefer the row that "

         "carries a usable price, then the most recent retrieval, then the row with the most populated "

         "fields. Ties are broken by source precedence (Appendix C). The rule is deterministic, which "

         "means the same input always produces the same survivor.")

    para(doc,

         f"In the reference run, {PM['duplicates_removed']} duplicate rows were dropped on the "

         f"business key, taking the duplicate rate from {pct(PM['duplicate_rate_before'])} to zero. "

         "Every drop is in the log with the survivor's row identifier, so a reviewer can reconstruct "

         "the decision. Duplicates are never summed: summing a re-pulled price doubles the weight of "

         "that month in any aggregate, which is a silent bias rather than a visible error.",

         size=9.5, italic=True, color="5C6B62")



    h2(doc, "5.6  S4 — Harmonise entities and units")

    para(doc,

         "Harmonisation is the largest step by row count and the one that most affects joins. It has "

         "four masters, each with one job.", space_after=4)

    table(doc,

          ["Master", "Key", "Contents", "Failure it prevents"],

          [

              ("Crop master", "crop_code", "Canonical name, synonyms, botanical name, variety flag", "Paddy/Rice split into two crops"),

              ("Geography master", "LGD code", "State and district codes with effective dates", "Renamed or split district losing history"),

              ("Mandi register", "mandi_id", "Market name, district, state, active dates", "Two markets with one name"),

              ("Unit table", "unit_code", "Conversion factor to the canonical unit", "INR/kg and INR/quintal in one column"),

          ],

          [3.0, 3.0, 6.6, 4.0], size=8.1, first_col_bold=True,

          caption_text="The four reference masters. Codes, not names, are the join keys.")



    para(doc,

         "Unit repair is the part that requires domain knowledge rather than a lookup. The rule is to "

         "compare each value with a robust median for its crop–state series and act only when the "

         "ratio is diagnostic. A ratio near 0.01 is a per-kilogram entry; a ratio near 10 or 0.1 is a "

         "one-place decimal slip. Anything else is left alone and flagged for review.")

    table(doc,

          ["Observed ratio to series median", "Interpretation", "Action", "Rule"],

          [

              ("0.004 – 0.025", "Price in INR/kg under a per-quintal label", "Multiply by 100", "R06"),

              ("0.05 – 0.20", "One decimal place low", "Multiply by 10", "R06"),

              ("5 – 20", "One decimal place high", "Divide by 10", "R06"),

              ("0.20 – 5 (outside robust band)", "Genuine variation or an unresolved error", "Flag; do not alter", "R07/R14"),

              ("Yield > 8× crop median", "Production in tonnes under a '000-tonne label", "Divide production by 1,000", "R10"),

              ("Yield < 0.55× crop median", "Area in acres under a hectare label", "Divide area by 2.471", "R10"),

          ],

          [5.6, 6.0, 3.4, 1.6], size=8.2, first_col_bold=True,

          caption_text="Unit-repair decision table. The bands are wide enough to absorb seasonality and tight enough to distinguish a unit error from a bad year.")



    para(doc,

         f"The reference run corrected {LOG['unit_drift_fixes']} unit-drift cells and "

         f"{LOG['decimal_fixes']} decimal slips, and repaired {LOG['production_fixes']} production "

         f"and {LOG['area_fixes']} area records in the yield panel. The important number is not the "

         "count but the ordering: unit repair happens before outlier flagging, so the outlier screen "

         "sees prices in one unit. Reversing the order would flag every per-kilogram entry as an "

         "extreme low value and every corrected value as an extreme high one.",

         size=9.5, italic=True, color="5C6B62")



    h2(doc, "5.7  S5 — Dates and calendars")

    para(doc,

         "A date is an identifier, not a string. The parser accepts the formats present in the source "

         "(ISO, DD/MM/YYYY, Mon-YYYY), resolves ambiguity by source convention rather than by "

         "guessing, and writes an ISO month start. Where day and month are both â‰¤ 12 and the source "

         "convention is unknown, the row is quarantined rather than guessed: a silently swapped date "

         "moves a price by a month and is almost impossible to detect downstream.")

    bullet(doc, "ISO 8601 period start, plus explicit crop_year, fiscal_year and "

                "marketing_year columns. Indian fiscal years and crop years do not align with the "

                "calendar, and a model that ignores the difference mis-specifies the season.",

           lead="Three calendars — ")

    bullet(doc, "a state-specific trading calendar marks Sundays, festivals and weekly closures. It "

                "is used to explain zeros, never to forward-fill prices for modelling.",

           lead="Trading calendar — ")

    bullet(doc, "each row keeps retrieved_at and vintage_id alongside the period. The period says "

                "what the row describes; the vintage says when it became knowable.", lead="Period vs vintage — ")



    h2(doc, "5.8  S6 — Missing values")

    para(doc,

         "Missing values are treated as a classification problem before they are treated as an "

         "imputation problem. The taxonomy below is the core of the method; the imputation rule is "

         "deliberately narrow.", space_after=4)

    table(doc,

          ["Class", "Cause", "Example", "Treatment"],

          [

              ("Structural", "Market closed, no trade, seasonal absence", "Sunday; onion not traded in June", "Keep missing; attach calendar feature; never impute"),

              ("Suppressed", "Publisher withholds a small count", "District yield withheld", "Keep missing; flag; never back-calculate"),

              ("Not reported", "Source missed a period", "State did not file for a month", "Impute only if internal gap â‰¤ 3 months; else leave"),

              ("Lost", "File or field missing in the pull", "Column absent from one release", "Re-pull; if impossible, treat as not reported and log"),

              ("Not applicable", "Concept does not apply", "Variety price where no variety market exists", "Keep null; exclude from that indicator"),

              ("Unknown", "Cause not determinable", "Blank with no footnote", "Leave missing; sensitivity analysis; do not impute"),

          ],

          [2.6, 5.4, 5.0, 3.6], size=8.0, first_col_bold=True,

          caption_text="The missing-value taxonomy. Only one of the six classes is eligible for imputation.")



    para(doc,

         "The imputation rule is bounded in three ways: by gap length, by neighbours and by the "

         "plausible range. An internal gap of up to three months is filled by time interpolation "

         "between the surrounding observed values. A longer gap is left missing, because interpolation "

         "across a season invents a shape the data does not support. Edge gaps are never filled, "

         "because there is no second anchor.", space_after=4)



    table(doc,

          ["Gap", "Length", "Method", "Justification"],

          [

              ("Internal, short", "1–3 months", "Linear interpolation in time", "Neighbours bound the value; seasonal shape is preserved locally"),

              ("Internal, long", "> 3 months", "Leave missing; flag", "Interpolation would cross a season and smooth away the signal"),

              ("Leading or trailing", "Any", "Leave missing; flag", "One-sided anchor; extrapolation is not imputation"),

              ("Structural", "Any", "Leave missing; calendar feature", "The absence is the fact"),

              ("Target variable", "Any", "Never impute", "Imputing the target trains the model on invented outcomes"),

          ],

          [4.0, 2.0, 4.6, 6.0], size=8.1, first_col_bold=True,

          caption_text="Gap treatment by length and position. The three-month limit is a parameter, not a universal law; Appendix F explains how to reset it for weekly or daily data.")



    para(doc,

         f"On MYP-26, {PM['imputed_cells']} cells were imputed ({pct(PM['imputation_share'])} of the "

         f"panel), all from internal gaps of three months or less. {PM['market_closed_cells']} zero "

         f"prices and {PM['invalid_cells']} invalid values were classified as structural or invalid and "

         "left missing. No long gap was interpolated. The imputation share is published because a "

         "clean table with a high imputation share is a partly synthetic table, and the reader is "

         "entitled to know that before trusting a forecast.")



    callout(doc, "Why not mean-impute and move on",

            "Mean imputation preserves the sample mean and destroys the variance, the covariance with "

            "every other variable, and the time structure. In a price panel it also erases seasonality "

            "by replacing a December onion price with an annual average. It is fast, and it is the "

            "single most common way a clean-looking panel becomes an uninformative one.",

            space_after=8)



    h2(doc, "5.9  S7 — Outliers")

    para(doc,

         "Outlier detection runs on the log of the price, within each crop–state series, using a "

         "modified z-score built on the median absolute deviation. The log makes a doubling and a "

         "halving symmetric; the median and MAD make the threshold resistant to the very values being "

         "tested. A conventional mean and standard deviation would be pulled toward a large error and "

         "could fail to flag it.")

    code_block(doc, [

        "log_price = np.log(price[price > 0])",

        "med  = np.median(log_price)",

        "mad  = np.median(np.abs(log_price - med))",

        "scale = 1.4826 * mad",

        "z = 0.6745 * (log_price - med) / scale",

        "flag = abs(z) > 3.0",

    ], size=8.2)



    para(doc,

         "The threshold of 3.0 is a screening parameter, not a verdict. Three outcomes follow.",

         space_after=4)

    bullet(doc, "a ratio to the series median near a power of ten, or a ratio near 0.01, identifies a "

                "mechanical cause. The value is corrected by the unit rule and the correction is "

                "logged. This is the only case in which an outlier is overwritten.",

           lead="Mechanical error — correct — ")

    bullet(doc, "a large deviation that is corroborated by neighbouring months, by another market, or "

                "by a documented event is retained and flagged as a genuine spike. Deleting it would "

                "delete the scarcity signal the model is meant to learn.",

           lead="Genuine event — retain and flag — ")

    bullet(doc, "a large deviation with no corroboration and no mechanical cause is flagged and "

                "excluded from model training, but left visible in the clean table. It is not "

                "winsorised by default, because replacing it with a percentile invents a value and "

                "hides the uncertainty.", lead="Unexplained — flag and exclude — ")



    para(doc,

         f"The reference run flagged {PM['genuine_spikes']} genuine event and "

         f"{PM['outliers_flagged']} unexplained values, and rejected {PM['implausible']} values "

         "outside the plausible band. Five of the seven planted digit errors were therefore caught — "

         "three as unexplained outliers and two as implausible — and two stayed inside the robust "

         "band. That residual is not a bug to hide: it is the measured limit of a univariate screen "

         "on a seasonal series, and §6.2 extends the screen with a seasonal-residual test for exactly "

         "this reason.",

         size=9.5, italic=True, color="5C6B62")



    para(doc,

         "Output: a clean price table where every value is either observed, mechanically corrected, "

         "imputed under the bound, or flagged. Gate: every flag has a rule, a reason and a review "

         "status; no value is both flagged and silently used in training.",

         size=9.5, italic=True, color="5C6B62")



    h2(doc, "5.10  S8 — Reconcile sources and vintages")

    para(doc,

         "Two sources rarely agree exactly, and a third usually disagrees with both. The strategy does "

         "not average disagreement away. It applies a documented precedence order, records the "

         "difference, and investigates anything above a tolerance.", space_after=4)

    bullet(doc, "official statistics over trade estimates for production; the designated price series "

                "over a secondary aggregator for price. Precedence is set per indicator in the source "

                "register, not chosen per row.", lead="Precedence by indicator — ")

    bullet(doc, "a relative difference above 5% between overlapping sources is investigated and "

                "explained. Below 5%, the higher-precedence source is used and the difference is "

                "recorded. Above 5%, the series is flagged until the cause is known.",

           lead="Tolerance — ")

    bullet(doc, "every release is kept with its vintage_id. A fact is retrieved as of the vintage "

                "that was available at the forecast origin, using an as-of join. The latest value is "

                "never substituted into a historical row.", lead="Point-in-time — ")

    bullet(doc, "suppressed values are retained as null and flagged. They are not inferred from "

                "neighbouring cells, because the suppression exists to prevent exactly that "

                "inference.", lead="Suppression — ")



    para(doc,

         f"The yield panel carries {YM['vintages']} release identifiers across 2020–2025, with 2024 "

         f"and 2025 having three releases each. The point-in-time view selects "

         f"{PM['pit_rows']} rows — one per crop, state and year — using the vintage available at the "

         "time. Training on the latest revised series and backtesting against it would be a "

         "look-ahead error even though every individual number is correct.",

         size=9.5, italic=True, color="5C6B62")



    h2(doc, "5.11  S9 — Validate and freeze")

    para(doc,

         "The final step is a gate, not a formality. The suite is run, the scorecard is regenerated, "

         "the outputs are hashed, and the clean layer is frozen. If any gate fails, the scope is "

         "narrowed or the series is dropped; the build does not proceed on a failed gate.")

    table(doc,

          ["Check", "Acceptance", "Measured on MYP-26"],

          [

              ("Completeness", "â‰¥ 98% of must-have price cells", pct(PM["completeness_after"])),

              ("Duplicate keys", "0", f"{PM['duplicate_rate_after'] * 100:.0f}"),

              ("Date conformance", "100% ISO", "100%"),

              ("Entity conformance", "100% mapped to a master", "100%"),

              ("Imputation share", "< 5% of price cells", pct(PM["imputation_share"])),

              ("Yield derivability", "100% of yield rows recomputable from production and area", "100%"),

              ("Determinism", "Clean clone reproduces the panel hash", "verified in §9.5"),

          ],

          [4.4, 8.4, 3.8], size=8.2, first_col_bold=True,

          caption_text="The seven-check acceptance suite. All checks pass on the reference run.")



    para(doc,

         "Output: a frozen clean layer, a cleaning log, a scorecard and an updated data dictionary. "

         "Gate G4: the suite passes, the log is complete, and a second run from the raw snapshot "

         "produces an identical hash.", size=9.5, italic=True, color="5C6B62")



    para(doc,

         "One deliberate omission: there is no step for 'manual correction'. If a value needs a human "

         "decision, the decision is captured as a parameter of a rule or as an entry in a review "

         "queue, not typed into the table. That is what keeps the process reproducible when the person "

         "who made the decision is no longer on the project.")











