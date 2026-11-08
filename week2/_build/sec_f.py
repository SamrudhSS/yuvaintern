# -*- coding: utf-8 -*-
"""Appendices A-H."""

from docbase import h1, h2, h3, para, bullet, table, code_block, callout
from facts import PM, YM, LOG, SCORE, pct, num


def appendix_a(doc):
    h1(doc, "Appendix A.  Cleaning-Log Schema", page_break=True)

    para(doc,
         "The cleaning log is the audit trail and a first-class deliverable. It is append-only, one "
         "row per changed, imputed, flagged or dropped value, and it joins back to the clean table on "
         "row_id and to the rule register on rule_id.")

    table(doc,
          ["Field", "Type", "Example", "Notes"],
          [
              ("step", "enum", "S6", "Pipeline step that made the change"),
              ("rule_id", "text", "R08", "Foreign key to the rule register (Appendix C)"),
              ("table", "enum", "prices", "prices, yields or a derived table"),
              ("row_id", "text", "P02799", "Stable identifier from the raw load"),
              ("field", "text", "modal_price_inr_quintal", "The column changed"),
              ("old_value", "text", "91.579", "Raw value; empty when the cell was null"),
              ("new_value", "text", "9157.9", "Clean value; empty for drops and flags"),
              ("action", "enum", "corrected", "corrected, imputed, harmonised, parsed, flagged, dropped, nulled, derived, left_missing"),
              ("reason", "text", "unit drift: INR/kg -> INR/quintal (x100)", "Human-readable cause, not a code"),
              ("run_id", "text", "2026-11-04T09:15Z-7f3a", "Ties the row to a pipeline run"),
          ],
          [2.2, 2.0, 5.6, 7.4], size=7.9, first_col_bold=True,
          caption_text="Cleaning-log schema. The reason field is prose so that a reviewer does not have to decode an enum.")

    para(doc, "An extract from the reference run, with three different actions:", space_after=4)
    code_block(doc, [
        "step rule  row_id   field              old_value    new_value   action",
        "S4   R06   P02786   modal_price        91.579       9157.9      corrected",
        "S6   R08   P02799   modal_price                     8758.84     imputed",
        "S7   R07   P00530   modal_price        4066.53      4066.53     flagged",
        "",
        "reason (third row): genuine spike corroborated by neighbours; retained",
    ], size=7.4)

    para(doc,
         f"The full log for MYP-26 has {num(LOG['rows'])} rows. It is small enough to review and "
         "large enough to answer the question every reviewer eventually asks: what did you change, and "
         "why?")


