# -*- coding: utf-8 -*-
"""Sections 7-9: preprocessing framework, workflow, reproducibility."""

from docbase import (h1, h2, h3, para, bullet, table, callout, code_block,
                     figure, spacer)
from facts import SCORE, PM, YM, LOG, PANEL, EX, pct, num

HASH = __import__("facts").FACTS["hashes"]


def section_7(doc):
    h1(doc, "7.  Preprocessing Framework", page_break=True)

    para(doc,
         "Cleaning produces a table that is correct about the past. Preprocessing produces a matrix "
         "that is usable for prediction, and the two are not the same artefact. The framework below "
         "separates them into layers with explicit contracts, so that a transformation cannot leak "
         "future information into a training row without a test failing.")

    h2(doc, "7.1  Five layers")
    table(doc,
          ["Layer", "Contents", "Contract", "Gate"],
          [
              ("L0 Raw", "Immutable snapshots and manifest", "Byte-identical to retrieval; hash recorded", "Manifest hash matches"),
              ("L1 Validated", "Typed, parsed, schema-conformant rows", "Every value has a type and a domain check", "Zero unexplained parse failures"),
              ("L2 Clean", "Harmonised, deduplicated, repaired, flagged", "Every intervention logged; every null classified", "Quality scorecard passes"),
              ("L3 Panel", "Analysis grain with derived indicators and vintages", "One row per crop-state-period; as-of joins only", "No feature timestamp after its origin"),
              ("L4 Matrix", "Encoded, scaled, split-ready numeric matrix", "Fit on training folds only; schema fixed", "Leakage and contract tests pass"),
          ],
          [2.4, 5.6, 6.2, 3.6], size=8.1, first_col_bold=True,
          caption_text="The five layers. Each layer has one job and one gate; a layer never reaches back to repair an earlier one.")

    para(doc,
         "The layering is not architectural decoration. It fixes where a decision is allowed to "
         "happen. A unit conversion belongs in L2 and must never appear in an L4 feature transform, "
         "because an L4 transform is fitted on training data and a unit is a fact about the world. "
         "Conversely, a scaler belongs in L4 and must never be applied in L2, because it would be "
         "fitted once on the whole panel and leak the test period into training.")

    h2(doc, "7.2  Framework components")
    table(doc,
          ["Component", "Responsibility", "Artefact"],
          [
              ("Configuration", "Declares grain, units, canonical names, thresholds and rule versions", "config.yaml, validated on load"),
              ("Rule registry", "Maps every rule identifier to a function, parameters and a test", "rules.py + test_rules.py"),
              ("Transform registry", "Declares each derived indicator with its formula, inputs and availability rule", "indicators.yaml"),
              ("Quality monitor", "Computes the scorecard before and after each run", "scorecard.json + trend table"),
              ("Provenance store", "Records source, vintage and retrieval time for every fact", "Columns on every table, not a side file"),
              ("Contract tests", "Asserts schema, dtypes, ranges, uniqueness and leakage rules", "test_contract.py, run in CI"),
          ],
          [3.4, 9.0, 5.4], size=8.1, first_col_bold=True,
          caption_text="Framework components. Each has an artefact that can be reviewed without reading the pipeline code.")

    para(doc,
         "The transform registry is the part that pays for itself. Each indicator is declared once, "
         "with its formula and the rule that determines when it is available. The feature builder "
         "reads the registry rather than hard-coding columns, so a new indicator cannot be added "
         "without also declaring its availability. That single constraint prevents most leakage.")

    h2(doc, "7.3  Transformation decisions by variable type")
    table(doc,
          ["Variable", "Options", "Chosen for MYP-26", "Reason"],
          [
              ("Price level", "Level, log, real, differenced, seasonal difference", "Real log price, plus 12-month log difference", "Stabilises variance; separates inflation from relative price; stationarity"),
              ("Yield", "Level, log, trend deviation, growth", "Level and deviation from a five-year local trend", "Annual series is short; differencing throws away the level information"),
              ("Production / area", "Level, log, share, growth", "Log level for production; share of state area", "Multiplicative scale; share is comparable across states"),
              ("Weather", "Raw, anomaly, z-score, GDD, SPI", "Anomaly from a 30-year local normal, plus GDD", "A 32 °C day means different things in Punjab and Karnataka"),
              ("Categorical", "One-hot, ordinal, target encoding", "One-hot for ≤10 levels; target encoding inside folds above that", "Cardinality control without leakage"),
              ("Counts", "Raw, log1p, rate", "log1p", "Heavy right tail; zeros retained"),
              ("Calendar", "Month dummies, Fourier terms, holiday flags", "Fourier terms plus festival and harvest flags", "Smooth seasonality with explicit event effects"),
          ],
          [3.0, 5.0, 5.2, 5.2], size=7.9, first_col_bold=True,
          caption_text="Transformation decisions. The choice is stated with the reason, so a later reviewer can challenge the reason rather than reverse-engineer it.")

    para(doc,
         "Two decisions are worth defending. First, price is modelled in real terms with the CPI "
         "deflator, because nominal prices in India contain a trend that a model will happily learn as "
         "if it were a market signal. Second, yield is not differenced: with six annual observations "
         "per series, a difference consumes a third of the history and amplifies measurement error. A "
         "deviation from a local trend is the more efficient way to remove the trend without losing "
         "the level.")

    h2(doc, "7.4  Scaling, encoding and imbalance")
    para(doc,
         "Scaling is model-dependent, and applying it globally is the most common leakage bug in "
         "applied machine learning. The rules are simple and non-negotiable:", space_after=4)
    bullet(doc, "fit the scaler inside each cross-validation fold, on the training part only. A "
                "scaler fitted on the full panel has seen the test period's mean and variance.",
           lead="Fit inside the fold — ")
    bullet(doc, "tree-based models do not need scaling; regularised linear models, kNN and neural "
                "networks do. Scaling a tree model is harmless but adds a step that can leak.",
           lead="Scale only where it matters — ")
    bullet(doc, "use a robust scaler (median and IQR) when flagged outliers are retained, because a "
                "standard scaler is dominated by the values the strategy chose not to delete.",
           lead="Robust where outliers remain — ")
    bullet(doc, "one-hot encode low-cardinality categories; target-encode high-cardinality ones "
                "inside the training fold, with smoothing. Never encode on the full panel.",
           lead="Encode inside the fold — ")
    bullet(doc, "do not scale the target. A scaled target makes the error metric uninterpretable in "
                "the units the decision-maker uses.", lead="Leave the target alone — ")

    para(doc,
         "Class imbalance is a secondary concern for this project because the targets are continuous. "
         "It matters for the event indicators — drought, policy intervention, price spike — where the "
         "positive class is rare. The approach is to report precision, recall and the confusion matrix "
         "rather than accuracy, and to set the decision threshold from the cost of the two errors, not "
         "from 0.5.")

    h2(doc, "7.5  Leakage discipline")
    para(doc,
         "Leakage is not a single mistake; it is a family of them. The framework tests for five "
         "specific forms on every build.", space_after=4)
    table(doc,
          ["Leakage form", "How it happens", "Assertion"],
          [
              ("Temporal", "A feature uses a value published after the forecast origin", "max(available_at) <= origin_date for every feature row"),
              ("Revision", "The latest revised value is used in a historical row", "As-of join on available_at; no un-vintaged reads"),
              ("Transform", "A scaler, encoder or imputer is fitted on the full panel", "Fit only on the training fold; transform the rest"),
              ("Target", "A feature is mechanically derived from the target", "Registry review; correlation and formula audit"),
              ("Split", "Random split of a time series", "Split by origin; rolling-origin evaluation only"),
          ],
          [3.2, 7.4, 5.6], size=8.1, first_col_bold=True,
          caption_text="Five leakage forms and the assertion that blocks each. The tests run in CI, not in a notebook.")

    h2(doc, "7.6  Output contract")
    para(doc,
         "The matrix handed to the model is a deliverable with a contract. It declares the grain, the "
         "row count, the column list with dtypes and units, the vintage rule, the missing-value policy "
         "and the hash of the clean layer it was built from. A model that receives a matrix without "
         "this contract cannot be reproduced, and a result from it cannot be defended.", space_after=4)

    code_block(doc, [
        "grain:        crop_code x state_lgd x period",
        "rows:         3,456",
        "target:       log_real_modal_price, horizon h in {1, 3, 6, 12}",
        "features:     30 declared in indicators.yaml, each with available_at",
        "missing:      imputed_short_gap allowed; structural and long gaps excluded",
        "scaling:      robust, fitted inside each rolling-origin fold",
        "source_hash:  " + HASH["prices_clean"][:16] + "...",
        "dictionary:   v1.0 (Appendix B and the project data dictionary)",
    ], size=8.2)


