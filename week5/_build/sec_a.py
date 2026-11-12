# -*- coding: utf-8 -*-
"""Sections 1-2: evaluation doctrine and the metric suite."""

from pathlib import Path

from docbase import (h1, h2, h3, para, bullet, table, callout, figure,
                     spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
import facts as F

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
M = F.META
H = F.HORIZONS


def section_1(doc):
    h1(doc, "1.  Scope, Evidence and Evaluation Doctrine", page_break=True)

    para(doc,
         "This document answers a narrower question than “is the model good?”. It answers the question a "
         "business actually asks: what may we claim about this forecast, what may we do with it, and what "
         "would have to change before we claim more? The distinction matters because a single accuracy "
         "number can support a procurement decision, a budget range, a trading signal or a policy "
         "recommendation — and it cannot support all four at once.")

    h2(doc, "1.1  What this strategy governs")

    para(doc,
         "The strategy is a standing evaluation protocol for the agribusiness forecasting system specified "
         "in Weeks 1–4. It applies to both forecast targets — monthly wholesale prices and seasonal crop "
         "yields — although the executed evidence in this document is price-based, because that is the "
         "target for which a complete, public, monthly history exists. The protocol covers five decisions:")

    bullet(doc, "whether a candidate model is published at all, and at which horizons;",
           lead="Publication. ")
    bullet(doc, "which number, range and caveat appear in front of a procurement director, a "
                "finance committee or a policy adviser;",
           lead="Framing. ")
    bullet(doc, "whether the forecast is used for level planning, direction timing, "
                "scenario design or not at all;",
           lead="Use. ")
    bullet(doc, "which failures are escalated, retired or reworked, and on what timetable;",
           lead="Escalation. ")
    bullet(doc, "what evidence would justify a stronger claim at the next review.",
           lead="Reinvestment. ")

    para(doc,
         "The protocol is deliberately asymmetric. It is easy to pass a weak bar and hard to earn a strong "
         "claim. A model may be published as a benchmark-relative range without being certified as a "
         "directional signal. That is not a compromise; it is the correct description of what the evidence "
         "supports.")

    h2(doc, "1.2  The five questions every evaluation must answer")

    para(doc,
         "Accuracy is not one property. Five questions separate the claims that stakeholders routinely "
         "blend together. Each has a primary metric, a failure signal and a place in the report. Table 1 "
         "is the contract between the evaluation team and the reader: if a question is not answered in the "
         "row’s evidence column, the report is incomplete.")

    table(doc,
          ["Question", "What it asks", "Primary evidence", "Failure signal", "Reported in"],
          [
              ("Q1  Accuracy",
               "How large is the typical error, in decision units?",
               "MAE, RMSE and MASE against both naïve benchmarks, by horizon",
               "A model whose error is no smaller than the benchmark, or whose advantage is smaller than the measurement noise",
               "§3.9, §5.3"),
              ("Q2  Calibration",
               "Does the stated range contain the truth at the promised rate?",
               "Empirical coverage at 50/80/90/95%, interval width and Winkler score",
               "Coverage more than five points below nominal, or narrow intervals achieved by under-covering",
               "§3.5, §4.5"),
              ("Q3  Direction",
               "Can it tell an increase from a decrease?",
               "Directional accuracy with a binomial confidence interval; base-rate comparison",
               "A confidence interval that includes 50%, or a hit rate that disappears once the market trend is removed",
               "§2.3, §5.6"),
              ("Q4  Stability",
               "Does the result survive crop, state, horizon and regime changes?",
               "Segment MASE, regime splits, volatility buckets, cross-commodity replication",
               "A pooled result that reverses in one or more segments, or a sign change across regimes",
               "§3.6–3.7"),
              ("Q5  Value",
               "Does it improve a decision after costs?",
               "Asymmetric cost-weighted error, procurement regret, threshold sweep",
               "Regret no better than the default rule, or an optimum that exists only in-sample",
               "§2.5, §4.5.8"),
          ],
          [2.2, 3.9, 4.4, 4.6, 1.5], size=8.0, first_col_bold=True,
          caption_text="The five evaluation questions, their primary evidence, and the signal that the claim has failed.")

    callout(doc, "WHY FIVE QUESTIONS",
            "A model can be accurate on average and useless for direction; it can be well calibrated and "
            "worse than a random walk; it can win in one crop and lose in another. Collapsing these into a "
            "single “model accuracy” line is how forecast reports become confidently wrong.")

    h2(doc, "1.3  Seven principles")

    para(doc,
         "The principles below are not stylistic preferences. Each one prevents a specific failure that "
         "appears repeatedly in applied forecasting reviews.", space_after=5)

    bullet(doc, "Every candidate is scored on the same folds as a random walk and a "
                "seasonal naïve. A model that cannot beat the pair is not reported as an improvement, "
                "however sophisticated its architecture. The pair matters because the two benchmarks fail "
                "in different conditions: the random walk survives shocks, the seasonal naïve captures "
                "harvest cycles.",
           lead="1. Benchmark or it did not happen. ")
    bullet(doc, "A pooled MASE can hide a crop that fails and a crop that "
                "carries the average. Every headline number is decomposed by crop, state and horizon "
                "before it is published.",
           lead="2. No pooled number without segments. ")
    bullet(doc, "The metric set, the gate thresholds and the fold "
                "boundaries are fixed before the candidate models are examined. Otherwise the evaluation "
                "quietly becomes a search for the metric that flatters the model.",
           lead="3. Pre-register the test. ")
    bullet(doc, "A point estimate of 0.98 is not evidence of a 2% "
                "improvement if the 95% interval runs from −7% to +7%. Every headline is accompanied by a "
                "paired bootstrap interval, a Diebold–Mariano test and a minimum detectable effect.",
           lead="4. Report the uncertainty of the metric, not only of the forecast. ")
    bullet(doc, "Accuracy, calibration and direction are separate "
                "claims with separate thresholds. Passing one does not license the others.",
           lead="5. Never let one metric speak for three. ")
    bullet(doc, "The relevant loss is asymmetric: a missed "
                "procurement costs more than a carried inventory. The evaluation therefore includes a "
                "cost-weighted error and a threshold rule, not only a symmetric statistical score.",
           lead="6. Score the decision, not just the forecast. ")
    bullet(doc, "The three-month horizon fails the promotion "
                "gate in the executed evidence, and it is reported with the same prominence as the "
                "horizons that pass. A failure that is omitted becomes a surprise in production.",
           lead="7. Publish the failure. ")

    h2(doc, "1.4  The evidence base")

    para(doc,
         f"The strategy is not illustrated with hypothetical numbers. It is executed on the World Bank "
         f"Pink Sheet monthly price panel used in Week 4: {M['n_months']} complete months from "
         f"{M['data_start']} to {M['data_end']}, covering wheat, rice, maize, soybeans and cotton, with "
         f"DAP and urea as input-cost series. The design matrix contains {M['n_design']} usable months and "
         f"{M['n_features']} past-only predictors. The primary ladder runs {M['n_folds']} expanding-window "
         f"folds at a {M['step']}-month step across four horizons, producing "
         f"{M['n_folds'] * 4 * 6:,} fold-level forecasts from six models. No model fit failed. The "
         f"cross-commodity check repeats the ladder on all five crops at a four-month step.")

    table(doc,
          ["Element", "Executed setting", "Why this setting"],
          [
              ("Target", "Wheat, US HRW, USD/metric ton (primary); rice, maize, soybeans and cotton (replication)",
               "A globally traded, continuously quoted series with no missing months; the same target used in the Week 4 executed notebook"),
              ("Frequency", "Monthly, 2000-01 to 2026-10", "Matches the decision cadence of procurement and the publication cadence of Agmarknet"),
              ("Training window", f"Expanding, minimum {M['min_train']} months", "Twelve years covers at least one full price cycle and identifies annual seasonality"),
              ("Origin step", f"{M['step']} months", "Overlapping 12-month targets would otherwise inflate the effective sample"),
              ("Folds", f"{M['n_folds']} per horizon", "The most folds the current vintage supports without a target running past the final observation"),
              ("Horizons", "1, 3, 6 and 12 months", "The four planning windows used by procurement, budgeting and planting decisions"),
              ("Benchmarks", "Random walk and seasonal naïve", "Adversarial pair; a candidate must beat both, not the weaker one"),
              ("Candidate ladder", "ETS, SARIMAX, direct GBDT and a past-only inverse-MSE ensemble",
               "Statistical, structural and machine-learning families with different failure modes"),
              ("Interval method", "Online conformal residuals, fold k uses folds < k only",
               "Distribution-free and auditable; avoids assuming Gaussian errors"),
              ("Computation", f"{M['runtime_seconds']:.0f} seconds on a laptop, no GPU", "Reproducible by a reviewer without infrastructure"),
          ],
          [3.0, 7.8, 5.8], size=8.0, first_col_bold=True,
          caption_text="Executed evidence base: data, folds, models and interval construction.")

    para(doc,
         "Two protocol changes from Week 1 are recorded here rather than hidden. Week 1 proposed a "
         "36-month initial window and a one-month step. The executed harness uses 120 months and a "
         "three-month step. A 36-month window cannot identify an annual seasonal pattern, and a one-month "
         "step with overlapping 12-month targets would produce 100-plus folds whose errors are almost "
         "perfectly correlated — precision that is not information. The longer window and wider step are "
         "the defensible choice; the change is documented so that a reader can challenge it.")

    figure(doc, FIG_DIR / "evaluation_architecture.png", width_cm=CONTENT_W,
           caption_text="The evaluation production line: five stages, four gates and one decision owner. A failure at any gate stops publication of the claim, not the analysis.")

    h2(doc, "1.5  Governance: who owns which judgement")

    para(doc,
         "An evaluation is a social process as much as a statistical one. If the same person selects the "
         "model, chooses the metric and signs the release, the protocol is decorative. Table 3 assigns "
         "four separable judgements. In a small team one person may hold more than one role, but the "
         "roles must be named in the release note and the conflict disclosed.")

    table(doc,
          ["Role", "Owns", "Cannot do alone", "Evidence produced"],
          [
              ("Model owner", "The ladder, folds, hyperparameters and code", "Approve the promotion decision",
               "Reproducible pipeline, fold-level predictions, model card"),
              ("Independent validator", "Metric computation, calibration and significance tests", "Change the model to make it pass",
               "Evaluation report, exception log, signed scorecard"),
              ("Business owner", "The decision the forecast informs and the cost of error", "Redefine the metric after seeing results",
               "Decision memo, threshold rule, value estimate"),
              ("Data steward", "Source vintage, publication lag, revisions and licensing", "Waive a provenance requirement",
               "Data dictionary, vintage log, coverage statement"),
              ("Release approver", "The published claim and its caveat", "Overrule the validator’s factual finding",
               "Signed release note and review date"),
          ],
          [3.0, 5.2, 4.2, 4.2], size=8.0, first_col_bold=True,
          caption_text="Evaluation governance: separable judgements and the evidence each role signs.")

    h2(doc, "1.6  How to read the numbers in this document")

    bullet(doc, "All price errors are in USD per metric ton. A percentage is always "
                "labelled as such. A basis point is never used to describe a price change.",
           lead="Units. ")
    bullet(doc, "An error is meaningful only next to the random-walk error on the same "
                "folds. “MAE fell by 2%” is not a result; “MAE was 2% below the random walk, with a 95% "
                "interval from −7% to +7%” is.",
           lead="Benchmarks. ")
    bullet(doc, "MASE appears in two forms. Absolute MASE divides by the in-sample "
                "seasonal-naïve error of the first 120 months; it is comparable across crops but rises "
                "mechanically with the horizon. Relative MASE divides by the random-walk error on the same "
                "folds and horizon; it is the promotion gate. The report always names which one is meant.",
           lead="MASE. ")
    bullet(doc, "Coverage is the share of realised values inside the stated interval. "
                "A 90% interval that contains 79% of outcomes is under-covering, even if it looks wide.",
           lead="Coverage. ")
    bullet(doc, "A result is called significant only when the paired 95% interval excludes "
                "zero and the Diebold–Mariano test agrees. A small p-value with an economically trivial "
                "difference is reported as statistically detectable but not materially useful.",
           lead="Significance. ")


def section_2(doc):
    h1(doc, "2.  The Metric Suite: What to Measure, and How Each Metric Lies", page_break=True)

    para(doc,
         "Every metric is a lens with a distortion. The purpose of a metric suite is not to accumulate "
         "scores but to make the distortions visible to one another. This section defines the metrics used "
         "in the harness, states the decision each one serves, and — more importantly — states the "
         "specific condition under which it misleads.")

    h2(doc, "2.1  A hierarchy, not a menu")

    para(doc,
         "The metrics are ordered by the claim they support. Accuracy answers “how far off?”. Calibration "
         "answers “how honest is the range?”. Direction answers “which way?”. Stability answers “for whom "
         "and when?”. Value answers “does it matter?”. A report that climbs the hierarchy can support a "
         "decision; a report that stops at accuracy can only describe an error.")

    table(doc,
          ["Layer", "Claim it supports", "Core metrics", "What it cannot establish"],
          [
              ("1  Accuracy", "The forecast is closer to the outcome than a stated benchmark",
               "MAE, RMSE, MASE vs RW, MASE vs SN", "Whether the difference is real, or whether the range is honest"),
              ("2  Calibration", "The stated uncertainty contains the truth at the promised rate",
               "Coverage, width, Winkler score, pinball loss", "Whether the centre of the distribution is useful"),
              ("3  Direction", "The forecast signals the correct sign of change",
               "Directional accuracy, base-rate skill, confusion matrix", "The size of the move, or the cost of a wrong sign"),
              ("4  Stability", "The result survives crop, state, horizon and regime changes",
               "Segment MASE, regime splits, volatility buckets, rank stability", "Whether the future will resemble the tested past"),
              ("5  Value", "The forecast improves a decision after costs",
               "Asymmetric cost-weighted error, regret, threshold sweep", "Whether the organisation will actually use it"),
          ],
          [2.6, 6.0, 5.0, 3.0], size=8.2, first_col_bold=True,
          caption_text="The evaluation hierarchy: five layers of claim, each with its own evidence standard.")

    callout(doc, "THE CARDINAL RULE",
            "No single metric may promote a model. Promotion requires a benchmark-relative accuracy result, "
            "a calibrated interval, a direction result that is separable from chance, stability across the "
            "declared segments, and a decision value that is positive after cost. A model may be published "
            "without clearing all five — but the claim in the report must name which layers it cleared.")

    h2(doc, "2.2  Point-accuracy metrics")

    h3(doc, "MAE — mean absolute error")
    para(doc,
         "MAE is the average absolute difference between the forecast and the outcome, in the units of the "
         "decision. It is the most interpretable accuracy metric and the one a procurement officer can "
         "budget against: an MAE of 12 USD/MT on a 300 USD/MT commodity is a 4% planning margin. It is "
         "robust to a single catastrophic miss, which is both its strength and its weakness: a model that "
         "is usually 10 USD wrong and occasionally 200 USD wrong can report the same MAE as a model that "
         "is consistently 20 USD wrong.", space_after=4)
    para(doc, "    MAE = (1/n) Σ |yᵢ − ŷᵢ|", size=9.5, italic=True, color=SECONDARY)
    para(doc,
         "MAE is scale-dependent, so it cannot compare wheat at 300 USD/MT with cotton at 2,000 USD/MT. "
         "That is why every cross-crop statement in this report uses MASE or a percentage, never raw MAE.")

    h3(doc, "RMSE — root mean squared error")
    para(doc,
         "RMSE squares the errors before averaging, so a 100 USD miss contributes 100 times as much as a "
         "10 USD miss. It is the right metric for stress questions — how bad is the bad month? — and the "
         "wrong metric for the typical planning question, because one shock can dominate the score. In the "
         "executed evidence, the ensemble’s h=1 RMSE is 17.9 against an MAE of 12.1, a ratio of 1.48; that "
         "gap is the tail talking. RMSE is reported as a risk diagnostic and is never the promotion gate.",
         space_after=4)
    para(doc, "    RMSE = √[(1/n) Σ (yᵢ − ŷᵢ)²]", size=9.5, italic=True, color=SECONDARY)

    h3(doc, "MAPE — mean absolute percentage error, and its near-zero problem")
    para(doc,
         "MAPE expresses the error as a percentage of the actual value. It is intuitive, unit-free and "
         "seductive. It is also asymmetric: an actual of 100 with a forecast of 110 scores 10.0%, while an "
         "actual of 110 with a forecast of 100 scores 9.1%. The same 10-unit error produces a different "
         "score depending on direction, which rewards under-forecasting. Near zero the metric explodes: an "
         "actual of 5 with a forecast of 10 is a 100% error, even though the absolute miss is 5 USD. In "
         "mandi data, where a perishable vegetable can trade at a few rupees per kilogram in glut and "
         "hundreds in scarcity, MAPE is not a safe headline.", space_after=4)
    para(doc, "    MAPE = (100/n) Σ |yᵢ − ŷᵢ| / |yᵢ|", size=9.5, italic=True, color=SECONDARY)
    para(doc,
         "The harness applies a pre-registered guard: MAPE is reported only when the first percentile of "
         "the evaluation target is at least five times the MAE. If that condition fails, MAPE is "
         "suppressed and sMAPE is shown instead, with the suppression stated in the table note. The "
         "condition is checked by code, not by eye.")

    h3(doc, "sMAPE — symmetric mean absolute percentage error")
    para(doc,
         "sMAPE divides the absolute error by the average of the actual and the forecast, which bounds it "
         "between 0% and 200% and removes the worst of MAPE’s directional bias. It still misbehaves near "
         "zero, and its upper bound is arbitrary: a forecast of −100 against an actual of +100 scores 200%, "
         "which is not a percentage a reader should interpret literally. sMAPE is used as the "
         "non-specialist-facing percentage, always alongside MASE, never alone.", space_after=4)
    para(doc, "    sMAPE = (200/n) Σ |yᵢ − ŷᵢ| / (|yᵢ| + |ŷᵢ|)", size=9.5, italic=True, color=SECONDARY)
    para(doc,
         "In the executed scorecard, sMAPE and MAPE agree closely because all prices are far from zero "
         "(the wheat series never falls below 90 USD/MT). That agreement is a property of this dataset, not "
         "a general licence. The guard exists for the datasets where it fails.")

    h3(doc, "MASE — mean absolute scaled error, the primary gate")
    para(doc,
         "MASE divides the forecast’s MAE by the MAE of a naïve benchmark on the same series. The result is "
         "scale-free: below 1.0 means the model beats the benchmark, above 1.0 means it does not. Two "
         "versions are used, and conflating them is one of the most common errors in forecast reporting.",
         space_after=4)
    para(doc, "    MASE_abs = MAE_model / [(1/(T−1)) Σ |yₜ − yₜ₋₁|]", size=9.5, italic=True, color=SECONDARY)
    para(doc, "    MASE_RW = MAE_model / MAE_randomwalk   (same folds, same horizon)", size=9.5, italic=True, color=SECONDARY)
    para(doc,
         "the first divides by the in-sample one-step naïve error of the first 120 months; it is comparable "
         "across crops but rises mechanically with the horizon, because a 12-month forecast is harder than a "
         "one-month forecast. The second divides by the random walk evaluated on exactly the same folds and "
         "horizon; it is the promotion gate. In the executed evidence the ensemble has an absolute MASE of "
         f"{F.num(F.score(1,'Ensemble')['mase'],2)} at h=1 and an absolute MASE of "
         f"{F.num(F.score(12,'Ensemble')['mase'],2)} at h=12, while its relative MASE is "
         f"{F.num(F.score(1,'Ensemble')['mase_rw'],3)} and {F.num(F.score(12,'Ensemble')['mase_rw'],3)}. "
         "The absolute figure above 1.0 does not mean the model loses to its benchmark: the denominator is "
         "fixed to the volatility of 2001–2010, and the 2011–2026 evaluation window was more volatile. The "
         "relative figure is the honest comparison because it uses the same folds. Both are shown so that "
         "the reader can see the scale drift rather than infer it.")

    h3(doc, "R² — the most over-read number in applied forecasting")
    para(doc,
         "The coefficient of determination measures the share of variance in the evaluation outcomes "
         "explained by the forecast. It is a legitimate descriptive statistic and a poor promotion "
         "criterion. Three traps explain why.", space_after=4)
    para(doc, "    R² = 1 − Σ(yᵢ − ŷᵢ)² / Σ(yᵢ − ȳ)²", size=9.5, italic=True, color=SECONDARY)
    bullet(doc, "When the series trends, the variance around its mean is large and "
                "almost any persistent forecast scores well. In the executed evidence the random walk "
                f"achieves R² = {F.num(F.score(1,'Random Walk')['r2'],3)} at h=1, while the ensemble achieves "
                f"{F.num(F.score(1,'Ensemble')['r2'],3)}. The difference is 0.003 — three thousandths of "
                "variance — yet the raw R² looks like a strong model because the trend is doing the work.",
           lead="Trend inflation. ")
    bullet(doc, "An out-of-sample R² can be negative. A model that is worse than "
                "predicting the evaluation-period mean has R² below zero. The metric is bounded above by 1 "
                "and unbounded below, so a single bad fold can move it dramatically.",
           lead="The negative tail. ")
    bullet(doc, "R² is insensitive to bias and to the cost of error. A model that "
                "consistently over-forecasts by 6 USD/MT can still have a high R². In this evaluation the "
                f"ensemble’s h=12 bias is {F.signed(F.score(12,'Ensemble')['bias'],1)} USD/MT, which is "
                "invisible in R² but material to a buyer.",
           lead="Bias invisibility. ")

    h3(doc, "Bias and MPE — the systematic error")
    para(doc,
         "Bias is the mean signed error, forecast minus actual. Positive means the model over-forecasts. "
         "The mean percentage error (MPE) expresses the same quantity as a percentage of the actual. The "
         "pair is reported because a model can have a low MAE and a persistent bias: random errors cancel, "
         "but a procurement department that consistently buys 5% too early does not.")
    para(doc, "    Bias = (1/n) Σ (ŷᵢ − yᵢ)        MPE = (100/n) Σ (ŷᵢ − yᵢ) / yᵢ",
         size=9.5, italic=True, color=SECONDARY)
    para(doc,
         f"The acceptance threshold is |MPE| < 5% of the mean price. The ensemble passes at h=1 "
         f"({F.signed(F.score(1,'Ensemble')['mpe'],2)}%) but drifts to "
         f"{F.signed(F.score(12,'Ensemble')['mpe'],2)}% at h=12; ETS is worse at "
         f"{F.signed(F.score(12,'ETS')['mpe'],2)}%. The drift is a finding, not a rounding error: the model "
         "is systematically optimistic at the long horizon, which overstates forward margins.")

    h2(doc, "2.3  Direction and probability")

    h3(doc, "Directional accuracy — the metric a trader acts on")
    para(doc,
         "Directional accuracy is the share of folds in which the forecast correctly predicts whether the "
         "price will rise or fall from its level at the forecast origin. A random walk has no predicted "
         "change and therefore no defined direction; it is excluded from this metric rather than scored as "
         "50%.", space_after=4)
    para(doc, "    DA = (100/n) Σ 1[sign(yᵢ − y₀) = sign(ŷᵢ − y₀)]", size=9.5, italic=True, color=SECONDARY)
    para(doc,
         f"The executed ensemble records {F.num(F.score(1,'Ensemble')['da'],1)}%, "
         f"{F.num(F.score(3,'Ensemble')['da'],1)}%, {F.num(F.score(6,'Ensemble')['da'],1)}% and "
         f"{F.num(F.score(12,'Ensemble')['da'],1)}% at h=1, 3, 6 and 12. Those numbers look close to a coin "
         "flip, and they are. With 60 folds, the 95% binomial interval around 50% runs from roughly 37% to "
         "63%; a hit rate of 55% is inside it. The correct conclusion is not “55% is promising” but “the "
         "evaluation cannot distinguish this model from chance on direction.” Directional use therefore "
         "fails the evidence test, regardless of the point accuracy.")

    h3(doc, "Pinball loss and CRPS — scoring the whole distribution")
    para(doc,
         "Pinball loss evaluates a quantile forecast. For a quantile q and forecast f, the loss penalises "
         "an outcome above f at rate q and an outcome below f at rate 1−q. Averaging the 5th and 95th "
         "quantile losses gives a simple distributional score; CRPS integrates the same idea over all "
         "quantiles. A point forecast can improve while the distribution worsens — for example, if the "
         "model widens its intervals to avoid misses.", space_after=4)
    para(doc,
         "    L_q(y, f) = q(y − f)  if y ≥ f;   (1−q)(f − y)  if y < f",
         size=9.5, italic=True, color=SECONDARY)
    para(doc,
         f"The executed result is exactly this kind of divergence. The ensemble’s h=1 pinball loss is "
         f"{F.num(F.score(1,'Ensemble')['pinball'],2)}, worse than the random walk’s "
         f"{F.num(F.score(1,'Random Walk')['pinball'],2)}, even though the ensemble has the lower MAE. The "
         "ensemble’s intervals are wider and its distribution is not better centred. A report that "
         "published only the MAE would miss the regression in probabilistic quality.")

    h3(doc, "Coverage, width and the Winkler score")
    para(doc,
         "Coverage is the share of realised values inside the stated interval. It is necessary but not "
         "sufficient: an interval from zero to infinity covers everything and is useless. Width measures "
         "sharpness. The Winkler score combines the two, adding a penalty of 2/α times the distance by which "
         "an outcome misses the interval. The three are always reported together.", space_after=4)
    para(doc, "    PICP = (100/n) Σ 1[Lᵢ ≤ yᵢ ≤ Uᵢ]        Winkler = width + (2/α)(L−y)⁺ + (2/α)(y−U)⁺",
         size=9.5, italic=True, color=SECONDARY)
    para(doc,
         f"The ensemble’s empirical 90% coverage is {F.num(F.score(1,'Ensemble')['coverage90'],1)}% at h=1, "
         f"{F.num(F.score(3,'Ensemble')['coverage90'],1)}% at h=3, "
         f"{F.num(F.score(6,'Ensemble')['coverage90'],1)}% at h=6 and "
         f"{F.num(F.score(12,'Ensemble')['coverage90'],1)}% at h=12. The h=12 interval under-covers by more "
         "than ten points. It is not narrow — its average width is 155 USD/MT — so the problem is not "
         "sharpness but a distribution that shifted after the calibration window. This is the single most "
         "important calibration finding in the report, and it is why coverage is monitored in production "
         "rather than certified once.")

    h2(doc, "2.4  Stability metrics")

    para(doc,
         "Stability asks whether the result is a property of the model or of one favourable slice of "
         "history. Three diagnostics are used. Segment MASE recomputes the gate separately for each crop, "
         "state, horizon and price regime. Fold dispersion reports the standard deviation of absolute error "
         "across folds, because a model with the same mean error and twice the dispersion is a different "
         "operational risk. Rank stability reports whether the ordering of models is consistent across "
         "folds; if the “best” model changes every few folds, the ranking is noise.")

    table(doc,
          ["Diagnostic", "Definition", "Acceptance rule", "What a failure means"],
          [
              ("Segment MASE", "MASE vs RW recomputed within each crop × horizon cell",
               "No cell above 1.10 unless the pooled result is also above 1.0",
               "The pooled average is carried by one or two favourable segments"),
              ("Regime split", "MASE recomputed before and after January 2023",
               "Sign of the advantage is the same in both periods",
               "The model’s edge is a regime artefact, not a stable relationship"),
              ("Volatility bucket", "MASE recomputed in low, mid and high volatility terciles",
               "No monotonic collapse in the high-volatility tercile",
               "The model fails precisely when the decision matters most"),
              ("Fold dispersion", "Standard deviation of absolute error across folds",
               "Reported, not gated; compared with the benchmark",
               "A wide dispersion means the average hides operational risk"),
              ("Rank stability", "Share of folds in which a model remains in the top two",
               "At least 70% for a champion claim",
               "Model selection is unstable; the champion is a fold-specific accident"),
          ],
          [2.8, 5.4, 4.2, 4.2], size=8.0, first_col_bold=True,
          caption_text="Stability diagnostics and the acceptance rules that turn them into decisions.")

    h2(doc, "2.5  Decision-weighted metrics")

    para(doc,
         "Symmetric error treats a 10 USD over-forecast and a 10 USD under-forecast as equally bad. In "
         "procurement they are not. An under-forecast that leaves the buyer short forces a spot purchase at "
         "the peak; an over-forecast carries inventory, insurance and spoilage. The harness therefore "
         "reports an asymmetric cost-weighted error with a 4:1 penalty, and a threshold rule that converts "
         "the forecast into a buy-now or wait decision.")

    para(doc, "    CWE = (1/n) Σ [ c_u · max(yᵢ − ŷᵢ, 0) + c_o · max(ŷᵢ − yᵢ, 0) ]",
         size=9.5, italic=True, color=SECONDARY)
    para(doc,
         f"With c_u = 1.00 and c_o = 0.25, the ensemble’s h=1 cost-weighted error is "
         f"{F.num(F.score(1,'Ensemble')['cwe'],2)} USD/MT against a random walk’s "
         f"{F.num(F.score(1,'Random Walk')['cwe'],2)}. The difference is less than one percent of the "
         "purchase price. At h=6 the ensemble is worse "
         f"({F.num(F.score(6,'Ensemble')['cwe'],2)} vs {F.num(F.score(6,'Random Walk')['cwe'],2)}). The "
         "decision-weighted view confirms the accuracy view: any advantage is small, horizon-dependent and "
         "not robust enough to support a strong operational claim.")

    para(doc,
         "The threshold rule is evaluated over a grid of buy-now thresholds from −3% to +6%. For each "
         "threshold the harness computes the realised purchase cost, the regret against perfect foresight "
         "and the share of price rises captured. The in-sample optimum is a threshold of "
         f"{F.DECISION_SUMMARY['best_tau']*100:+.1f}%, which reduces regret from "
         f"{F.num(F.DECISION_SUMMARY['always_wait_regret_pct'],2)}% for an always-wait policy to "
         f"{F.num(F.DECISION_SUMMARY['best_regret_pct'],2)}%. That is a real but small improvement — about "
         f"{F.num(F.DECISION_SUMMARY['always_wait_regret']-F.DECISION_SUMMARY['best_regret'],2)} USD/MT on "
         "an average price near 267 USD/MT. It is also an in-sample optimum, and the report treats it as a "
         "hypothesis to test in shadow deployment, not as a production setting.")

    h2(doc, "2.6  The metric registry")

    para(doc,
         "Table 6 is the controlled vocabulary for the rest of the document. Any number that appears in a "
         "release note must map to a row here, with the stated unit, threshold and known failure mode. "
         "Metrics that are not in the registry are exploratory and cannot support a published claim.")

    table(doc,
          ["Metric", "Formula (compact)", "Unit", "Decision threshold", "Primary use", "Known failure mode"],
          [
              ("MAE", "mean |y − ŷ|", "USD/MT", "Benchmark-relative; no absolute threshold", "Planning margin, procurement budget", "Hides catastrophic tails; scale-dependent"),
              ("RMSE", "√mean (y − ŷ)²", "USD/MT", "Reported, not gated", "Stress and tail risk", "One shock dominates; not comparable across crops"),
              ("MAPE", "100·mean |y − ŷ|/|y|", "%", "Suppressed when p1(y) < 5·MAE", "Non-specialist error summary", "Explodes near zero; rewards under-forecasting"),
              ("sMAPE", "200·mean |y − ŷ|/(|y|+|ŷ|)", "%", "Reported with MASE", "Cross-crop communication", "Unstable near zero; arbitrary 200% bound"),
              ("MASE_abs", "MAE / in-sample naïve MAE", "ratio", "< 1.0 is desirable", "Cross-crop comparability", "Rises with horizon; denominator choice matters"),
              ("MASE_RW", "MAE / RW MAE on same folds", "ratio", "< 1.00, and MASE_SN < 1.00", "Promotion gate", "A point estimate; must carry a CI"),
              ("R²", "1 − SSE/SST", "ratio", "Never used to promote", "Descriptive variance share", "Inflated by trend; can be negative; ignores bias"),
              ("Bias", "mean (ŷ − y)", "USD/MT", "|MPE| < 5%", "Detect systematic optimism", "Sign convention confusion"),
              ("MPE", "100·mean (ŷ − y)/y", "%", "|MPE| < 5%", "Bias as a share of price", "Unstable when prices are low"),
              ("Directional accuracy", "share of correct signs", "%", "CI must exclude 50%; ≥ 55% for timing", "Trading and timing decisions", "Chance is wide with few folds; trend inflates it"),
              ("Pinball loss", "mean quantile loss", "USD/MT", "Reported and compared", "Distributional accuracy", "Not intuitive to non-specialists"),
              ("Coverage", "share inside interval", "%", "Within 5 points of nominal", "Calibration audit", "Can be gamed by widening the interval"),
              ("Interval width", "mean (U − L)", "USD/MT", "Reported with coverage", "Sharpness", "Narrow intervals may simply under-cover"),
              ("Winkler score", "width + miss penalty", "USD/MT", "Minimised", "Joint sharpness and calibration", "Sensitive to the α level"),
              ("CWE", "asymmetric absolute loss", "USD/MT", "Lower than the benchmark", "Procurement cost", "Penalty ratio is a business assumption"),
              ("Regret", "cost − perfect-foresight cost", "USD/MT", "Lower than the default rule", "Decision value", "In-sample optimum may not persist"),
          ],
          [2.3, 3.3, 1.4, 2.9, 3.0, 3.7], size=7.6, first_col_bold=True,
          caption_text="Metric registry: the controlled vocabulary for every published number.")

    h2(doc, "2.7  Choosing metrics by decision")

    para(doc,
         "Different readers need different numbers. A procurement director needs MAE and cost-weighted "
         "error in USD/MT. A finance committee needs the interval and the budget range. A trading desk "
         "needs directional accuracy and a confusion matrix. A policy adviser needs scenario ranges and a "
         "stated failure condition. A data team needs pinball loss, coverage and stability diagnostics. "
         "Table 7 maps the decision to the metric set, so that no reader is handed a number that answers "
         "someone else’s question.")

    table(doc,
          ["Decision", "Primary metric", "Supporting evidence", "What the reader should do with it"],
          [
              ("Procurement timing", "CWE and directional accuracy", "Threshold sweep, regret, confusion matrix",
               "Set a buy-now threshold; do not act on a point forecast alone"),
              ("Budget and cash planning", "MAE and 90% interval width", "Coverage, bias, scenario range",
               "Budget to the upper band, not the point"),
              ("Planting and input purchase", "Segment MASE for yield", "Regime split, weather stress tests",
               "Use the range for input planning; do not treat the point as a target"),
              ("Insurance pricing", "Pinball loss and coverage", "Tail loss, Winkler score, worst-fold error",
               "Price to the tail, and re-price when coverage drifts"),
              ("Policy and buffer stock", "Scenario range and bias", "Regime stability, structural-break log",
               "Use the range to size the buffer; state the policy-shock caveat"),
              ("Model operations", "MASE, coverage and rank stability", "Fold dispersion, drift monitors",
               "Retrain or retire on a pre-agreed trigger"),
          ],
          [3.2, 4.2, 5.0, 4.2], size=8.0, first_col_bold=True,
          caption_text="Decision-to-metric mapping: every audience receives only the numbers it can act on.")

    h2(doc, "2.8  What this evaluation deliberately does not use")

    bullet(doc, "A high R² is not evidence of forecast skill when the series "
                "trends. It is reported, with the random-walk R² beside it, and it never promotes a model.",
           lead="R² as a headline. ")
    bullet(doc, "MAPE is suppressed when the target approaches zero. "
                "The guard is coded, not judgemental.",
           lead="MAPE on thin or volatile markets. ")
    bullet(doc, "“75% accurate” is a classification metric applied to a "
                "continuous problem. It hides the size and cost of the 25%.",
           lead="Percentage accuracy on a continuous target. ")
    bullet(doc, "If a model wins in one crop and loses in four, the "
                "pooled average is not the result. The segment table is.",
           lead="A pooled number presented as the result. ")
    bullet(doc, "Testing twenty configurations and reporting the best "
                "one without a multiple-comparison adjustment is a search, not an evaluation. The harness "
                "fixes the ladder and reports every rung.",
           lead="Best-of-many without a correction. ")
    bullet(doc, "The evaluation reports what happened on the tested folds. "
                "It does not claim that the relationship will hold through an unobserved policy shock.",
           lead="Backtest as prophecy. ")