def appendix_b(doc):
    h1(doc, "Appendix B.  Quality Flags and Dictionary Extension")

    para(doc,
         "Every fact row carries a quality_flag. The flag is never null, and it is the single field "
         "that determines whether a value enters a model. The vocabulary is closed; a new flag is a "
         "schema change, not a free-text annotation.")

    table(doc,
          ["Flag", "Meaning", "In the clean table", "Used in models?"],
          [
              ("ok", "Observed and valid", "Value present", "Yes"),
              ("imputed_short_gap", "Interpolated across ≤3 months", "Value present", "Yes, with sensitivity run"),
              ("imputed_bounded", "Imputed with an explicit domain bound", "Value present", "Yes, with sensitivity run"),
              ("market_closed", "Zero price reclassified as no trade", "Null", "No; calendar feature instead"),
              ("invalid", "Negative or impossible value", "Null", "No"),
              ("missing_long_gap", "Gap > 3 months", "Null", "No"),
              ("suppressed", "Withheld by the publisher", "Null", "No; never inferred"),
              ("outlier_unresolved", "Robust outlier without corroboration", "Value present", "No"),
              ("spike_genuine", "Corroborated genuine event", "Value present", "Yes"),
              ("implausible", "Outside the physical domain after repair", "Value present", "No"),
              ("provisional", "Advance estimate; later releases expected", "Value present", "Only in point-in-time use"),
              ("discontinued", "Series ended; no current observation", "Historical values only", "No"),
          ],
          [3.4, 6.0, 3.4, 4.4], size=7.9, first_col_bold=True,
          caption_text="The closed flag vocabulary. The model-inclusion column is the operational meaning of each flag.")

    para(doc,
         "The data dictionary is extended with five fields beyond the Week 1 specification: "
         "quality_flag, outlier_z, vintage_id, available_at and rule_version. The first two "
         "describe the value; the next two describe when it was knowable; the last describes the rule "
         "that produced it. Together they make every row self-describing. The extension is reproduced "
         "below so that the Week 1 dictionary and the implementation cannot drift apart.",
         space_after=4)

    table(doc,
          ["Field", "Type", "Unit", "Definition", "Available when"],
          [
              ("modal_price_inr_quintal", "float", "INR / quintal", "State modal wholesale price, canonical unit", "Source publication"),
              ("price_real_inr_quintal", "float", "INR 2011-12", "Modal price deflated by CPI-IW", "Deflator release"),
              ("log_price", "float", "log INR", "Natural log of the real price", "Derived"),
              ("arrival_tonnes", "float", "tonnes", "Market arrivals, aggregated to state-month", "Source publication"),
              ("production_kt", "float", "'000 tonnes", "Production estimate for the crop year", "Vintage release"),
              ("area_kha", "float", "'000 hectares", "Area sown or harvested", "Vintage release"),
              ("yield_t_ha", "float", "t / ha", "Production ÷ area, ratio of sums", "Derived at vintage"),
              ("yield_trend_dev", "float", "% of trend", "Deviation from a five-year local trend", "Needs five prior years"),
              ("rainfall_anomaly_mm", "float", "mm", "Departure from the 30-year local normal", "Meteorological release"),
              ("gdd_c", "float", "°C days", "Growing-degree days above the crop base", "Daily weather, lagged"),
              ("crop_year", "text", "label", "Growing and marketing year (e.g. 2024-25)", "Derived from period"),
              ("vintage_id", "date", "ISO date", "Publication date of the release used", "At load"),
              ("available_at", "timestamp", "UTC", "Earliest moment the value was knowable", "At load"),
              ("quality_flag", "enum", "—", "Closed-vocabulary status controlling model inclusion", "At clean"),
              ("outlier_z", "float", "score", "Modified z on log price within crop-state", "At clean"),
              ("rule_version", "text", "semver", "Version of the rule that produced the row", "At clean"),
          ],
          [4.2, 1.8, 2.8, 5.4, 3.4], size=7.7, first_col_bold=True,
          caption_text="Dictionary extension. The availability column is the field that prevents leakage when the indicator is used as a feature.")