def section_8(doc):
    h1(doc, "8.  Workflow and Sequence", page_break=True)

    para(doc,
         "The diagram below is the whole strategy on one page. The cleaning lane is loss-aware and "
         "fully logged; the preprocessing lane is contract-driven. Seven gates sit between the stages, "
         "and the three controls below the lanes apply to every stage rather than to one.")

    figure(doc, "figures/workflow.png", width_cm=16.4,
           caption_text="The cleaning and preprocessing workflow. Gates G1–G4 govern the clean layer; G5–G7 govern the model-ready matrix.")

    para(doc,
         "A diagram is useful for orientation and useless for execution. The numbered sequence below "
         "is the executable form: seventeen steps in the order they run, each with its output.",
         space_after=4)

    h2(doc, "8.1  The seventeen-step sequence")
    table(doc,
          ["#", "Step", "Action", "Output"],
          [
              ("1", "S0", "Snapshot the source; record URL, time, rows, licence and SHA-256", "Immutable raw file + manifest row"),
              ("2", "S1", "Profile columns, check row absence against the expected grid, open the defect register", "Profile report + defect register"),
              ("3", "S2", "Validate types, domains, enums, cross-field logic and referential integrity", "Validated table + nulled invalid values"),
              ("4", "S3", "Resolve exact, key and near duplicates with the survivorship rule", "Unique business keys"),
              ("5", "S4", "Map crops, states, districts and mandis; convert units and currency", "Harmonised table"),
              ("6", "S5", "Parse dates to ISO; derive crop, fiscal and marketing years; attach the trading calendar", "Calendar-complete table"),
              ("7", "S6", "Classify every gap by cause; interpolate short internal gaps; leave the rest", "Clean price table with flags"),
              ("8", "S7", "Screen outliers on log price; corroborate or flag; correct only mechanical errors", "Outlier flags + corrections"),
              ("9", "S8", "Apply source precedence; keep every vintage; build as-of views", "Reconciled table + point-in-time view"),
              ("10", "S9", "Run the acceptance suite, publish the scorecard, hash and freeze", "Frozen clean layer"),
              ("11", "P0", "Declare transformations per variable, with formula and availability rule", "Transform registry"),
              ("12", "P1", "Derive indicators and lags; enforce the availability rule at creation", "Indicator panel"),
              ("13", "P2", "Aggregate with a ratio of sums; never a mean of ratios", "Analysis panel"),
              ("14", "P3", "Encode categorical variables inside the training fold", "Encoded features"),
              ("15", "P4", "Scale numeric features inside each fold, robustly where outliers remain", "Scaled features"),
              ("16", "P5", "Assemble the model matrix; attach the contract and the source hash", "Model-ready matrix"),
              ("17", "P6", "Run leakage, schema and reproducibility tests; fail the build on any breach", "Signed matrix + test report"),
          ],
          [0.9, 1.3, 9.4, 4.6], size=7.8, first_col_bold=True,
          caption_text="The executable sequence. Steps 1–10 are cleaning; 11–17 are preprocessing.")

    para(doc,
         "Two features of the sequence are easy to miss. Step 11 comes before any derivation, so the "
         "availability rule is declared rather than discovered. Step 17 can fail the build, which "
         "means the tests have authority; a test suite that only warns is a suggestion.",
         size=9.5, italic=True, color="5C6B62")

    h2(doc, "8.2  Time and ownership")
    table(doc,
          ["Stage", "Days", "Owner", "Reviewer"],
          [
              ("S0–S1 intake and profiling", "1.0", "Data engineer", "Analyst"),
              ("S2–S3 validation and deduplication", "0.5", "Data engineer", "Analyst"),
              ("S4–S5 harmonisation", "1.0", "Analyst", "Domain reviewer"),
              ("S6–S8 missing, outliers, reconciliation", "1.5", "Analyst", "Statistician"),
              ("S9 freeze and sign-off", "0.5", "Analyst", "Project lead"),
              ("P0–P6 preprocessing", "2.0", "Analyst", "Statistician"),
          ],
          [8.0, 1.6, 3.4, 3.2], size=8.2, first_col_bold=True,
          caption_text="Indicative effort for the first pass. The estimates assume the source register and masters already exist.")

    para(doc,
         "The effort concentrates in S6–S8, which is where judgement is required. That is also the "
         "part that is easiest to rush and hardest to audit later. The review pairing is deliberate: "
         "the person who writes the imputation rule should not be the only person who signs it off.")


