# -*- coding: utf-8 -*-
"""Sections 5-6: the reporting system, the executive summary, and limitations."""

from pathlib import Path

from docbase import (h1, h2, h3, para, bullet, table, callout, figure,
                     spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
import facts as F

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
H = F.HORIZONS


def section_5(doc):
    h1(doc, "5.  The Reporting System and the Executive Summary", page_break=True)

    para(doc,
         "A forecast is not finished when the model converges. It is finished when a named person can make "
         "a decision with it, explain the decision to someone else, and say what would prove them wrong. "
         "The reporting system exists to make that possible without diluting the evidence. It has three "
         "tiers, one executive-summary template and one failure protocol.")

    h2(doc, "5.1  Three report tiers, one source of truth")

    para(doc,
         "The same scorecard feeds three documents. The decision memo is one page and is written for the "
         "person who owns the budget. The evaluation report is the working document for the business and "
         "validation teams. The audit pack is the technical evidence that lets an outsider reproduce every "
         "number. No tier may contain a number that is absent from the tier below it.")

    table(doc,
          ["Tier", "Audience and cadence", "Length and mandatory content", "What it must not contain"],
          [
              ("1  Decision memo", "Business owner, board, policy lead; monthly and after any shock",
               "One page: finding, range, decision, caveat, owner, review date",
               "Model architecture, p-values without interpretation, unexplained acronyms"),
              ("2  Evaluation report", "Procurement, finance, agronomy, validation; monthly or quarterly",
               "8–12 pages: scorecard, calibration, segments, two or three charts, limitations, actions",
               "A claim that is not traceable to a table or a fold file"),
              ("3  Audit pack", "Validator, data engineer, external reviewer; per release",
               "Fold-level predictions, code hash, data vintage, metric definitions, test outputs",
               "Edited numbers, hand-adjusted scores, charts without source data"),
          ],
          [2.6, 4.6, 5.4, 4.0], size=8.0, first_col_bold=True,
          caption_text="Three report tiers: one evidence base, three levels of detail.")

    h2(doc, "5.2  The four-box executive summary")

    para(doc,
         "The executive summary is not a shortened report. It is a structured argument with four boxes. "
         "Each box answers one question and refuses to answer the others. The structure is deliberately "
         "rigid: it prevents the two most common failures — burying the decision under method, and "
         "presenting a point estimate without the uncertainty that qualifies it.")

    table(doc,
          ["Box", "Question it answers", "What must be in it", "What must not be in it"],
          [
              ("FINDING", "What did we learn, relative to a benchmark?",
               "One sentence: model, target, horizon, benchmark-relative result and gate outcome",
               "A raw accuracy number with no benchmark"),
              ("RANGE", "How wrong could it be?",
               "The interval, its coverage in backtest, and the direction of the known bias",
               "A point estimate presented as the forecast"),
              ("DECISION", "What should the reader do, and what should they not do?",
               "The permitted use, the prohibited use, the owner and the review date",
               "A generic recommendation to “use with caution”"),
              ("CAVEAT", "What would change the conclusion?",
               "The failure condition, the segment that fails, and the next test",
               "A disclaimer that protects the author rather than informing the reader"),
          ],
          [2.4, 4.4, 6.2, 3.6], size=8.0, first_col_bold=True,
          caption_text="The four-box executive summary: a fixed structure for a decision-grade claim.")

    h2(doc, "5.3  A worked executive summary")

    para(doc,
         "The example below uses the executed wheat results. It is deliberately unglamorous. The finding "
         "is a pass on the accuracy gate and a fail on the significance and direction gates. The decision "
         "is a planning use, not a trading use. The caveat names the horizon that fails and the condition "
         "that would trigger a re-run. This is what an honest summary looks like when the evidence is "
         "mixed.")

    table(doc,
          ["Box", "Worked text (wheat, October 2026 origin)"],
          [
              ("FINDING",
               f"At the one-month horizon the ensemble is 2.1% more accurate than a random walk "
               f"(MAE {F.num(F.score(1,'Ensemble')['mae'],2)} vs "
               f"{F.num(F.score(1,'Random Walk')['mae'],2)} USD/MT), which passes the accuracy gate. "
               f"The paired 95% interval on the difference is "
               f"{F.signed(F.sig(1,'Ensemble')['ci_lo'],2)} to "
               f"{F.signed(F.sig(1,'Ensemble')['ci_hi'],2)} USD/MT (p = "
               f"{F.num(F.sig(1,'Ensemble')['dm_p'],2)}), so the improvement is not statistically "
               f"separable from zero. At three months the model fails the gate (MASE "
               f"{F.num(F.score(3,'Ensemble')['mase_rw'],3)})."),
              ("RANGE",
               f"The 12-month point forecast is {F.num(F.latest_row(12)['forecast'],2)} USD/MT. The "
               f"conformal 90% band is {F.num(F.latest_row(12)['lo90'],0)}–"
               f"{F.num(F.latest_row(12)['hi90'],0)} USD/MT, but backtest coverage at this horizon is "
               f"{F.num(F.score(12,'Ensemble')['coverage90'],1)}%, so the band should be read as an "
               f"approximate 80% band. The model is also modestly optimistic at this horizon "
               f"(bias {F.signed(F.score(12,'Ensemble')['bias'],1)} USD/MT)."),
              ("DECISION",
               "Use the range for budget, contract-window and scenario planning. Do not use it as a "
               "directional trading or daily timing signal: directional accuracy is "
               f"{F.num(F.score(1,'Ensemble')['da'],1)}% at h=1 and "
               f"{F.num(F.score(12,'Ensemble')['da'],1)}% at h=12, both inside the binomial noise band "
               "around chance. The procurement threshold, if tested, is a separate decision and requires "
               "shadow deployment."),
              ("CAVEAT",
               "The three-month horizon is not supported and must be published as a benchmark, not as a "
               "model forecast. The evaluation is underpowered for a 2% effect: the minimum detectable "
               f"effect at h=1 is {F.num(F.sig(1,'Ensemble')['mde_pct'],1)}% of the random-walk MAE. "
               "Re-run after twelve new monthly observations, or immediately after a policy or trade "
               "shock. Owner: model validator. Review: 25 February 2027."),
          ],
          [2.4, 14.2], size=8.6, first_col_bold=True,
          caption_text="Worked executive summary for the executed wheat model. The boxes are filled from the scorecard, not written from memory.")

    callout(doc, "THE TEST OF A GOOD SUMMARY",
            "A reader who disagrees with the decision should be able to point to the box that would have "
            "to change. If every box is hedged, the summary has transferred the judgement back to the "
            "reader, which is the opposite of reporting.")

    h2(doc, "5.4  Ten writing rules")

    para(doc,
         "The rules are mechanical on purpose. They can be checked by an editor who does not understand "
         "the model, which is exactly the point.", space_after=5)

    bullet(doc, "The first sentence names the decision, not the "
                "algorithm. “Publish the range, not the point” is a decision; “we fitted a SARIMAX” is not.",
           lead="1. Lead with the decision. ")
    bullet(doc, "Every accuracy number is followed by its benchmark. "
                "“MAE 12.1” is incomplete; “MAE 12.1 against a random walk’s 12.4” is a result.",
           lead="2. Benchmark every number. ")
    bullet(doc, "The interval precedes the point. The reader should "
                "know the range before they anchor on the central path.",
           lead="3. Range before point. ")
    bullet(doc, "USD per metric ton for buyers, percentage for "
                "cross-crop comparison, days for lead time. Never switch units mid-sentence.",
           lead="4. Use the unit the reader budgets in. ")
    bullet(doc, "“MAE fell 2.1% and the interval includes zero” is two "
                "sentences. Combining them invites the reader to hear only the first.",
           lead="5. One number per sentence. ")
    bullet(doc, "If the 95% interval includes zero, write “we cannot "
                "distinguish this from the benchmark.” Do not write “broadly stable” or “directionally positive”.",
           lead="6. Say “we do not know” when the interval includes zero. ")
    bullet(doc, "Report 12.1 USD/MT, not 12.0937. Report 2.1%, not "
                "2.0873%. Precision beyond the decision is noise dressed as rigour.",
           lead="7. Round to decision precision. ")
    bullet(doc, "“Conformal interval” becomes “a range calibrated on "
                "past forecast errors”. “MASE” becomes “error relative to a random walk” on first use.",
           lead="8. Translate the jargon once, then use it. ")
    bullet(doc, "The caveat is a condition, not a disclaimer. “The "
                "model fails at three months” is useful; “forecasts are inherently uncertain” is not.",
           lead="9. State the failure condition. ")
    bullet(doc, "Every memo ends with a named owner and a date. A "
                "report without an owner is an orphan.",
           lead="10. Name the owner and the review date. ")

    h2(doc, "5.5  Stakeholder message matrix")

    para(doc,
         "The same evidence becomes a different message for each audience. The differences are not "
         "spin; they are the selection of the metric and the decision that the audience owns. Table 23 "
         "specifies what each group receives and what it must not be given.")

    table(doc,
          ["Audience", "Their decision", "What they receive", "What they must not receive", "Cadence"],
          [
              ("Board / finance", "Approve the budget range and the risk appetite",
               "One fan chart, the range, the verdict, the cost of error",
               "Fold counts, p-values, model names", "Monthly, one page"),
              ("Procurement", "Set the buy-now threshold and the contract window",
               "Horizon forecast, CWE, threshold curve, segment caveat",
               "R², SHAP values, architecture comparisons", "Weekly exception note; monthly review"),
              ("Agronomy / inputs", "Plan planting, irrigation and input purchase",
               "Yield range, weather drivers, regime caveat, state split",
               "Price-model diagnostics", "Seasonal, before the planting window"),
              ("Policy / buffer stock", "Size the buffer and time releases",
               "Scenario range, bias, structural-break log, distributional note",
               "A single point forecast presented as a target", "Quarterly and event-driven"),
              ("Data / modelling", "Retrain, recalibrate or retire",
               "Full scorecard, calibration drift, failing segments, fold file",
               "Nothing; this is the audit audience", "Monthly"),
              ("External / public", "Understand the outlook without acting on advice",
               "Plain-language range, source, limitation, disclaimer",
               "Actionable trading or agronomic advice", "As published"),
          ],
          [2.6, 3.6, 4.4, 3.6, 2.4], size=7.8, first_col_bold=True,
          caption_text="Stakeholder message matrix: one evidence base, six decision contexts.")

    h2(doc, "5.6  Reporting a failure: the three-month horizon")

    para(doc,
         f"The three-month horizon fails the accuracy gate. The best candidate, SARIMAX, has a MASE "
         f"against the random walk of {F.num(F.score(3,'SARIMAX')['mase_rw'],3)}; the ensemble is "
         f"{F.num(F.score(3,'Ensemble')['mase_rw'],3)}. The failure is small in absolute terms and real in "
         "gate terms. The reporting protocol treats it as a first-class result, not an embarrassment.")

    table(doc,
          ["Step", "What the report says", "Why"],
          [
              ("State the finding", "“At three months, no candidate beats the random walk on the pre-registered gate.”",
               "The reader hears the result before the explanation"),
              ("Show the evidence", "MASE table, paired interval, and the fold-level chart",
               "A claim without a table is an assertion"),
              ("Quantify the impact", "The random-walk MAE is 21.3 USD/MT; the best candidate is 21.9",
               "The operational difference is small; the claim difference is large"),
              ("Name the cause", "Flat exogenous assumptions, quarterly horizon, and the random walk’s advantage in tranquil periods",
               "A cause is a hypothesis for the next test, not an excuse"),
              ("State the action", "Publish the random-walk forecast at h=3; keep the model in shadow; review in 90 days",
               "A failure without an action becomes a recurring surprise"),
              ("Assign the owner", "Model validator, with the business owner informed",
               "Accountability is part of the result"),
          ],
          [3.0, 8.4, 5.2], size=8.0, first_col_bold=True,
          caption_text="Failure protocol: how a gate failure is reported, explained and acted on.")

    para(doc,
         "The protocol has a second purpose. A team that reports failures visibly is a team that can be "
         "trusted when it reports a pass. The alternative — publishing only the favourable horizons — "
         "produces a report that looks stronger and is worth less.")

    h2(doc, "5.7  Cadence, triggers and version control")

    para(doc,
         "Reporting is a schedule plus a set of triggers. The schedule keeps the evidence current; the "
         "triggers stop the team from waiting for the next scheduled review when the world has changed. "
         "Every artefact carries a model version, a data vintage and a code hash, so a number can be "
         "traced to the exact run that produced it.")

    table(doc,
          ["Cadence or trigger", "Artefact", "Owner", "Decision it supports"],
          [
              ("Weekly", "Exception note: only forecasts outside the band, data gaps, or a coverage breach", "Data steward",
               "Escalate or suppress a publication"),
              ("Monthly", "One-page decision memo and updated scorecard", "Model validator",
               "Continue, pause or recalibrate"),
              ("Quarterly", "Full evaluation report and limitation review", "Independent validator",
               "Promote, demote or retire a model"),
              ("Annually", "Model risk review and documentation refresh", "Release approver",
               "Renew the mandate"),
              ("Coverage drift > 5 points", "Calibration alert and recalibration note", "Model validator",
               "Widen, recalibrate or stop publishing the interval"),
              ("MASE drift > 10% for 3 months", "Performance alert and root-cause note", "Model owner",
               "Retrain, switch to benchmark or retire"),
              ("Policy or trade shock", "Immediate re-run with a regime flag", "Business owner and validator",
               "Suspend the model or publish with a widened band"),
              ("Data vintage change", "Reproducibility check and version bump", "Data steward",
               "Confirm that the reported numbers still hold"),
          ],
          [3.8, 6.8, 3.2, 2.8], size=8.0, first_col_bold=True,
          caption_text="Reporting cadence, trigger conditions, owners and the decision each artefact supports.")

    h2(doc, "5.8  The recommendation log")

    para(doc,
         "The strategy ends with decisions, not observations. The log below is the bridge from evaluation "
         "to operation. Each recommendation has an owner, a date and a success criterion, so that the next "
         "review can ask whether it worked rather than whether it was mentioned.")

    table(doc,
          ["Recommendation", "Scope", "Owner", "Success criterion", "Review"],
          [
              ("Publish h=1, h=6 and h=12 as benchmark-relative ranges, with the statistical caveat",
               "External and internal reporting", "Release approver",
               "No release note claims superiority without a CI excluding zero", "Monthly"),
              ("Publish the random walk at h=3; keep the model in shadow",
               "Three-month horizon", "Model validator",
               "Random-walk benchmark published; shadow error logged", "90 days"),
              ("Prohibit directional and trading use",
               "Procurement and sales", "Business owner",
               "No decision log cites the model as a direction signal", "Quarterly"),
              ("Recalibrate intervals with regime-weighted conformal residuals",
               "All horizons", "Model owner",
               "h=12 coverage within five points of nominal on a held-out period", "6 months"),
              ("Run a shadow deployment of the buy-now threshold",
               "Procurement", "Business owner",
               "Regret lower than always-wait after costs, out of sample", "6 months"),
              ("Add mandi arrivals, spatial basis and policy events to the feature set",
               "Data and model", "Data steward and model owner",
               "At least one failing crop clears the gate without per-crop tuning", "12 months"),
              ("Replace the single-number promotion rule with the four-gate protocol",
               "Governance", "Independent validator",
               "Every release note carries G0–G4 status", "Immediate"),
          ],
          [6.0, 3.2, 2.8, 3.4, 1.2], size=7.8, first_col_bold=True,
          caption_text="Recommendation log: the decisions that follow from the evaluation, with owners and success criteria.")


def section_6(doc):
    h1(doc, "6.  Limitations: What This Evaluation Cannot Establish", page_break=True)

    para(doc,
         "A limitations section is not a disclaimer. It is a map of the boundary between what the evidence "
         "supports and what the reader might reasonably infer. The boundaries below are specific, "
         "evidenced and, where possible, quantified. Each one implies a refinement, which Section 7 "
         "prioritises.")

    h2(doc, "6.1  A taxonomy of limitation")

    table(doc,
          ["Family", "What it covers", "Typical symptom", "Where it bites"],
          [
              ("Data", "Coverage, vintage, revision, aggregation and missingness",
               "The backtest is clean but the live input is late, revised or unobserved",
               "Every forecast that uses a published series"),
              ("Statistical", "Sample size, dependence, non-stationarity, multiple testing",
               "A confident point estimate that does not survive a different fold set",
               "Significance claims and model rankings"),
              ("Methodological", "Target definition, feature set, model class, loss function",
               "The model answers a slightly different question from the one the business asks",
               "Decision relevance and transfer"),
              ("Decision", "Costs, incentives, adoption and the forecast-to-action gap",
               "A good forecast that no one uses, or a bad decision made with a good forecast",
               "Operational value"),
              ("Governance", "Accountability, transparency, licensing and advice risk",
               "No one can say who owns the claim, or the model becomes uncontestable",
               "Publication and long-run trust"),
          ],
          [2.6, 6.4, 4.2, 3.4], size=8.0, first_col_bold=True,
          caption_text="Five families of limitation and the point at which each one enters the decision.")

    h2(doc, "6.2  Data limitations")

    para(doc,
         "The executed evidence uses global benchmark prices, not Indian mandi prices. That is a "
         "deliberate choice for reproducibility, and it is also the largest external-validity limitation "
         "in the document. The two series differ in level, volatility, seasonality and policy exposure. A "
         "model that is benchmark-equivalent on US HRW wheat may be better or worse on Nashik onion, and "
         "this evaluation cannot tell you which.")

    bullet(doc, "Agmarknet does not cover every transaction. Thin markets, "
                "direct farm-gate sales and inter-state flows are under-represented. A model trained on "
                "reported mandi prices can be systematically wrong where the reported market is not the "
                "relevant market.",
           lead="Coverage bias in mandi data. ")
    bullet(doc, "Daily prices are published with a lag and revised. A "
                "feature that looks available at the origin may not have been available to a decision-maker "
                "on that date. The Week 4 leakage checklist addresses the modelling side; it cannot "
                "manufacture a real-time feed.",
           lead="Publication lag and revision. ")
    bullet(doc, "The modal price is the most common price, not the "
                "transacted average. It can hide quality premia, quantity discounts and the difference "
                "between a headline quote and a realised contract.",
           lead="Modal versus transaction price. ")
    bullet(doc, "State-level averages hide district heterogeneity. A "
                "state forecast can be right while every district is wrong in offsetting directions.",
           lead="Aggregation. ")
    bullet(doc, "The global panel has no arrivals, warehouse stocks, "
                "trade policy events, freight costs or exchange rates. These are precisely the variables "
                "that break a price forecast during a shock.",
           lead="Omitted drivers. ")
    bullet(doc, "Prices are nominal US dollars. Inflation and exchange-rate "
                "movements are inside the series, not modelled separately. A nominal forecast can be "
                "accurate and economically misleading.",
           lead="Nominal values. ")
    bullet(doc, "The modern window begins in 2000. The 1990s liberalisation, "
                "the 2007–08 food crisis and the 2011–12 drought are represented only partially, which "
                "limits the model’s experience of extreme regimes.",
           lead="Window truncation. ")

    h2(doc, "6.3  Statistical limitations")

    para(doc,
         f"The harness has {F.META['n_folds']} folds, which sounds like a large sample and is not. "
         "Adjacent folds share 12-month targets, so the errors are correlated; the effective independent "
         "sample is closer to the number of non-overlapping 12-month blocks, roughly fifteen. That is the "
         "sample that supports the confidence intervals, and it is why the intervals are wide.")

    bullet(doc, "Twenty candidate-horizon comparisons are made. "
                "At a 5% threshold, one false positive is expected by chance. The report shows the "
                "uncorrected p-values for transparency and does not treat any of them as a discovery.",
           lead="Multiple comparisons. ")
    bullet(doc, "The series is non-stationary. Coefficients and "
                "error variances change across regimes; a model that is stable in one period can invert in "
                "the next. The regime table in Section 3.6 shows exactly this inversion.",
           lead="Non-stationarity. ")
    bullet(doc, "Conformal coverage assumes exchangeability between "
                "calibration and test residuals. A regime shift violates that assumption, which is why "
                "h=12 coverage falls to 79%. The method is distribution-free, not assumption-free.",
           lead="Exchangeability. ")
    bullet(doc, "Parameter uncertainty is not propagated into the "
                "forecast interval. The conformal band captures past forecast error, not the uncertainty "
                "of the estimated coefficients. In a short sample the second component can be material.",
           lead="Parameter uncertainty. ")
    bullet(doc, "The five crops are not independent. Common energy, "
                "freight and policy shocks induce cross-correlation. Treating them as five independent "
                "replications overstates the evidence for transfer.",
           lead="Cross-sectional dependence. ")
    bullet(doc, "The five crops were chosen for commercial diversity, not "
                "at random. They are not a representative sample of Indian agriculture, and the "
                "cross-commodity result should not be extrapolated to pulses, oilseeds or horticulture "
                "without a new test.",
           lead="Selection of crops. ")

    h2(doc, "6.4  Methodological limitations")

    bullet(doc, "The primary target is a univariate price. The model does "
                "not estimate a supply-and-demand system, so it cannot answer “what happens to price if "
                "the export ban is lifted?”. Scenario analysis can, but only with an explicit "
                "transmission assumption.",
           lead="Reduced-form target. ")
    bullet(doc, "Fertilizer prices are held flat over the forecast "
                "block. This is conservative for cost-push inflation and optimistic for a fertilizer "
                "spike. The choice is documented but not tested for sensitivity.",
           lead="Flat exogenous assumptions. ")
    bullet(doc, "The ladder is deliberately small: ETS, SARIMAX, a "
                "direct GBDT and an inverse-MSE ensemble. It is a fair test of the framework, not a "
                "search over the state of the art. A transformer or a hierarchical Bayesian model might "
                "do better; this evaluation cannot say.",
           lead="Limited model class. ")
    bullet(doc, "Each crop is modelled separately. A hierarchical "
                "model that borrows strength across states and crops could improve the thin segments, but "
                "it also imposes a pooling assumption that may be wrong. The current design avoids the "
                "assumption rather than testing it.",
           lead="No pooling. ")
    bullet(doc, "Ensemble weights are inverse-MSE and can be unstable when "
                "the members’ errors are correlated. A stacking model with a stability constraint is a "
                "candidate refinement, not a current feature.",
           lead="Unstable ensemble weights. ")
    bullet(doc, "A backtest is not a live deployment. It cannot capture "
                "latency, data revisions, operational errors, or the behavioural response of users to the "
                "forecast. Shadow deployment is the only way to test those.",
           lead="Backtest–live gap. ")
    bullet(doc, "The cost ratio of 4:1 is an assumption, not a "
                "measurement. A different ratio changes the cost-weighted ranking and the optimal "
                "threshold. The ratio should be calibrated with the procurement team before the "
                "threshold is used.",
           lead="Cost parameters. ")

    h2(doc, "6.5  Decision and organisational limitations")

    para(doc,
         "The evaluation measures forecast quality. It does not measure whether the organisation will use "
         "the forecast well. A procurement team measured on price paid may prefer to wait, even when the "
         "model says buy; a sales team measured on volume may prefer to promise availability, even when "
         "the model says the margin is thin. These incentive effects are outside the model and inside the "
         "outcome.")

    bullet(doc, "The threshold rule is an in-sample optimum. It has not "
                "been tested on a live decision stream, and it may not survive transaction costs, "
                "counterparty constraints or the behaviour of other buyers.",
           lead="In-sample threshold. ")
    bullet(doc, "The forecast is one input to a decision that also "
                "involves contracts, storage, credit and relationships. A model that ignores those "
                "constraints can recommend a purchase the organisation cannot execute.",
           lead="Forecast-to-action gap. ")
    bullet(doc, "If the model is used widely, its predictions can "
                "influence the behaviour they are trying to predict. A buy signal that moves enough "
                "volume becomes self-defeating. The evaluation cannot estimate this feedback.",
           lead="Reflexivity. ")
    bullet(doc, "The report is written in English and assumes a reader "
                "comfortable with percentages and ranges. Field staff and farmers may need a different "
                "representation, tested with actual users rather than assumed.",
           lead="Literacy and language. ")

    h2(doc, "6.6  Ethical and governance limitations")

    bullet(doc, "A price forecast can be read as advice to sell or "
                "hold. The report must state that it is decision support, not agronomic or investment "
                "advice, and must not be distributed as a recommendation to farmers without a human "
                "intermediary.",
           lead="Advice risk. ")
    bullet(doc, "A widely used forecast can become a coordination "
                "device. If large buyers act on the same signal, the market outcome is affected. The "
                "governance question is not only whether the forecast is accurate but who gets it first.",
           lead="Market power. ")
    bullet(doc, "The model is trained on public data but the derived "
                "scorecard and the code are the organisation’s intellectual property. The release note "
                "should state the licence and the attribution requirements of the underlying sources.",
           lead="Licensing. ")
    bullet(doc, "A single model used by every decision-maker is a "
                "single point of failure. The benchmark forecast should remain available as a fallback, "
                "and the model should be contestable by an independent validator.",
           lead="Model monoculture. ")

    h2(doc, "6.7  What this evaluation cannot tell you")

    table(doc,
          ["Question a reader might ask", "Why the current evaluation cannot answer it"],
          [
              ("Will the model work on Nashik onion prices?", "The executed evidence is global wheat; the mandi panel has different coverage, volatility and policy exposure."),
              ("Is the model better than a human expert?", "No expert forecast was collected on the same folds; the comparison would need a prospective, blinded design."),
              ("What happens if the export ban is lifted?", "The model is reduced-form; it does not identify a policy transmission channel. A scenario with an explicit assumption is required."),
              ("Will the forecast improve procurement profit?", "Only a shadow deployment or a controlled pilot can measure the decision value after costs and behaviour."),
              ("Is the model fair across states and farm sizes?", "The evaluation is at crop level; distributional and equity analysis requires state, district and farm-size data that are not in the panel."),
              ("Will the relationship hold next year?", "The backtest cannot certify the future. It can only state the conditions under which the relationship held in the past."),
              ("Is 2% better than a random walk worth the maintenance cost?", "The evaluation quantifies the error difference, not the total cost of ownership. That is a business case, not a statistical result."),
              ("Can the interval be trusted at h=12?", "Backtest coverage is 79% against a nominal 90%; the interval is approximate and must be recalibrated before it is published as a 90% band."),
          ],
          [6.4, 10.2], size=8.2, first_col_bold=True,
          caption_text="Explicit limits of the evidence: questions the current evaluation is not designed to answer.")

    h2(doc, "6.8  The limitation register")

    para(doc,
         "The register converts the narrative into an operating list. Each limitation has an evidence "
         "signal, a severity, a mitigation and an owner. The severity is a judgement, not a measurement; "
         "it is recorded so that a reader can challenge the priority rather than the existence of the "
         "limitation.")

    table(doc,
          ["Limitation", "Evidence", "Severity", "Mitigation", "Owner", "Trigger"],
          [
              ("Global benchmark, not mandi prices", "Data source mismatch", "High",
               "Replicate on the Indian panel; report both", "Data steward", "Before any India release"),
              ("h=12 interval under-covers", "79% empirical vs 90% nominal", "High",
               "Regime-weighted conformal; publish as approximate 80%", "Model owner", "Immediately"),
              ("Direction near chance", "46.7-55.0% DA; CI includes 50%", "High",
               "Prohibit timing use; collect a prospective signal test", "Business owner", "Immediately"),
              ("Underpowered for small effects", "MDE 11% vs observed 2%", "Medium",
               "Extend folds, pool crops, or accept parity", "Validator", "Next review"),
              ("h=3 gate failure", "MASE 1.01–1.04", "Medium",
               "Publish benchmark; shadow the model", "Validator", "90 days"),
              ("Regime sign inversion", "Pre/post-2023 MASE reverses", "Medium",
               "Regime-conditional reporting; rolling recalibration", "Model owner", "Quarterly"),
              ("Flat fertilizer exog", "Assumption in forecast block", "Medium",
               "Scenario the input cost; test sensitivity", "Model owner", "Next release"),
              ("Cost ratio is assumed", "4:1 not calibrated", "Medium",
               "Calibrate with procurement; rerun CWE", "Business owner", "Before threshold use"),
              ("No live decision test", "Backtest only", "High",
               "Shadow deployment for 90 days", "Business owner", "Next quarter"),
              ("Cross-crop dependence", "Common shocks", "Low",
               "Report as five correlated cases, not five replications", "Validator", "Documentation"),
          ],
          [3.4, 3.6, 1.5, 4.0, 2.3, 1.8], size=7.6, first_col_bold=True,
          caption_text="Limitation register: evidence, severity, mitigation, owner and trigger.")

    callout(doc, "THE LIMITATION THAT MATTERS MOST",
            "The evaluation is honest about accuracy but cannot establish decision value. That requires a "
            "shadow deployment with real buyers, real costs and real incentives. Until then, every "
            "recommendation in this report is a hypothesis about value, not a measurement of it.")