def appendix_c(doc):
    h1(doc, "Appendix C.  Rule Register", page_break=True)

    para(doc,
         "The register is the contract between the strategy and the code. Each rule has an identifier, "
         "a parameter, a test and a record of whether it fired on the reference panel. A rule that "
         "does not fire is still tested; absence of the defect is not absence of the rule.")

    table(doc,
          ["ID", "Rule", "Key parameters", "Test", "Fired"],
          [
              ("R01", "Schema and domain validation", "Price > 0; production ≥ 0; area > 0", "Invalid values are nulled, never clipped", "47"),
              ("R02", "Duplicate resolution", "Key = crop + state + period; survivorship order", "Zero duplicate keys after the step", "79"),
              ("R03", "Entity canonicalisation", "Crop, state, district and mandi maps", "Zero unmapped entities", "67"),
              ("R04", "Date parsing", "ISO, DD/MM/YYYY, Mon-YYYY; day-first convention", "Zero unparsed dates; no ambiguous date guessed", "117"),
              ("R05", "Calendar derivation", "Crop, fiscal and marketing year definitions", "Every row has all three years", "by design"),
              ("R06", "Unit and scale repair", "Ratio bands 0.004–0.025, 0.05–0.2, 5–20", "Corrected values inside the plausible band", "62"),
              ("R07", "Robust outlier flagging", "Log price; MAD; |z| > 3.0; neighbour corroboration", "Every flag has a reason and a review status", "6"),
              ("R08", "Missing classification and bounded imputation", "≤3 months; internal only; three bounds", "No imputed target, suppression or long gap", "160"),
              ("R09", "Ratio-of-sums aggregation", "Σproduction ÷ Σarea", "State yield equals total ÷ total, not mean of ratios", "by design"),
              ("R10", "Derived-quantity unit repair", "Yield > 8× or < 0.55× crop median", "Repaired yield inside the crop range", "10"),
              ("R11", "Vintage separation", "One row per release; available_at", "No release overwritten", "by design"),
              ("R12", "Source reconciliation", "Precedence per indicator; 5% tolerance", "Disagreements recorded, never averaged", "by design"),
              ("R13", "Suppression handling", "Flag only; no inference", "No suppressed cell has a value", "not triggered"),
              ("R14", "Plausibility bounds", "400–20,000 INR/quintal; crop yield ranges", "No unflagged impossible value", "2"),
              ("R15", "As-of join", "available_at <= origin_date", "No feature timestamp after its origin", "by design"),
              ("R16", "Fold-local scaling", "Fit on train only; robust where outliers retained", "Scaler statistics differ by fold", "by design"),
              ("R17", "Fold-local encoding", "One-hot ≤10 levels; target encoding above", "No global target encoding", "by design"),
              ("R18", "Output contract", "Schema, units, hash, dictionary version", "Contract test passes before release", "by design"),
          ],
          [1.2, 4.2, 5.4, 5.0, 1.6], size=7.6, first_col_bold=True,
          caption_text="The rule register. ‘Fired’ is the number of log rows on MYP-26; ‘by design’ rules are structural and are tested rather than counted.")

    para(doc,
         "The parameters are deliberately separated from the rules. A weekly panel changes the "
         "three-month gap bound to seven days without changing the logic of R08; a new crop changes "
         "the plausible band without changing R14. That separation is what makes the register "
         "reusable across Weeks 3–5 and across datasets.")


def appendix_d(doc):
    h1(doc, "Appendix D.  Reproducibility Checklist")

    para(doc, "Run this list before any handover. Each item is binary; there is no partial credit.",
         space_after=4)

    table(doc,
          ["#", "Check", "Evidence"],
          [
              ("1", "Raw snapshots are immutable and hash-recorded", "Manifest with SHA-256 per file"),
              ("2", "Every raw file has a source, licence and retrieval time", "Manifest row completeness = 100%"),
              ("3", "Environment is pinned", "requirements.lock; Python version recorded"),
              ("4", "All stochastic steps have a sealed seed", "Seed in config and manifest"),
              ("5", "Every rule is a function with a unit test", "Test suite passes"),
              ("6", "Every changed value is in the cleaning log", "Log count reconciliation"),
              ("7", "Rules are versioned with a changelog", "Semver and scorecard diff"),
              ("8", "Every artefact carries a run_id", "Artefact headers and filenames"),
              ("9", "A clean clone reproduces the panel hash", "Hash comparison, not a visual check"),
              ("10", "A negative control fails as expected", "Perturbed input trips the suite"),
              ("11", "The data dictionary matches the schema", "Dictionary validation test"),
              ("12", "The README runs end to end in ≤10 minutes", "Timed on a clean machine"),
          ],
          [0.9, 9.4, 6.4], size=8.1, first_col_bold=True,
          caption_text="Twelve checks. Items 9 and 10 are the ones most often skipped and most informative.")

    callout(doc, "The ten-minute test",
            "Hand the repository to a colleague who has not seen it, with no verbal instructions. If "
            "they cannot reproduce the panel in ten minutes, the documentation is part of the bug.",
            space_after=4)