def section_9(doc):
    h1(doc, "9.  Reproducibility")

    para(doc,
         "A cleaning decision that cannot be reproduced is an anecdote. Reproducibility is treated "
         "here as a set of mechanical controls, not as a virtue. Each control below prevents a "
         "specific failure, and each has a test that can be run without trusting the author.")

    h2(doc, "9.1  Ten controls")
    table(doc,
          ["#", "Control", "Failure it prevents", "Test"],
          [
              ("1", "Immutable raw snapshots", "A source is edited or silently refreshed", "SHA-256 matches the manifest"),
              ("2", "Manifest with provenance", "No one knows which pull produced a number", "Every raw file has a row"),
              ("3", "Pinned environment", "A library upgrade changes a result", "pip install -r requirements.lock in CI"),
              ("4", "Sealed seeds", "Stochastic steps differ between runs", "Two runs produce identical hashes"),
              ("5", "One function per rule", "A change in one place alters another", "Unit tests per rule identifier"),
              ("6", "Cleaning log", "The effect of cleaning is invisible", "Every changed cell has a log row"),
              ("7", "Rule versioning", "A rule changes without anyone noticing", "Semver + changelog + scorecard diff"),
              ("8", "Run identifiers", "Outputs from different runs are mixed", "Every artefact carries run_id"),
              ("9", "Clean-clone rebuild", "The pipeline only works on one machine", "A fresh clone reproduces the hash"),
              ("10", "Retention policy", "Old artefacts disappear or linger forever", "Dated snapshots; documented retention"),
          ],
          [0.9, 4.4, 6.0, 5.0], size=8.0, first_col_bold=True,
          caption_text="Ten reproducibility controls. Each is cheap; the absence of any one is expensive.")

    h2(doc, "9.2  The manifest")
    para(doc,
         "The manifest is the spine of the audit trail. It is append-only, one row per retrieval, and "
         "it is the only place where a raw file's identity is recorded.", space_after=4)

    code_block(doc, [
        "{",
        "  \"run_id\": \"2026-11-04T09:15:00Z-7f3a\",",
        "  \"source_id\": \"AGMARKNET\",",
        "  \"endpoint\": \"https://agmarknet.gov.in/...\",",
        "  \"retrieved_at\": \"2026-11-04T09:15:00Z\",",
        "  \"period_covered\": \"2020-01-01/2025-12-31\",",
        "  \"rows\": 3535,",
        "  \"sha256\": \"c0a070b878b301f5ca3ad37c402e7fb2...\",",
        "  \"licence\": \"Government Open Data Licence - India\",",
        "  \"status\": \"complete\",",
        "  \"notes\": \"monthly modal price, state level; units as published\"",
        "}",
    ], size=8.0)

    para(doc,
         "Two fields do the most work. sha256 makes the snapshot verifiable; retrieved_at makes it "
         "possible to reconstruct which version of a revised series was in hand at a given time. "
         "Without the second, a point-in-time backtest is impossible even with perfect code.")

    h2(doc, "9.3  Rule versioning")
    para(doc,
         "Rules change, and pretending otherwise produces a pipeline that is reproducible only by "
         "never improving it. The strategy versions rules with semantic versioning: a patch fixes an "
         "implementation without changing behaviour; a minor version adds a rule or a parameter; a "
         "major version changes an output. Every version carries a changelog entry and a scorecard "
         "diff against the previous run.", space_after=4)
    table(doc,
          ["Change", "Version bump", "Required evidence"],
          [
              ("Refactor, same output", "Patch", "Identical panel hash"),
              ("New threshold or new rule", "Minor", "Scorecard diff + review"),
              ("Output changes for existing cells", "Major", "Re-run, diff, re-sign-off, note in the release"),
          ],
          [6.0, 3.4, 6.8], size=8.1, first_col_bold=True,
          caption_text="Rule versioning. A major change is allowed; an unrecorded one is not.")

    h2(doc, "9.4  The determinism test")
    para(doc,
         "Determinism is tested, not asserted. The procedure is deliberately blunt: delete the "
         "generated layers, re-run from the frozen raw snapshot with the sealed seed, and compare "
         "hashes. Any difference is a failure, including a difference that looks harmless.",
         space_after=4)
    bullet(doc, "the clean price panel, the clean yield panel and the cleaning log are hashed after "
                "each run and compared with the previous run's values.", lead="Three hashes — ")
    bullet(doc, "the run is repeated in a fresh virtual environment built from the lock file, on a "
                "different working directory, to catch hidden absolute paths and local state.",
           lead="Fresh environment — ")
    bullet(doc, "a deliberately perturbed input is fed through the suite. The tests must fail. A test "
                "suite that passes on corrupted input is not testing anything.",
           lead="Negative control — ")

    para(doc,
         "For the reference run, the clean price panel hashes to "
         f"{HASH['prices_clean'][:16]}…, the yield panel to {HASH['yield_clean'][:16]}…, and the "
         f"cleaning log to {HASH['cleaning_log'][:16]}…. These are the values a second run must "
         "reproduce. They are quoted in the report so that a reviewer can check the claim rather than "
         "take it on trust.", size=9.5, italic=True, color="5C6B62")

    h2(doc, "9.5  The clean-clone gate")
    para(doc,
         "The final gate is the one that matters to a handover: a person who has never seen the "
         "project clones the repository, installs from the lock file, runs one command, and gets the "
         "same panel. If that takes more than ten minutes, or requires a conversation, the pipeline "
         "is not finished. The gate is stated as a test rather than a hope because it is the only "
         "reproducibility claim that a reviewer can verify without reading the code.")

    callout(doc, "Reproducibility is a property of the design",
            "If the raw data is immutable, the rules are functions, the log is complete and the "
            "environment is pinned, reproducibility follows. If any one of those is missing, no "
            "amount of documentation will recover it after the fact.",
            space_after=6)
