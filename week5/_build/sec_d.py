# -*- coding: utf-8 -*-
"""Sections 7-8 and appendices A-F."""

from pathlib import Path

from docbase import (h1, h2, h3, para, bullet, table, callout, figure,
                     spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
import facts as F

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
H = F.HORIZONS


def section_7(doc):
    h1(doc, "7.  Refinement Roadmap: What to Build, in What Order", page_break=True)

    para(doc,
         "The evaluation does not end with a verdict. It ends with a ranked list of investments that "
         "would change the verdict. The list below is scored on impact, confidence and effort, and "
         "sequenced so that the cheapest evidence comes first. The ordering is deliberately biased toward "
         "learning rather than modelling: a shadow deployment that measures decision value is worth more "
         "than a more sophisticated model that no one has tested in use.")

    h2(doc, "7.1  How the backlog is prioritised")

    para(doc,
         "Each initiative is scored from 1 to 5 on three dimensions. Impact is the expected change in the "
         "decision, not in the metric. Confidence is the strength of the evidence that the initiative will "
         "deliver the impact. Effort is the people-weeks and data-access cost. The priority score is "
         "impact × confidence ÷ effort; it is a conversation starter, not an oracle. The horizon column "
         "records when the initiative can realistically produce evidence.")

    table(doc,
          ["Rank", "Initiative", "Type", "Impact", "Conf.", "Effort", "Score", "Horizon", "Success criterion"],
          [
              ("1", "Shadow-deploy the buy-now threshold with real procurement decisions", "Decision", "5", "5", "2", "12.5", "0–90 days",
               "Regret below always-wait after costs, out of sample"),
              ("2", "Test the decision memo and fan chart with non-specialist readers", "Reporting", "3", "4", "1", "12.0", "0–90 days",
               "80% of readers correctly state the range and the permitted use"),
              ("3", "Automate the scorecard and one-screen dashboard from the fold file", "Reporting", "4", "5", "2", "10.0", "0–90 days",
               "Zero hand-typed numbers in the monthly memo"),
              ("4", "Regime-weighted conformal recalibration of intervals", "Model", "4", "4", "2", "8.0", "3–6 months",
               "h=12 coverage within five points on a held-out period"),
              ("5", "Add a stability constraint to the ensemble weights", "Model", "2", "4", "1", "8.0", "3–6 months",
               "Weight dispersion across folds falls by half without a loss in MAE"),
              ("6", "Add mandi arrivals, spatial basis and warehouse stocks", "Data", "5", "4", "3", "6.7", "6–12 months",
               "At least one failing crop clears the gate without per-crop tuning"),
              ("7", "Pre-register and run an A/B threshold test", "Evaluation", "4", "4", "3", "5.3", "3–6 months",
               "A threshold beat the default rule with a pre-registered test"),
              ("8", "Add a policy and trade event calendar with dated flags", "Data", "5", "3", "3", "5.0", "6–12 months",
               "Policy-shock folds are identified before the forecast, not after"),
              ("9", "Extend the history before 2000 and test pre-liberalisation stability", "Data", "3", "3", "2", "4.5", "6–12 months",
               "The sign of the advantage is unchanged in the extended window"),
              ("10", "Build a hierarchical panel model across states and crops", "Model", "4", "3", "4", "3.0", "6–12 months",
               "Thin segments improve without degrading the pooled result"),
              ("11", "Test weekly-frequency data and a mixed-frequency model", "Data", "4", "3", "4", "3.0", "6–12 months",
               "Weekly information improves h=1 without breaking calibration"),
              ("12", "Train on a decision-weighted loss rather than MAE", "Model", "4", "2", "4", "2.0", "12 months",
               "CWE improves on a held-out period without a material MAE loss"),
          ],
          [1.0, 5.0, 1.8, 1.2, 1.1, 1.1, 1.1, 1.6, 2.7], size=7.4, first_col_bold=True,
          caption_text="Refinement backlog: ranked by impact × confidence ÷ effort, with a success criterion for each item.")

    h2(doc, "7.2  Model refinements")

    para(doc,
         "The first model refinement is not a bigger model; it is a more honest one. Regime-weighted "
         "conformal calibration addresses the h=12 under-coverage directly. Instead of pooling all past "
         "residuals, it weights recent folds more heavily and widens the band when the local error "
         "variance rises. The method is still distribution-free, but it stops assuming that the 2011–2022 "
         "error distribution is the right reference for 2026.")

    para(doc,
         "The second is a hierarchical panel. The current design fits each crop separately, which is "
         "robust but wasteful in thin segments. A partial-pooling model borrows strength across states "
         "and crops while allowing each segment its own level. The risk is that pooling imports a "
         "relationship that does not hold locally; the reward is a usable forecast for the segments where "
         "a standalone model has too few observations. The right test is a pre-registered comparison on "
         "the failing crops, not a global replacement.")

    para(doc,
         "The third is a stability constraint on the ensemble. Inverse-MSE weights are optimal in "
         "expectation and unstable in practice when the members are correlated. A constrained stack — "
         "weights bounded, smoothed across folds, and shrunk toward equal weights when the evidence is "
         "thin — is likely to give up a negligible amount of in-sample accuracy for a meaningful gain in "
         "fold-to-fold reliability. The evaluation should judge it on rank stability, not only on MAE.")

    para(doc,
         "The fourth is a decision-weighted loss. If the business truly faces a 4:1 asymmetry, training on "
         "symmetric error is a mismatch. A pinball or asymmetric loss can be used directly, but it must be "
         "tested against the same pre-registered gate. A model that improves CWE while degrading MAE is "
         "not automatically better; it is a different trade-off that the business owner must accept "
         "explicitly.")

    h2(doc, "7.3  Data refinements")

    para(doc,
         "The largest expected gain is data, not architecture. The failing crops are the ones most exposed "
         "to arrivals, stocks and policy. Adding mandi arrivals and the spatial basis — the difference "
         "between the local and the national price — gives the model a supply signal it currently lacks. "
         "Warehouse stocks and import/export clearance data add a second. A dated policy-event calendar "
         "turns an unmodelled shock into a known regime flag, which is exactly what the 2023 split shows "
         "the model needs.")

    para(doc,
         "Higher-frequency data is the second frontier. Weekly mandi prices, rainfall nowcasts and "
         "satellite vegetation indices can improve the one-month horizon without changing the model class. "
         "The risk is that higher frequency also brings more noise and more publication irregularity. The "
         "evaluation must test the information gain, not just the data volume.")

    h2(doc, "7.4  Evaluation refinements")

    para(doc,
         "The evaluation itself needs three upgrades. First, prequential evaluation: score each forecast "
         "as it is made, not only in a retrospective batch. This closes the gap between backtest and live "
         "behaviour and detects drift earlier. Second, a proper power calculation before the next run, so "
         "that the team knows whether the design can detect the effect it hopes to find. Third, a "
         "decision-focused test with a pre-registered threshold, because the current decision analysis is "
         "an in-sample sweep, not a prospective trial.")

    para(doc,
         "A fourth upgrade is multiple-comparison discipline. The harness reports twenty tests. The next "
         "version should declare a family of tests in advance, apply a correction, and report the "
         "corrected interval alongside the uncorrected one. This is not a statistical nicety; it is the "
         "difference between a finding and a search.")

    h2(doc, "7.5  Reporting refinements")

    para(doc,
         "The report is already structured around the decision, but it has not been tested with the people "
         "who will use it. A short comprehension study — ten procurement staff, five minutes, four "
         "questions about the range and the permitted use — would tell us whether the fan chart and the "
         "four-box summary work. If readers cannot state the range after reading the page, the page has "
         "failed, regardless of the model’s MASE.")

    para(doc,
         "The second reporting refinement is automation. The monthly memo should be generated from the "
         "fold file and the scorecard, with no hand-typed numbers. Automation does not remove judgement; "
         "it removes the opportunity for a transcription error to masquerade as a finding.")

    h2(doc, "7.6  The 12-month roadmap")

    table(doc,
          ["Phase", "Milestones", "Exit criteria"],
          [
              ("0–90 days", "Shadow-deploy the threshold; test the memo with readers; automate the scorecard; recalibrate the h=12 interval; publish the h=3 benchmark",
               "A monthly memo with zero hand-typed numbers; a reader comprehension rate of at least 80%; a calibrated 90% band at h=12; an h=3 page that states the failure"),
              ("3–6 months", "Run the A/B threshold test; add the stability constraint; begin the arrivals and basis data work; pre-register the next evaluation",
               "A pre-registered decision test with a result; ensemble rank stability above 70%; a data contract for arrivals and basis"),
              ("6–12 months", "Test the hierarchical panel; add the policy-event calendar; extend the history; publish the second evaluation report",
               "At least one failing crop clears the gate without per-crop tuning; the policy-shock folds are identified ex ante; the extended window does not reverse the sign"),
          ],
          [2.6, 8.4, 5.6], size=8.0, first_col_bold=True,
          caption_text="Twelve-month roadmap: three phases, each with a milestone and an exit criterion.")

    h2(doc, "7.7  Stop rules")

    para(doc,
         "A refinement roadmap needs a retirement rule as much as a build rule. The following conditions "
         "stop publication or trigger a mandatory review. They are pre-registered, so that stopping is a "
         "decision rather than a reaction.", space_after=4)
    bullet(doc, "MASE against the random walk above 1.10 for three consecutive "
                "months at the published horizon.", lead="Performance stop. ")
    bullet(doc, "Empirical 90% coverage below 80% for two consecutive quarters, "
                "or a drift of more than ten points from the calibration baseline.", lead="Calibration stop. ")
    bullet(doc, "The input data vintage cannot be verified, or a source changes "
                "its definition without a backfill.", lead="Provenance stop. ")
    bullet(doc, "A policy or trade shock invalidates the regime assumption and the "
                "model has not been re-estimated on post-shock data.", lead="Regime stop. ")
    bullet(doc, "The cost of maintaining the model exceeds the measured decision "
                "value for two consecutive reviews.", lead="Value stop. ")

    h2(doc, "7.8  How we will know the evaluation system is working")

    para(doc,
         "The evaluation system is itself a product. It should be judged on whether it improves decisions, "
         "not only on whether it produces reports. Five indicators are proposed. They are deliberately "
         "few, measurable and hard to game.")

    table(doc,
          ["Indicator", "Baseline (this report)", "Target", "Why it matters"],
          [
              ("Claims with a confidence interval", "100% of headline claims", "100%", "Prevents overclaiming"),
              ("Gate failures with an action", "1 of 1 (h=3)", "100%", "Tests the failure protocol"),
              ("Data release to decision memo", "Not measured", "< 10 working days", "Measures operational fitness"),
              ("Reader comprehension of the range", "Not measured", "≥ 80%", "Tests the visual system"),
              ("Reproducibility of a published number", "Reproduced within 0.01%", "100% within 0.1%", "Makes the audit credible"),
          ],
          [4.8, 4.4, 2.8, 4.6], size=7.6, first_col_bold=True,
          caption_text="Success indicators for the evaluation system, not only for the model.")


def section_8(doc):
    h1(doc, "8.  Conclusion: From Accuracy to Accountability", page_break=True)

    para(doc,
         "The most useful result in this evaluation is not a forecast. It is the demonstration that a "
         "well-built model can pass the accuracy gate and still fail the claims that matter. The ensemble "
         "is 2.1% closer to the outcome than a random walk at one month, and that difference is "
         "indistinguishable from zero once sampling uncertainty is counted. It is no better at direction. "
         "Its twelve-month interval under-covers. Those are not reasons to abandon the work; they are the "
         "reasons the work is worth doing carefully.")

    para(doc,
         "The strategy that emerges is deliberately modest. Publish benchmark-relative ranges for the "
         "horizons that clear the gate. Publish the random walk where the gate fails. Prohibit directional "
         "use until a prospective test supports it. Recalibrate the long-horizon interval before it is "
         "shown to a decision-maker. Test the decision value in shadow deployment before claiming it. Each "
         "of these is a smaller claim than the design target promised, and each is a claim the evidence "
         "can carry.")

    para(doc,
         "The wider lesson is about the relationship between evaluation and credibility. A team that "
         "reports a 2% edge with a confidence interval, names the horizon that fails, and states the "
         "condition that would change its mind is more credible than a team that reports a 46% edge and "
         "cannot reproduce it. The first team will be believed when it eventually has a strong result. The "
         "second will be audited, and the audit will not go well.")

    callout(doc, "THE ONE-PAGE ANSWER",
            "Use the model as a planning range at one, six and twelve months. Do not claim it beats a "
            "random walk; the evidence does not support that claim. Do not use it for direction; the "
            "evidence does not support that either. Publish the random walk at three months. Recalibrate "
            "the long-horizon interval. Test the decision value in a shadow deployment. Review in ninety "
            "days, or immediately after a policy shock.")

    h2(doc, "8.1  Release decision record")

    para(doc,
         "The record below is the version a validator can sign. It separates what the evidence permits "
         "from what it forbids, and it names the condition that reopens each decision.")

    table(doc,
          ["Decision area", "Evidence", "Permitted use", "Prohibited use", "Review trigger"],
          [
              ("Accuracy, h=1, 6, 12", "Gate passed; parity with random walk",
               "Planning ranges and budget scenarios", "A claim of superior accuracy",
               "Twelve new monthly outcomes; re-run the audit"),
              ("Accuracy, h=3", "Gate failed (MASE 1.041 for the ensemble)",
               "Publish the random walk as the benchmark", "A model forecast at h=3",
               "Model revision with a pre-registered test"),
              ("Direction", "Chance-level, 46.7-55.0% across horizons",
               "Scenario discussion only", "Trading or daily timing",
               "A prospective directional test"),
              ("Calibration, h=12", "78.8% empirical vs 90% nominal",
               "An approximate 80% planning band", "A stated 90% band",
               "Regime-weighted recalibration"),
              ("Decision value", "In-sample threshold gain; no live test",
               "Shadow deployment only", "A production procurement rule",
               "Prospective cost and regret test"),
          ],
          [3.3, 3.9, 3.4, 3.0, 3.0], size=7.4, first_col_bold=True,
          caption_text="Release decision record: what the evidence permits, what it forbids and what reopens the question.")


def appendix_a(doc):
    h1(doc, "Appendix A.  Formulae and Worked Calculations", page_break=True)

    para(doc,
         "The formulae below are the exact definitions used by evaluation_engine.py. The worked values "
         "are for the ensemble at h=1 on the wheat panel, using all 60 folds unless a metric requires the "
         "52 folds for which a conformal interval had been issued.")

    table(doc,
          ["Quantity", "Definition", "Worked value (ENS, h=1)"],
          [
              ("MAE", "mean |y − ŷ|", f"{F.num(F.score(1,'Ensemble')['mae'],4)} USD/MT"),
              ("RMSE", "√mean (y − ŷ)²", f"{F.num(F.score(1,'Ensemble')['rmse'],4)} USD/MT"),
              ("MAPE", "100 · mean |y − ŷ| / |y|", f"{F.num(F.score(1,'Ensemble')['mape'],3)}%"),
              ("sMAPE", "200 · mean |y − ŷ| / (|y| + |ŷ|)", f"{F.num(F.score(1,'Ensemble')['smape'],3)}%"),
              ("Scale", "mean |Δy| over the first 120 months", f"{F.num(F.META['scale'],4)} USD/MT"),
              ("MASE (absolute)", "MAE / scale", f"{F.num(F.score(1,'Ensemble')['mase'],4)}"),
              ("MASE vs RW", "MAE / MAE(RW) on the same folds", f"{F.num(F.score(1,'Ensemble')['mase_rw'],4)}"),
              ("MASE vs SN", "MAE / MAE(SN) on the same folds", f"{F.num(F.score(1,'Ensemble')['mase_sn'],4)}"),
              ("R²", "1 − SSE / SST", f"{F.num(F.score(1,'Ensemble')['r2'],4)}"),
              ("Bias", "mean (ŷ − y)", f"{F.signed(F.score(1,'Ensemble')['bias'],4)} USD/MT"),
              ("MPE", "100 · mean (ŷ − y) / y", f"{F.signed(F.score(1,'Ensemble')['mpe'],3)}%"),
              ("Directional accuracy", "share of correct signs vs origin", f"{F.num(F.score(1,'Ensemble')['da'],1)}%"),
              ("Pinball loss", "mean of 5% and 95% quantile losses", f"{F.num(F.score(1,'Ensemble')['pinball'],4)} USD/MT"),
              ("Coverage 90%", "share inside the 90% interval", f"{F.num(F.score(1,'Ensemble')['coverage90'],2)}%"),
              ("Width 90%", "mean (upper − lower)", f"{F.num(F.score(1,'Ensemble')['width90'],2)} USD/MT"),
              ("Winkler 90%", "width + miss penalty", f"{F.num(F.score(1,'Ensemble')['winkler90'],2)} USD/MT"),
              ("CWE", "mean asymmetric absolute loss (4:1)", f"{F.num(F.score(1,'Ensemble')['cwe'],4)} USD/MT"),
          ],
          [3.2, 7.4, 6.0], size=8.2, first_col_bold=True,
          caption_text="Metric definitions and the exact values for the ensemble at h=1.")

    para(doc,
         "A note on the scale term. The denominator of absolute MASE is the mean absolute first difference "
         f"over the first 120 months, {F.num(F.META['scale'],4)} USD/MT. The evaluation-period random walk "
         f"has a larger MAE ({F.num(F.score(1,'Random Walk')['mae'],4)}), which is why the absolute MASE is "
         f"above 1.0 while the relative MASE is below 1.0. The two numbers answer different questions: the "
         "first compares the model with the volatility of the early sample, the second with the benchmark "
         "on the same folds. Both are correct; only the second is a promotion gate.")

    para(doc,
         "The interval metrics use the 52 folds with a conformal interval (the first eight folds have no "
         "prior residual pool). Pinball loss is the average of the 5% and 95% quantile losses, each "
         "computed with the standard asymmetric formula. The Winkler score uses α = 0.10, so a miss is "
         "penalised at 20 times its distance beyond the band. The cost-weighted error uses c_u = 1.00 and "
         "c_o = 0.25; the ratio is a business assumption, not a statistical estimate.")


def appendix_b(doc):
    h1(doc, "Appendix B.  Pre-Registration Form and Evaluation Checklist", page_break=True)

    para(doc,
         "The form is completed before the run and signed by the validator. It is short because a long "
         "form is not completed. The completed example is the actual pre-registration for this report.")

    table(doc,
          ["Field", "Completed entry"],
          [
              ("Report / model version", "Week 5 audit, ladder v1.0; Base model: Week 4 six-rung ladder"),
              ("Claim under test", "The ensemble reduces MAE against a random walk at one, three, six and twelve months"),
              ("Primary metric", "MASE vs random walk, same folds and horizon"),
              ("Secondary metrics", "MAE, RMSE, sMAPE, R², bias, directional accuracy, pinball loss, coverage, width, Winkler, CWE"),
              ("Benchmarks", "Random walk and seasonal naïve, same folds and horizons"),
              ("Segments", "Five crops, four horizons, two regimes (pre/post-2023), three volatility terciles"),
              ("Fold design", "Expanding window, minimum 120 months, origin step 3 months, 60 folds"),
              ("Success threshold", "MASE < 1.00 against both benchmarks and a paired 95% interval excluding zero"),
              ("Multiple comparisons", "20 candidate-horizon tests; Bonferroni threshold 0.0025 reported alongside uncorrected p-values"),
              ("Failure action", "Publish the benchmark, log the failure, set a 90-day review"),
              ("Data vintage", "World Bank Pink Sheet, 2000-01 to 2026-10, November 2026 edition"),
              ("Owner and date", "Independent validator; signed before the first candidate was fitted"),
          ],
          [4.0, 12.6], size=8.2, first_col_bold=True,
          caption_text="Completed pre-registration form for the Week 5 evaluation.")

    h2(doc, "B.1  The evaluator’s checklist")

    para(doc, "The checklist is run before any number is released. A single unchecked box blocks publication.",
         space_after=4)
    bullet(doc, "The data vintage is recorded, the date range is complete, and no month is missing.")
    bullet(doc, "No feature at the origin uses an observation dated after the origin.")
    bullet(doc, "The scaler, imputer and decomposition are fitted inside each fold, not on the full sample.")
    bullet(doc, "The benchmark is evaluated on exactly the same folds and horizon.")
    bullet(doc, "The metric definition is the pre-registered one, with no post-hoc variant.")
    bullet(doc, "The point estimate is accompanied by a paired interval and a sample size.")
    bullet(doc, "The direction result is accompanied by a binomial interval and a base-rate comparison.")
    bullet(doc, "The interval is accompanied by coverage, width and Winkler score.")
    bullet(doc, "Every segment with a failing result is shown, not only the pooled result.")
    bullet(doc, "The report states the failure condition and the next test.")
    bullet(doc, "A second analyst can reproduce the number from the archived fold file.")
    bullet(doc, "The release note names the owner and the review date.")


def appendix_c(doc):
    h1(doc, "Appendix C.  Executive Summary Template", page_break=True)

    para(doc,
         "The template is printed below in blank form. It fits on one page, uses four boxes and forces the "
         "writer to separate the finding from the range, the decision from the caveat. The worked example "
         "in Section 5.3 shows how it reads when filled.")

    table(doc,
          ["Box", "Prompt", "Length"],
          [
              ("FINDING", "At [horizon], the [model] is [better/worse] than [benchmark] by [metric and value]; the confidence interval is [interval] and the gate is [pass/fail].", "One sentence"),
              ("RANGE", "The point forecast is [value] with a [level] band of [lower]–[upper]. Backtest coverage at this horizon is [value]%, so the band should be read as [interpretation].", "Two sentences"),
              ("DECISION", "Use it for [permitted use]. Do not use it for [prohibited use]. Owner: [name]. Review: [date].", "Two sentences"),
              ("CAVEAT", "The result fails at [segment/horizon] because [evidence]. The minimum detectable effect is [value]. Re-run when [trigger].", "Two sentences"),
          ],
          [2.6, 12.4, 1.6], size=8.6, first_col_bold=True,
          caption_text="The four-box executive summary template in blank form.")

    h2(doc, "C.1  The one-page memo layout")

    para(doc, "The memo is laid out in a fixed order, so that a reader can find the same element on every page:",
         space_after=4)
    bullet(doc, "One line: the decision and the horizon.")
    bullet(doc, "The four boxes, in order: FINDING, RANGE, DECISION, CAVEAT.")
    bullet(doc, "One chart: the fan chart for the headline horizon, with the band labelled.")
    bullet(doc, "One table: the horizon verdict, with MAE, MASE and gate status.")
    bullet(doc, "A footer: data vintage, model version, fold count, owner and review date.")

    para(doc,
         "The memo is not allowed to exceed one page. If it does, the additional material belongs in the "
         "evaluation report, not in the decision memo. The constraint is the point: a decision-maker who "
         "cannot find the decision in one page will not find it in twelve.")


def appendix_d(doc):
    h1(doc, "Appendix D.  Reproduction: Data, Code and Outputs", page_break=True)

    para(doc,
         "Every number in this report is generated by a small, deterministic pipeline and stored in a set "
         "of CSV files. The report builder reads the generated facts file rather than retyping values, so "
         "the prose and the tables cannot drift apart. The environment used for the audit is listed below.")

    table(doc,
          ["Component", "Version / setting"],
          [
              ("Python", "3.14.2"),
              ("pandas", "3.0.0"),
              ("NumPy", "2.4.2"),
              ("statsmodels", "0.15.0"),
              ("scikit-learn", "1.9.1"),
              ("Matplotlib", "3.11.2"),
              ("python-docx", "1.2.0"),
              ("Data source", "World Bank Pink Sheet, prepared CSV in week4/data"),
              ("Data window", f"{F.META['data_start']} to {F.META['data_end']}"),
              ("Design matrix", f"{F.META['n_design']} months × {F.META['n_features']} predictors"),
              ("Primary folds", f"{F.META['n_folds']} per horizon, step {F.META['step']} months"),
              ("Runtime", f"{F.META['runtime_seconds']:.0f} seconds for the full audit on a laptop"),
          ],
          [4.0, 12.6], size=8.4, first_col_bold=True,
          caption_text="Reproduction environment and execution settings.")

    h2(doc, "D.1  Output files")

    table(doc,
          ["File", "Contents"],
          [
              ("fold_predictions_wheat.csv", "1,440 fold-level forecasts with conformal bands"),
              ("fold_predictions_*.csv", "Same for rice, maize, soybeans and cotton"),
              ("metrics_by_horizon.csv", "24 rows: six models × four horizons"),
              ("metrics_by_commodity.csv", "Cross-commodity scorecard"),
              ("calibration.csv", "Nominal vs empirical coverage, 50–95%"),
              ("significance.csv", "Bootstrap intervals, DM tests, MDE"),
              ("regime_metrics.csv", "MASE before and after January 2023"),
              ("volatility_metrics.csv", "MASE by volatility tercile"),
              ("decision_curve.csv", "Cost, regret, hit rate, capture by threshold"),
              ("latest_forecast.csv", "October 2026 forecast and bands"),
              ("facts.json", "Machine-readable fact base for the report"),
          ],
          [5.6, 11.0], size=7.6, first_col_bold=True,
          caption_text="Reproduction outputs: the audit trail behind every number in the report.")

    h2(doc, "D.2  Commands")

    para(doc, "From the repository root:", space_after=4)
    para(doc,
         "python week5/_build/evaluation_engine.py\n"
         "python week5/_build/diagram_generator.py\n"
         "python week5/_build/build_week5.py\n"
         "powershell -ExecutionPolicy Bypass -File week5/_build/export_pdf.ps1\n"
         "python week5/_build/scrub_metadata.py all",
         size=8.4, color=SECONDARY)

    para(doc,
         "The first script executes the ladder and writes the fold-level predictions, metrics, "
         "calibration, significance, regime, volatility, decision and latest-forecast files, plus "
         "facts.json. The second renders the figures. The third assembles the Word document. The fourth "
         "exports the PDF and refreshes the fields. The fifth removes identifying metadata. The scripts "
         "are deterministic: the random seed is fixed at 42, and the model ladder is not tuned per fold.")

    h2(doc, "D.3  Reproducing one published number")

    para(doc,
         "The worked example is the headline h=1 ensemble MAE, 12.0916 USD/MT. It can be rebuilt from "
         "the archived fold file without rerunning the ladder.", space_after=4)
    bullet(doc, "Read week5/data/fold_predictions_wheat.csv and keep the rows where horizon is 1 and "
                "model is L5. The file contains 60 folds for this cell.",
           lead="Load the fold file. ")
    bullet(doc, "Take the absolute difference between actual and forecast, then the mean. The result "
                "should be 12.0916; a difference above 1e-6 means the file and the published number are "
                "out of sync.",
           lead="Recompute the point metric. ")
    bullet(doc, "Repeat the same calculation for model L0 on the same folds, then divide the candidate "
                "MAE by the random-walk MAE. The result is 0.9787, the MASE vs RW in Table 15.",
           lead="Recompute the relative metric. ")
    bullet(doc, "Keep only rows with a non-null lo90 (52 of 60), count the outcomes inside [lo90, hi90], "
                "and divide by 52. The result is 90.4%, the coverage in Table 15.",
           lead="Recompute the interval metric. ")
    bullet(doc, "Run build_week5.py and confirm that the new DOCX carries the same three values. "
                "facts.json is the only bridge between the engine and the prose.",
           lead="Check the build. ")

    para(doc,
         "A reproduction that requires the report builder to retype numbers is not a reproduction. The "
         "chain above is deliberately one-way: fold file → metrics → facts → document, and every link is "
         "a file on disk.")

    table(doc,
          ["Quantity", "Rebuilt from fold file", "Published", "Tolerance"],
          [
              ("h=1 ENS MAE (USD/MT)", "12.0916", "12.0916", "< 1e-6"),
              ("MASE vs RW", "0.9787", "0.9787", "±0.0001"),
              ("90% coverage", "90.4%", "90.4%", "±0.1 pp"),
              ("Coverage sample", "52 folds", "52 folds", "exact"),
          ],
          [5.4, 4.6, 3.2, 3.4], size=7.8, first_col_bold=True,
          caption_text="Reproduction check: three published numbers rebuilt from the archived fold file.")


def appendix_e(doc):
    h1(doc, "Appendix E.  Glossary for Non-Specialist Readers", page_break=True)

    para(doc,
         "The glossary is written for the reader who needs to understand the report, not to reproduce the "
         "model. Each entry is one sentence and avoids a definition that depends on another undefined term.")

    table(doc,
          ["Term", "Plain-language meaning"],
          [
              ("Random walk", "The forecast that next month’s price will equal this month’s price. A surprisingly hard benchmark to beat."),
              ("Seasonal naïve", "The forecast that this month’s price will equal the price in the same month last year. Captures harvest cycles."),
              ("Rolling origin", "A backtest that moves the forecast date forward through history, using only the data available at each date."),
              ("MASE", "The model’s average error divided by a naïve benchmark’s average error. Below 1.0 means the model beats the benchmark."),
              ("MAE", "The average absolute error, in the units of the forecast. The easiest accuracy number to explain."),
              ("RMSE", "An error measure that punishes large misses more heavily than MAE. Useful for tail risk."),
              ("R²", "The share of variation explained by the forecast. Can look impressive simply because prices trend."),
              ("Bias", "The average signed error. Positive means the forecast is systematically too high."),
              ("Directional accuracy", "The share of times the forecast correctly predicts whether the price will rise or fall."),
              ("Prediction interval", "A range that is intended to contain the outcome with a stated probability."),
              ("Coverage", "The share of outcomes that actually fell inside the stated interval in backtest."),
              ("Conformal prediction", "A way of building intervals from past forecast errors without assuming a particular statistical distribution."),
              ("Pinball loss", "A score for a quantile forecast; lower is better, and it rewards both accuracy and honesty about uncertainty."),
              ("Diebold–Mariano test", "A statistical test for whether one forecast is genuinely better than another on the same outcomes."),
              ("Minimum detectable effect", "The smallest improvement the evaluation could reliably detect with its sample size."),
              ("Cost-weighted error", "An error measure that penalises a shortfall more heavily than an excess, reflecting procurement costs."),
              ("Regret", "The extra cost of a decision compared with perfect foresight. A decision-value measure, not an accuracy measure."),
              ("Regime", "A period with a distinct market behaviour, such as before and after a policy shock."),
              ("Leakage", "Accidentally using information from the future in a backtest, which makes the model look better than it is."),
          ],
          [3.6, 13.0], size=8.2, first_col_bold=True,
          caption_text="Glossary: the minimum vocabulary needed to read this report.")


def appendix_f(doc):
    h1(doc, "Appendix F.  Sources and References", page_break=True)

    para(doc,
         "The data sources are public and free at the point of use. The methodological references are the "
         "primary sources for the metrics and tests used in the harness; they are listed so that a reader "
         "can check the definitions rather than take them on trust.")

    h2(doc, "F.1  Data sources")

    bullet(doc, "World Bank Commodity Markets Outlook, Pink Sheet historical monthly prices, November 2026 edition. "
                "Prepared CSV in week4/data; terms CC BY 4.0.", lead="World Bank. ")
    bullet(doc, "Directorate of Marketing and Inspection, Agmarknet daily mandi prices and arrivals. "
                "The intended production source for the Indian deployment.", lead="Agmarknet. ")
    bullet(doc, "Directorate of Economics and Statistics, Agricultural Statistics at a Glance. "
                "Production, area and yield benchmarks.", lead="DES. ")
    bullet(doc, "FAOSTAT crop and trade statistics; UN Comtrade and ITC Trade Map for trade flows; "
                "IMD and NASA POWER for weather; Copernicus for vegetation indices.", lead="FAO and partners. ")
    bullet(doc, "Commission for Agricultural Costs and Prices, price policy reports and MSP notifications, "
                "used for the policy-event calendar in the refinement roadmap.", lead="CACP. ")

    h2(doc, "F.2  Methodological references")

    refs = [
        "Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy. International Journal of Forecasting, 22(4), 679–688.",
        "Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. Journal of Business & Economic Statistics, 13(3), 253–263.",
        "Harvey, D., Leybourne, S., & Newbold, P. (1997). Testing the equality of prediction mean squared errors. International Journal of Forecasting, 13(2), 281–291.",
        "Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. Journal of the American Statistical Association, 102(477), 359–378.",
        "Gneiting, T., Balabdaoui, F., & Raftery, A. E. (2007). Probabilistic forecasts, calibration and sharpness. Journal of the Royal Statistical Society: Series B, 69(2), 243–268.",
        "Vovk, V., Gammerman, A., & Shafer, G. (2005). Algorithmic Learning in a Random World. Springer.",
        "Angelopoulos, A. N., & Bates, S. (2021). A gentle introduction to conformal prediction and distribution-free uncertainty quantification. arXiv:2107.07511.",
        "Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. International Journal of Forecasting, 38(4), 1346–1364.",
        "Hyndman, R. J., & Athanasopoulos, G. (2021). Forecasting: Principles and Practice (3rd ed.). OTexts.",
        "World Bank (2026). Commodity Markets Outlook, October 2026. Washington, DC: World Bank.",
    ]
    for ref in refs:
        bullet(doc, ref)

    h2(doc, "F.3  Attribution and licence")

    para(doc,
         "All charts in this report are original work built from the sources above. The World Bank data are "
         "used under CC BY 4.0 and are attributed in every chart’s source line. The report is decision "
         "support, not investment, trading or agronomic advice. No proprietary or paid data sits on the "
         "critical path of the evaluation.")


explanations = {
    1: "Design target assumed the 31 predictors would add signal beyond price persistence; on global benchmark prices they largely did not.",
    3: "The random walk is hardest to beat at the quarterly horizon; the target assumed exogenous cost-push information that the flat-exog design does not deliver.",
    6: "SARIMAX recovers most of the gap, but the measured advantage is 0.9%, not the 34% implied by the target.",
    12: "The target was closest at the long horizon, where trend and seasonality do more of the work; even so, the gap is 20 points of MASE.",
}