def appendix_e(doc):
    h1(doc, "Appendix E.  Glossary")

    terms = [
        ("As-of join", "A join that selects the version of a fact knowable at a given date, not the latest version."),
        ("Business key", "The columns that uniquely identify a fact: crop, state and period for a monthly price."),
        ("Cleaning log", "The append-only record of every changed, imputed, flagged or dropped value."),
        ("Crop year", "The year of the growing and marketing cycle, which may not align with the calendar year."),
        ("Defect register", "The prioritised list of data problems found in profiling, with a rule and an owner."),
        ("Imputation", "Replacing a missing value with an estimate, with a flag and a stated bound."),
        ("LGD code", "Local Government Directory code; the stable identifier for Indian states and districts."),
        ("MAD", "Median absolute deviation; a robust measure of spread used in the modified z-score."),
        ("Mandi", "A regulated wholesale market for agricultural produce."),
        ("MAR / MCAR / MNAR", "Missingness mechanisms: at random, completely at random, and not at random."),
        ("Point-in-time", "A view that uses only information available at the forecast origin."),
        ("Quality flag", "The closed-vocabulary status attached to every fact row, controlling model inclusion."),
        ("Ratio of sums", "An aggregate computed as Σnumerator ÷ Σdenominator, not as a mean of ratios."),
        ("Survivorship rule", "The deterministic rule that decides which duplicate row is kept."),
        ("Vintage", "A specific release of a series, identified by its publication date."),
        ("Winsorising", "Replacing extreme values with a percentile; deliberately not used for prices here."),
        ("Quarterly / monthly modal price", "The most frequently occurring price in a period, as reported by a market."),
        ("Leakage", "Use of information in training that would not have been available at prediction time."),
    ]
    table(doc, ["Term", "Definition"], terms, [4.6, 12.0], size=8.4, first_col_bold=True,
          caption_text="Terms as they are used in this document, not as they might be used elsewhere.")


def appendix_f(doc):
    h1(doc, "Appendix F.  Assumptions, Limitations and Brief Compliance", page_break=True)

    h2(doc, "F.1  Assumptions")
    bullet(doc, "the source register and the four masters exist before cleaning begins. This document "
                "specifies them but does not build them.", lead="A1 — ")
    bullet(doc, "a monthly grain is sufficient for the price analysis; daily quotes are aggregated "
                "upstream with the same rules.", lead="A2 — ")
    bullet(doc, "the CPI deflator and the RBI reference rate are available for every period in scope.",
           lead="A3 — ")
    bullet(doc, "the plausible price and yield bands in Appendix C are wide enough to absorb normal "
                "seasonal and regional variation. They are parameters, not constants.", lead="A4 — ")

    h2(doc, "F.2  Limitations")
    para(doc,
         "Three limitations should be stated before the strategy is applied to real data. First, the "
         "three-month imputation bound is calibrated for monthly data and must be reset for weekly or "
         "daily series; applied unchanged to daily quotes it would interpolate across a quarter and "
         "smooth away exactly the variation of interest. Second, the univariate outlier screen has "
         "limited power on strongly seasonal series: two of seven planted digit errors survived it in "
         "the reference run, which is why the contextual screen is specified rather than optional. "
         "Third, the strategy cannot recover a value that is missing because the publisher suppressed "
         "it, and it should not try; the correct output is a flag and a coverage gap, not an estimate.")
    para(doc,
         "A fourth limitation is organisational rather than statistical. The controls only work if the "
         "project treats the rule register as a contract. A team that edits the clean table directly "
         "can satisfy every test in this document and still produce an unauditable result.")

    h2(doc, "F.3  Compliance with the brief")
    table(doc,
          ["Requirement", "Where it is addressed", "Evidence"],
          [
              ("Introduction to common agribusiness data-quality issues", "Section 3", "Eight defect classes; six structural causes; impact analysis"),
              ("Missing values, inconsistent formats and outliers", "Sections 3, 5, 6", "Taxonomy, validation, robust screens, worked cases"),
              ("Specific methods — imputation, normalisation, filtering", "Section 6, 7", "Seven-method comparison; transformation table; bounds"),
              ("Step-by-step cleaning plan", "Section 5", "S0–S9 with decision rules, outputs and gates"),
              ("Proposed preprocessing framework", "Section 7", "Five layers, contracts, leakage tests"),
              ("Workflow diagram or list", "Section 8", "Diagram plus a seventeen-step executable sequence"),
              ("Importance of reproducibility", "Section 9", "Ten controls, manifest, determinism test, clean-clone gate"),
              ("Hypothetical examples (bonus)", "Section 10", "Six cases extracted from a seeded reference run"),
          ],
          [6.4, 4.4, 5.8], size=8.0, first_col_bold=True,
          caption_text="How each element of the brief maps to the document.")


def appendix_g(doc):
    h1(doc, "Appendix G.  Statistical Notes")

    para(doc,
         "These notes give the derivations behind the methods in Section 6. They are written for a "
         "reader who wants to check the reasoning or adapt the parameters, not as a statistics primer.")

    h3(doc, "G.1  Modified z-score and the MAD")
    para(doc,
         "For observations x₁…xₙ, let m = median(x) and MAD = median(|xᵢ − m|). The modified z-score is",
         space_after=2)
    code_block(doc, ["zᵢ = 0.6745 × (xᵢ − m) / MAD"], size=9.0, space_after=6)
    para(doc,
         "The constant 0.6745 makes the scale comparable to a standard deviation under normality, "
         "because for a normal distribution MAD ≈ 0.6745σ. The influence function of the median and "
         "the MAD is bounded: a single value can move the estimate only slightly, which is why the "
         "screen does not mask the very outlier it is testing. With a mean and standard deviation, one "
         "large error inflates σ and can push its own z-score below the threshold.")
    para(doc,
         "The price screen applies the statistic to log price. If p is log-normal, log p is normal, so "
         "the threshold has a stable interpretation across crops whose price levels differ by an order "
         "of magnitude. On the raw scale, a ₹500 deviation is large for onion and trivial for cotton; "
         "on the log scale, the same proportional deviation has the same score.")

    h3(doc, "G.2  IQR fences")
    para(doc,
         "The distributional cross-check uses Q1 and Q3 and the fences Q1 − 1.5·IQR and Q3 + 1.5·IQR, "
         "with 3·IQR as the extreme fence. The fences make no distributional assumption, which is "
         "their advantage and their weakness: on a seasonal series the interquartile range is wide, so "
         "the fences are wide, and a moderate error can sit comfortably inside them. The IQR is a "
         "cross-check, not the decision rule.")

    h3(doc, "G.3  Interpolation and its error")
    para(doc,
         "Linear interpolation between anchors (t₀, y₀) and (t₁, y₁) gives, for t between them,")
    code_block(doc, ["ŷ(t) = y₀ + (y₁ − y₀) × (t − t₀) / (t₁ − t₀)"], size=9.0, space_after=6)
    para(doc,
         "Time-weighted interpolation uses the actual elapsed time, not the row index; the reference "
         "run's imputed March value is not the arithmetic midpoint because February to April spans "
         "different month lengths. The interpolation error is bounded by the curvature of the series "
         "over the gap: if the second derivative is bounded by M, the error is at most M·h²/8 for a gap "
         "of length h. That bound is why the rule limits the gap to three months: the error grows with "
         "the square of the gap, so a six-month gap is four times as uncertain as a three-month one.")
    para(doc,
         "Interpolation assumes the series is smooth across the gap. If a policy announcement, a "
         "festival or a market closure falls inside it, the assumption fails and no amount of "
         "neighbour information can recover the shape. The flag makes the assumption visible; the "
         "sensitivity analysis measures its effect.")

    h3(doc, "G.4  MICE, in one paragraph")
    para(doc,
         "Multiple Imputation by Chained Equations fits a conditional model for each variable with "
         "missing data, using the other variables as predictors, and iterates until the imputations "
         "stabilise. It preserves cross-variable structure that interpolation ignores, and it produces "
         "multiple completed datasets whose variation reflects imputation uncertainty. It is the right "
         "tool when many indicators are correlated and the missingness is MAR. It is the wrong tool "
         "for a short gap in a single series, where it adds model dependence and runtime without "
         "adding information, and it is not a substitute for classifying the cause of the gap.")

    h3(doc, "G.5  Variance-stabilising transforms")
    para(doc,
         "The Box-Cox family maps a positive variable to y(λ) = (x^λ − 1)/λ for λ ≠ 0 and log x for "
         "λ = 0. The Yeo-Johnson extension handles zero and negative values. For prices the log "
         "(λ = 0) is the default because it has a direct interpretation as a proportional change and "
         "because the series is strictly positive after validation. The transformation is applied "
         "before outlier screening and before modelling, and it is inverted before any result is "
         "reported in rupees.")

    h3(doc, "G.6  STL residuals")
    para(doc,
         "STL decomposes a series into trend, seasonal and remainder components by local regression. "
         "The remainder is the part not explained by level or season, and it is the natural input to a "
         "contextual outlier screen: a value is surprising if its remainder is extreme, not if its "
         "level is. STL requires at least two full seasonal cycles, which is why it is a second-pass "
         "screen on the longer series rather than a first-pass rule on every crop–state pair.")

    h3(doc, "G.7  Mahalanobis distance and isolation forests")
    para(doc,
         "The Mahalanobis distance d² = (x − μ)ᵀ Σ⁻¹ (x − μ) measures how far a multivariate "
         "observation is from the centre, accounting for covariance. It is powerful when indicators "
         "are correlated (price, arrivals, rainfall) and misleading when Σ is estimated from the same "
         "contaminated sample. An isolation forest isolates observations by random partitioning and "
         "scores them by how quickly they separate; it scales well and makes few assumptions, but its "
         "output is a score, not a cause. Neither method replaces the corroboration test: a "
         "multivariate flag still needs an explanation before a value is excluded.")

    h3(doc, "G.8  Why a ratio of sums")
    para(doc,
         "Let districts i have production Pᵢ and area Aᵢ. The state yield is ΣPᵢ / ΣAᵢ. The mean of "
         "district yields is (1/n)·Σ(Pᵢ/Aᵢ), which weights a small district equally with a large one. "
         "The two coincide only when all areas are equal. Since area shares are highly unequal, the "
         "mean of ratios is biased toward the yields of small districts, and the bias does not vanish "
         "as n grows. The ratio of sums is the only aggregate that preserves the physical identity "
         "production = yield × area.")


def appendix_h(doc):
    h1(doc, "Appendix H.  Test Catalogue", page_break=True)

    para(doc,
         "The tests below run in CI on every build. A failing test blocks the release; a warning is "
         "not a control. The catalogue is deliberately short enough to be read in one sitting.")

    table(doc,
          ["ID", "Test", "Assertion", "Failure means"],
          [
              ("T01", "Manifest integrity", "Every raw file has a row and a matching SHA-256", "The evidence base is incomplete"),
              ("T02", "Key uniqueness", "Zero duplicate business keys in L2", "Deduplication failed or the key is wrong"),
              ("T03", "Completeness", "Usable price cells ÷ grid ≥ 98%", "A series has a coverage gap"),
              ("T04", "Type and domain", "No invalid value without a flag", "Validation was bypassed"),
              ("T05", "Entity conformance", "100% of rows map to a master", "A new alias was introduced"),
              ("T06", "Date conformance", "100% ISO month starts", "A parser silently failed"),
              ("T07", "Imputation bounds", "No imputed target, suppression or long gap", "R08 was applied outside its scope"),
              ("T08", "Flag completeness", "No null flag; no unknown flag", "A new state was introduced without a schema change"),
              ("T09", "Log reconciliation", "Changed cells = log rows for changes", "A change was made outside the rules"),
              ("T10", "Point-in-time", "No feature available_at after origin", "Vintage leakage"),
              ("T11", "Fold-local transforms", "Scaler and encoder statistics differ by fold", "Global fitting leaked the test period"),
              ("T12", "Target isolation", "No feature is a deterministic function of the target", "Target leakage"),
              ("T13", "Determinism", "Two runs produce identical hashes", "A hidden source of randomness or state"),
              ("T14", "Negative control", "Perturbed input fails the suite", "The tests are not testing"),
              ("T15", "Contract", "Schema, units and hash match the declaration", "The matrix is not the one that was signed"),
          ],
          [1.2, 4.2, 7.4, 6.0], size=7.8, first_col_bold=True,
          caption_text="Fifteen tests. T14 is the one that keeps the other fourteen honest.")
