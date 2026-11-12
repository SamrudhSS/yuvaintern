# -*- coding: utf-8 -*-
"""Sections 3-4: evaluation design and visual communication."""

from pathlib import Path

from docbase import (h1, h2, h3, para, bullet, table, callout, figure,
                     spacer, CONTENT_W, PRIMARY, SECONDARY, ACCENT, PALE)
import facts as F

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
H = F.HORIZONS

PASS3 = [c for c in F.CROPS if F.cross_score(c, 3)["gate"] == "PASS"]
FAIL3 = [c for c in F.CROPS if F.cross_score(c, 3)["gate"] != "PASS"]
PASS12 = [c for c in F.CROPS if F.cross_score(c, 12)["gate"] == "PASS"]
FAIL12 = [c for c in F.CROPS if F.cross_score(c, 12)["gate"] != "PASS"]


def section_3(doc):
    h1(doc, "3.  Evaluation Design: Folds, Gates, Significance and Stress", page_break=True)

    para(doc,
         "A metric is only as trustworthy as the design that produced it. This section specifies the "
         "evaluation design in enough detail that another analyst could reproduce it, challenge it or "
         "extend it. The design has four moving parts: the unit of evaluation, the fold construction, the "
         "promotion gates, and the stress tests that ask whether the result survives a change of crop, "
         "regime or volatility.")

    h2(doc, "3.1  The unit of evaluation is a segment, not a dataset")

    para(doc,
         "The first design decision is what counts as one observation. A pooled row-level evaluation treats "
         "every month of every crop as exchangeable. It is easy to compute and almost always misleading: a "
         "model that is excellent on maize and poor on wheat can post a respectable pooled MAE, and a model "
         "that is good in one state can be carried by that state’s price level. The harness therefore "
         "evaluates at the level of crop × horizon, and reports state-level results separately when the "
         "Indian mandi panel is used. A headline is always a summary of cells, never a substitute for them.")

    bullet(doc, "Each crop has its own price level, volatility and seasonal "
                "pattern. A 20 USD error is large for wheat and small for cotton.", lead="Crop. ")
    bullet(doc, "The same model can pass at one month and fail at twelve. "
                "The horizon is part of the unit, not a robustness check.", lead="Horizon. ")
    bullet(doc, "A model that works in Punjab and fails in Bihar is not a "
                "national model. State-level segmentation is mandatory for the mandi deployment.",
           lead="State. ")
    bullet(doc, "A result that holds only before 2023 is a historical "
                "description, not a forecast capability. Regime is a reporting dimension.",
           lead="Period. ")

    h2(doc, "3.2  Rolling-origin backtesting")

    para(doc,
         "Forecasts are evaluated by moving the forecast origin forward through time, never by a random "
         "train–test split. At each origin the model sees only data up to that month, forecasts 1, 3, 6 and "
         "12 months ahead, and is then scored against outcomes it could not have seen. The origin advances "
         "three months, so consecutive folds share some target months; the overlap is disclosed rather than "
         "treated as independent evidence. The first training window is 120 months, which is the minimum "
         "needed to identify an annual seasonal pattern with any confidence.")

    figure(doc, FIG_DIR / "rolling_origin.png", width_cm=CONTENT_W,
           caption_text="Expanding-window rolling-origin splits: grey is the training window, red is the 12-month forecast block. Only the first ten of sixty folds are shown.")

    table(doc,
          ["Parameter", "Setting", "Consequence for the result"],
          [
              ("Initial training window", f"{F.META['min_train']} months (2001-01 to 2010-12)",
               "Long enough for annual seasonality; too short for a full commodity super-cycle"),
              ("Origin step", f"{F.META['step']} months", "60 folds; adjacent 12-month targets overlap, so the effective independent sample is smaller than 60"),
              ("Maximum horizon", "12 months", "The longest planning window; also the point at which interval coverage is weakest"),
              ("Final origin", "2025-09 (target 2026-09 for h=12)", "The last 12-month target that the current vintage supports; October 2026 is held back"),
              ("Data quarantine", "No observation after the origin enters any feature, scaler or weight",
               "Prevents lookahead leakage; the most common cause of optimistic backtests"),
              ("Ensemble weights", "Estimated from folds strictly before the current fold",
               "The ensemble cannot peek at the outcome it is trying to predict"),
              ("Interval calibration", "Online conformal: fold k uses residuals from folds < k",
               "Distribution-free, but vulnerable to regime shifts in the error distribution"),
              ("Model selection", "Fixed ladder, no per-fold tuning", "Removes the selection bias that inflates a best-of-many result"),
          ],
          [3.3, 6.2, 7.1], size=8.0, first_col_bold=True,
          caption_text="Rolling-origin design parameters and why each one matters.")

    para(doc,
         "Two details are easy to get wrong and are therefore stated explicitly. First, the fertilizer "
         "exogenous series are held flat at their last observed value for the forecast block; this is a "
         "conservative assumption, not a forecast of input costs. Second, the GBDT is trained on the log "
         "return and predicts a change, not a price level, so it cannot extrapolate to a level it has never "
         "seen. Both choices reduce the chance of a spectacular backtest that cannot survive contact with "
         "the next month.")

    h2(doc, "3.3  The promotion gates")

    para(doc,
         "Week 4 specified a single promotion rule: beat both naïve benchmarks on MASE at every horizon. "
         "The executed audit shows why that rule is necessary but not sufficient. A candidate clears the "
         "accuracy gate at three horizons and still cannot be distinguished from the random walk once "
         "sampling uncertainty is counted. A model should therefore pass an integrity check and four "
         "promotion gates, in order, before a claim is published.")

    table(doc,
          ["Gate", "Rule", "Evidence", "If it fails"],
          [
              ("G0  Integrity", "No observation after the origin in any feature, weight or scaler; all folds reproducible",
               "Fold-level prediction file, code hash, leakage checklist", "Stop. The result is invalid, not merely uncertain"),
              ("G1  Accuracy", "MASE vs RW < 1.00 and MASE vs SN < 1.00 at the claimed horizon",
               "Scorecard and heatmap", "Publish the benchmark instead; do not report an improvement"),
              ("G2  Significance", "Paired 95% interval on ΔMAE excludes zero; Diebold–Mariano agrees; effect exceeds the MDE",
               "Bootstrap, DM test, power calculation", "Report parity, not superiority; the point estimate may still be useful for planning"),
              ("G3  Calibration", "Coverage within five points of nominal, with interval width reported",
               "Reliability curve and coverage table", "Recalibrate or widen; do not publish the interval as stated"),
              ("G4  Decision value", "Cost-weighted error or regret better than the default rule, out of sample",
               "Threshold sweep, regret curve", "Do not recommend the decision use; keep the model as a monitoring aid"),
          ],
          [2.7, 6.0, 4.2, 3.7], size=8.0, first_col_bold=True,
          caption_text="The integrity check and four promotion gates: accuracy, significance, calibration and decision value.")

    callout(doc, "THE GATE THAT CHANGED THE CONCLUSION",
            "G1 alone would have published three “passes”. G2 shows that none of the three improvements is "
            "statistically separable from zero. The model is therefore reported as benchmark-equivalent on "
            "point accuracy — useful for planning ranges, not for a claim of superior foresight.")

    h2(doc, "3.4  Significance, power and the minimum detectable effect")

    para(doc,
         "A backtest produces a point estimate. The decision needs to know whether that estimate would "
         "survive a different sample. Three tools answer the question. The paired bootstrap resamples folds "
         "and recomputes the MAE difference, preserving the dependence between models on the same fold. The "
         "Diebold–Mariano test compares the loss differential with a heteroskedasticity- and "
         "autocorrelation-consistent variance, with the Harvey–Leybourne–Newbold small-sample correction. "
         "The minimum detectable effect (MDE) translates the standard error into the smallest improvement "
         "the design could reliably detect at 80% power.")

    para(doc,
         f"The MDE is the most useful number in this section and the least often reported. At h=1 the "
         f"design can detect an improvement of about {F.num(F.sig(1,'Ensemble')['mde_pct'],1)}% of the "
         f"random-walk MAE. The observed ensemble gain is "
         f"{F.num(-F.sig(1,'Ensemble')['mae_diff_pct'],1)}%. The evaluation is therefore underpowered for "
         "the effect it is trying to measure: a genuine 2% edge and a genuine 0% edge produce "
         "indistinguishable backtests at this sample size. That is not a reason to claim the edge; it is a "
         "reason to stop pretending the backtest can settle the question.")

    table(doc,
          ["Horizon", "Candidate", "ΔMAE vs RW (USD/MT)", "95% bootstrap interval", "DM p-value", "MDE (% of RW MAE)", "Reading"],
          [
              (f"h = {h}",
               F.head(h)["model"],
               F.signed(F.sig(h, F.head(h)["model"])["mae_diff_vs_rw"], 2),
               f"[{F.signed(F.sig(h, F.head(h)['model'])['ci_lo'], 2)}, {F.signed(F.sig(h, F.head(h)['model'])['ci_hi'], 2)}]",
               F.num(F.sig(h, F.head(h)["model"])["dm_p"], 3),
               F.num(F.sig(h, F.head(h)["model"])["mde_pct"], 1) + "%",
               "Not separable from zero" if F.sig(h, F.head(h)["model"])["dm_p"] > 0.05 else "Detectable")
              for h in H
          ],
          [1.5, 2.6, 3.0, 3.3, 1.7, 2.3, 2.2], size=8.0, first_col_bold=True,
          caption_text="Paired uncertainty for the best candidate at each horizon. Positive ΔMAE means the candidate is worse than the random walk.")

    para(doc,
         "Two further adjustments matter. First, the harness tests five candidates at four horizons, so "
         "twenty comparisons are made. A Bonferroni-corrected threshold would be 0.0025, and no candidate "
         "comes close; uncorrected p-values are shown for transparency, not as a licence to cherry-pick. "
         "Second, the evaluation reports the whole ladder, not only the winner. ETS is significantly worse "
         f"than the random walk at h=1 (p = {F.num(F.sig(1,'ETS')['dm_p'],3)}), and the direct GBDT is "
         f"significantly worse at h=3 (p = {F.num(F.sig(3,'GBDT (direct)')['dm_p'],3)}). A report that "
         "showed only the champion would hide the fact that two of the five candidates are reliably worse "
         "than doing nothing at the horizons where they are claimed.")

    h2(doc, "3.5  Calibration protocol")

    para(doc,
         "Point accuracy and interval honesty are separate achievements. The harness issues intervals by "
         "online conformal prediction: for fold k, it takes the signed residuals of the same model and "
         "horizon from folds 1 to k−1, adds the appropriate empirical quantiles to the point forecast, and "
         "only then reveals the outcome. No future residual enters the interval. The method is "
         "distribution-free and auditable, and it makes the coverage promise testable.")

    para(doc,
         f"The result is instructive. At h=1 the ensemble’s 90% interval covers "
         f"{F.num(F.score(1,'Ensemble')['coverage90'],1)}% of outcomes — essentially nominal. At h=3 and h=6 "
         f"it covers {F.num(F.score(3,'Ensemble')['coverage90'],1)}% and "
         f"{F.num(F.score(6,'Ensemble')['coverage90'],1)}%, just outside the five-point tolerance. At h=12 "
         f"it covers only {F.num(F.score(12,'Ensemble')['coverage90'],1)}%, more than ten points below the "
         f"promise, despite an average width of {F.num(F.score(12,'Ensemble')['width90'],0)} USD/MT. The "
         "interval is not too narrow; the error distribution changed after the calibration window. The "
         f"random walk is worse still at h=12 ({F.num(F.score(12,'Random Walk')['coverage90'],1)}%). This "
         "is the central calibration lesson: coverage is a monitored property, not a one-time certificate.")

    table(doc,
          ["Horizon", "ENS 90% coverage", "ENS width (USD/MT)", "RW 90% coverage", "RW width (USD/MT)", "Verdict"],
          [
              (f"h = {h}",
               F.num(F.score(h, "Ensemble")["coverage90"], 1) + "%",
               F.num(F.score(h, "Ensemble")["width90"], 0),
               F.num(F.score(h, "Random Walk")["coverage90"], 1) + "%",
               F.num(F.score(h, "Random Walk")["width90"], 0),
               "Nominal" if abs(F.score(h, "Ensemble")["coverage90"] - 90) <= 5 else "Under-covering")
              for h in H
          ],
          [1.6, 3.1, 3.1, 2.9, 2.9, 3.0], size=8.2, first_col_bold=True,
          caption_text="Empirical 90% interval coverage and width. A wide interval that still under-covers is a distribution failure, not a sharpness failure.")

    h2(doc, "3.6  Regime and volatility stress tests")

    para(doc,
         "A backtest that spans one regime measures one regime. The harness splits the folds at January "
         "2023 — after the fertilizer spike, the energy shock and the post-pandemic dislocation — and "
         "recomputes the gate in each period. It also sorts folds into low, mid and high volatility "
         "terciles using the 12-month rolling coefficient of variation at the origin. The purpose is not to "
         "find a favourable subsample but to see whether the sign of the result is stable.")

    table(doc,
          ["Horizon", "Period", "Folds", "ENS MASE vs RW", "SARIMAX MASE vs RW", "Reading"],
          [
              (f"h = {h}", period,
               str(int(F.regime_row(h, "Ensemble", period)["folds"])),
               F.num(F.regime_row(h, "Ensemble", period)["mase_rw"], 3),
               F.num(F.regime_row(h, "SARIMAX", period)["mase_rw"], 3),
               "Ensemble better" if F.regime_row(h, "Ensemble", period)["mase_rw"] < 1 else "Ensemble worse")
              for h in H for period in ["2010-2022", "2023-2026"]
          ],
          [1.5, 2.2, 1.4, 3.0, 3.6, 4.9], size=7.8, first_col_bold=True,
          caption_text="Regime split: the sign of the model’s advantage is not stable across periods.")

    para(doc,
         f"The split exposes an important instability. At h=1 the ensemble beats the random walk before "
         f"2023 (MASE {F.num(F.regime_row(1,'Ensemble','2010-2022')['mase_rw'],3)}) and loses to it after "
         f"2023 (MASE {F.num(F.regime_row(1,'Ensemble','2023-2026')['mase_rw'],3)}). At h=12 the pattern "
         f"reverses: {F.num(F.regime_row(12,'Ensemble','2010-2022')['mase_rw'],3)} before 2023 and "
         f"{F.num(F.regime_row(12,'Ensemble','2023-2026')['mase_rw'],3)} after. A model whose edge changes "
         "sign with the regime cannot be described as uniformly better; it can be described as "
         "regime-conditional, and that is a different, weaker claim.")

    para(doc,
         "The volatility buckets tell a similarly mixed story. At h=1 the ensemble’s MASE in the high "
         f"volatility tercile is {F.num(F.vol_rows(1).iloc[2]['mase_rw'],3)}, slightly worse than the random "
         f"walk; in the low-volatility tercile it is {F.num(F.vol_rows(1).iloc[0]['mase_rw'],3)}. At h=6 "
         f"the high-volatility tercile is {F.num(F.vol_rows(6).iloc[2]['mase_rw'],3)}, better than the "
         "benchmark. There is no monotonic story. The honest summary is that the model’s advantage is "
         "small, unstable and not reliably concentrated where the operational risk is highest.")

    h2(doc, "3.7  Cross-commodity replication and the pooling trap")

    para(doc,
         "The wheat result is one cell. The cross-commodity check repeats the ladder on rice, maize, "
         "soybeans and cotton with the same hyperparameters and no per-crop tuning. This is a test of "
         "transfer, not a search for a better crop. The result is deliberately unflattering: the model "
         "family that wins on one crop does not automatically win on another, and the pooled average hides "
         "the difference.")

    figure(doc, FIG_DIR / "cross_commodity.png", width_cm=CONTENT_W,
           caption_text="Best candidate per crop and horizon, measured by MASE against the random walk. A tick means both naïve benchmarks were beaten; a cross means the cell failed.")

    para(doc,
         f"At h=3, {len(PASS3)} of five crops clear the gate"
         + (f" ({', '.join(PASS3)})" if PASS3 else "")
         + (f", while {', '.join(FAIL3)} do not" if FAIL3 else "")
         + f". At h=12, {len(PASS12)} of five clear it"
         + (f" ({', '.join(PASS12)})" if PASS12 else "")
         + (f", while {', '.join(FAIL12)} do not" if FAIL12 else "")
         + f". The MAE-weighted pooled MASE at h=3 is {F.num(F.pooled_mase(3),3)} — comfortably below 1.0 — "
         "even though at least one crop fails. That is the pooling trap in one number: the average looks "
         "like a success while a grower in the failing crop experiences a model that is no better than "
         "doing nothing.")

    table(doc,
          ["Crop", "Best h=3", "MAE h=3", "MASE h=3", "Gate h=3", "Best h=12", "MASE h=12", "Gate h=12"],
          [
              (crop,
               F.cross_score(crop, 3)["model"],
               F.num(F.cross_score(crop, 3)["mae"], 1),
               F.num(F.cross_score(crop, 3)["mase_rw"], 3),
               F.gate(F.cross_score(crop, 3)["gate"]),
               F.cross_score(crop, 12)["model"],
               F.num(F.cross_score(crop, 12)["mase_rw"], 3),
               F.gate(F.cross_score(crop, 12)["gate"]))
              for crop in F.CROPS
          ],
          [1.8, 2.4, 1.7, 1.9, 2.3, 2.4, 2.0, 2.1], size=8.0, first_col_bold=True,
          caption_text="Cross-commodity replication: the same ladder, same hyperparameters, different crop.")

    callout(doc, "WHAT THE CROSS-CHECK BUYS",
            "It converts a wheat-specific observation into a statement about a model family. It also "
            "identifies where the framework needs exogenous data rather than a better algorithm: the "
            "failing crops are the ones whose prices are most exposed to policy and trade shocks that the "
            "current feature set does not observe.")

    h2(doc, "3.8  Pre-registration: the checklist signed before the run")

    para(doc,
         "The checklist below is completed and timestamped before the first candidate is fitted. Its "
         "purpose is to prevent the evaluation from becoming a search for a favourable metric. It is short "
         "enough to be practical and specific enough to be auditable. Appendix B reproduces the full form.")

    table(doc,
          ["Item", "Required entry", "Example from this evaluation"],
          [
              ("Claim under test", "One sentence, falsifiable", "The ensemble reduces MAE versus a random walk at h=1"),
              ("Primary metric", "One metric, one variant", "MASE vs RW, same folds and horizon"),
              ("Secondary metrics", "Named in advance, not selected post hoc", "MAE, RMSE, coverage, pinball, CWE, DA"),
              ("Segments", "Crop, state, horizon, period, volatility", "Five crops × four horizons × two regimes"),
              ("Fold boundaries", "Dates and step", "2010-12 to 2025-09, step 3 months"),
              ("Benchmarks", "Both naïve models, same folds", "Random walk and seasonal naïve"),
              ("Success threshold", "Numeric, with a significance rule", "MASE < 1.00 and 95% CI excluding zero"),
              ("Failure action", "What happens if the gate fails", "Publish the benchmark and a driver note"),
              ("Owner and date", "Named reviewer and timestamp", "Validator signs before the run"),
          ],
          [3.4, 5.4, 7.8], size=8.0, first_col_bold=True,
          caption_text="Pre-registration checklist: the decisions that must be fixed before results are seen.")

    h2(doc, "3.9  The executed scorecard")

    para(doc,
         "Table 15 is the audit in one view. The best candidate at each horizon is shown with its "
         "benchmark-relative error, the paired interval, the significance test, the coverage and the "
         "directional result. The verdict column is intentionally conservative: a gate pass is not the "
         "same as a licence to claim superiority.")

    table(doc,
          ["Horizon", "Best candidate", "MAE", "MASE vs RW", "ΔMAE vs RW [95% CI]", "DM p", "Gate", "Cover 90", "DA", "Verdict"],
          [
              (f"h = {h}",
               F.head(h)["model"],
               F.num(F.head(h)["mae"], 1),
               F.num(F.head(h)["mase_rw"], 3),
               f"{F.signed(F.sig(h, F.head(h)['model'])['mae_diff_vs_rw'], 2)} [{F.signed(F.sig(h, F.head(h)['model'])['ci_lo'], 2)}, {F.signed(F.sig(h, F.head(h)['model'])['ci_hi'], 2)}]",
               F.num(F.sig(h, F.head(h)["model"])["dm_p"], 3),
               F.gate(F.head(h)["gate"]),
               F.num(F.head(h)["coverage90"], 1) + "%",
               F.num(F.head(h)["da"], 1) + "%",
               "Parity, not superiority" if F.sig(h, F.head(h)["model"])["dm_p"] > 0.05 else "Superiority supported")
              for h in H
          ],
          [1.2, 2.4, 1.3, 1.7, 3.7, 1.2, 1.4, 1.4, 1.2, 2.1], size=7.6, first_col_bold=True,
          caption_text="Executed headline scorecard. Every gate pass is accompanied by the uncertainty that qualifies it.")

    figure(doc, FIG_DIR / "scorecard_heatmap.png", width_cm=CONTENT_W,
           caption_text="MASE against the random walk for all six models and four horizons. Values below 1.0 beat the benchmark; the colour scale is centred on 1.0.")

    para(doc,
         f"Four results deserve to be stated plainly. First, {F.gate_count()[0]} of "
         f"{F.gate_count()[1]} candidate-horizon cells clear the Week 4 accuracy gate. Second, no candidate’s "
         "improvement over the random walk is statistically separable from zero at the 95% level; the "
         "smallest p-value among the passing candidates is well above 0.05. Third, directional accuracy "
         "sits between 46.7% and 55.0%, inside the binomial noise band around a coin flip. Fourth, interval "
         "coverage is nominal at h=1 and degrades to 79% at h=12. The model is a modest planning aid, not "
         "a forecasting breakthrough.")

    h2(doc, "3.10  Reconciling the design target with the measured evidence")

    para(doc,
         "Week 4 specified a design-target matrix in which the ensemble reached MASE 0.54 at h=1 and 0.74 "
         "at h=12. The executed evidence is 0.979 and 0.945. The gap is not a coding error, and it should "
         "not be quietly dropped. It is the difference between a specification and an outcome, and it is "
         "the most important lesson in the whole five-week programme.")

    target = {1: 0.54, 3: 0.58, 6: 0.66, 12: 0.74}
    table(doc,
          ["Horizon", "Design target MASE", "Week 4 executed", "Week 5 audit", "Audit vs Week 4", "Why the target and the evidence differ"],
          [
              (f"h = {h}",
               f"{target[h]:.2f}",
               F.num(F.head(h)["mase_rw"], 3),
               F.num(F.head(h)["mase_rw"], 3),
               f"{F.num(F.REPRODUCE[F.REPRODUCE.horizon == h]['delta_pct'].iloc[0], 3)}%",
               explanations[h])
              for h in H
          ],
          [1.3, 2.4, 2.4, 2.2, 2.0, 6.3], size=7.8, first_col_bold=True,
          caption_text="Design-target matrix versus executed evidence. The audit reproduces the Week 4 run to within 0.01%.")

    para(doc,
         f"The audit reproduces the Week 4 numbers almost exactly: the largest difference across horizons "
         f"is {F.reproduce_max_delta():.3f}%, which is numerical noise from library versions, not a modelling "
         "change. That reproducibility is itself a result: the pipeline is stable, so the gap cannot be "
         "explained away as a bug. The design targets assumed that a richer feature set would extract "
         "signal from global benchmark prices. It did not. Benchmark prices behave close to a random walk "
         "at short horizons, and the 31 causal predictors add little to the persistence already captured "
         "by the last observed price. The target matrix was an accuracy envelope, written before the "
         "evidence existed. The executed scorecard is what the data actually supports.")

    callout(doc, "THE HONEST HEADLINE",
            "The model does not deliver the 46% error reduction promised by the design target. It delivers "
            "a 2% reduction at h=1 that is indistinguishable from zero, and a 5.5% reduction at h=12 that "
            "is also indistinguishable from zero. Reporting this is more valuable than publishing the "
            "target and hoping nobody checks.")


def section_4(doc):
    h1(doc, "4.  Visualisation Strategy: Making the Evidence Legible", page_break=True)

    para(doc,
         "A chart is a decision interface. The reader does not want the data; they want to know what it "
         "means for the choice in front of them. Most forecast charts fail because they answer the "
         "analyst’s question (“what did the model produce?”) rather than the reader’s question (“how wrong "
         "could this be, and what should I do?”). This section specifies the visual system, chart by chart, "
         "so that the same evidence can be read by a board member, a procurement officer and a modelling "
         "reviewer without being redrawn three times.")

    h2(doc, "4.1  Why forecast charts fail")

    bullet(doc, "The chart shows a dense line and a second dense line. The "
                "reader cannot tell whether the gap is good, bad or normal, because no benchmark, threshold "
                "or error band is visible.",
           lead="The chart has no benchmark. ")
    bullet(doc, "A point forecast is drawn as a solid line into the future, "
                "which reads as certainty. The interval is either omitted or drawn so faintly that it "
                "disappears in print.",
           lead="The chart hides uncertainty. ")
    bullet(doc, "Twelve crops, four horizons and six models are placed on "
                "one axis. The chart is accurate and unreadable. The reader takes away the busiest colour, "
                "not the finding.",
           lead="The chart encodes everything. ")
    bullet(doc, "The title says “Wheat price, USD/MT” instead of “The "
                "forecast range is wide enough to matter”. The reader has to do the interpretation, and "
                "will usually do a different one.",
           lead="The title describes the axes, not the message. ")
    bullet(doc, "A red–green scale is used for pass–fail. Roughly one "
                "in twelve men cannot distinguish the two ends, and a printed report loses the distinction "
                "entirely.",
           lead="The colour carries the meaning. ")

    h2(doc, "4.2  Seven design rules")

    para(doc,
         "The rules are ordered by how often they are violated. They apply to every chart in the report "
         "and to every chart in the proposed dashboard.", space_after=5)

    bullet(doc, "Every chart has one sentence at the top that states what "
                "the reader should conclude. If the sentence cannot be written, the chart is not ready.",
           lead="1. One chart, one message. ")
    bullet(doc, "The title is a finding, not a label. “Error grows faster than the "
                "horizon” is a finding; “MAE by horizon” is a label.",
           lead="2. Write the title as a sentence. ")
    bullet(doc, "The benchmark, the gate and the unit are visible in the chart "
                "or its subtitle. A reader should not need the surrounding paragraph to know what good looks like.",
           lead="3. Put the benchmark in the frame. ")
    bullet(doc, "Every forecast is drawn with at least a 90% band, and the band is "
                "labelled with its meaning, not only its percentage. A point line into the future is not "
                "allowed unless the interval is shown elsewhere on the same page.",
           lead="4. Show uncertainty at the same visual weight as the point. ")
    bullet(doc, "Thresholds, targets and break-even lines are annotated in words. "
                "A dashed line without a label is a rumour.",
           lead="5. Annotate the threshold. ")
    bullet(doc, "Colour encodes one dimension and never carries the only copy of "
                "the meaning. Pass–fail is also marked with a tick or cross; a series is also labelled "
                "directly at its end.",
           lead="6. Colour is a second channel, never the only one. ")
    bullet(doc, "Every chart carries the data vintage and the fold count. A chart "
                "without a source cannot be audited, and a chart without a fold count cannot be compared "
                "with another chart.",
           lead="7. Source and sample size are part of the chart. ")

    h2(doc, "4.3  The visual ladder: one evidence base, three audiences")

    para(doc,
         "The same result is presented at three levels of detail. The board sees one chart and one "
         "decision. Operations sees the forecast, the error by horizon and the decision threshold. The "
         "technical reviewer sees the scorecard, the calibration curve, the residual diagnostics and the "
         "fold-level data. The levels are not different analyses; they are different crops of the same "
         "evidence. Table 17 specifies the ladder.")

    table(doc,
          ["Level", "Audience", "Question they own", "What they see", "What they never see", "Time to read"],
          [
              ("L1  Decision", "Board, finance committee, policy lead",
               "Is the forecast good enough to act on, and what is the range?",
               "One fan chart, one verdict box, one recommendation",
               "Model names, fold counts, residual diagnostics", "60 seconds"),
              ("L2  Operations", "Procurement, sales, supply planning",
               "When should we buy, and how wrong could the number be?",
               "Fan chart, error by horizon, threshold curve, segment table",
               "Hyperparameters, SHAP values, DM statistics", "5 minutes"),
              ("L3  Technical", "Validation, modelling, data engineering",
               "Is the result real, stable and reproducible?",
               "Scorecard, calibration curve, residual diagnostics, fold-level data",
               "Nothing; this is the full audit", "30 minutes"),
          ],
          [2.3, 3.3, 3.6, 3.6, 2.6, 1.2], size=8.0, first_col_bold=True,
          caption_text="The visual ladder: three audiences, one evidence base, three crops of the same result.")

    callout(doc, "THE LADDER RULE",
            "No audience is given a chart from a level above its need, and no audience is given a number "
            "without the caveat that belongs to it. The board sees the range; operations sees the "
            "threshold; the reviewer sees the residuals. Sending all three the same 12-panel dashboard is "
            "not transparency — it is abdication.")

    h2(doc, "4.4  The chart catalogue")

    para(doc,
         "Ten chart types cover the reporting system. Each is specified with its purpose, audience, data "
         "source and the failure mode it is designed to prevent. Any new chart must earn a row in this "
         "table or be treated as exploratory.")

    table(doc,
          ["Chart", "Question it answers", "Audience", "Data", "Design rule", "Failure it prevents"],
          [
              ("Fan chart", "What is the range, and how does it widen?", "L1, L2", "Latest forecast + conformal bands",
               "Three bands, direct labels, origin marked", "Point-forecast certainty"),
              ("Scorecard heatmap", "Which model wins where?", "L2, L3", "MASE matrix",
               "Diverging scale centred on 1.0; ticks and crosses", "Cherry-picked single number"),
              ("Predicted vs actual", "Does the forecast track the turning points?", "L2, L3", "Fold-level predictions",
               "Two horizons, shaded absolute error, same axes", "Aggregate score hiding timing failure"),
              ("Error by horizon", "How fast does accuracy decay?", "L2, L3", "MAE and MASE by horizon",
               "Bars in decision units; line in benchmark units; no dual axis", "Comparing raw errors across horizons"),
              ("Calibration curve", "Does the interval mean what it says?", "L3", "Nominal vs empirical coverage",
               "45° reference, four horizons, width reported", "Overconfident intervals"),
              ("Residual panel", "Is there structure left in the errors?", "L3", "Residuals over time, ACF, Q–Q",
               "Four panels, one message", "Autocorrelation masquerading as skill"),
              ("Cross-commodity grid", "Does the result transfer?", "L2, L3", "MASE by crop × horizon",
               "Best model labelled in each cell; gate marked", "Pooled average hiding a failing crop"),
              ("Decision curve", "What threshold should we use?", "L2", "Cost and hit rate vs threshold",
               "Perfect-foresight line, default rule, optimum marked", "Accuracy without decision value"),
              ("Threshold matrix", "Where does the sign go wrong?", "L2, L3", "Confusion matrix at the chosen threshold",
               "Counts, not percentages only", "Hit rate hiding asymmetric errors"),
              ("One-screen dashboard", "What is the whole story in one view?", "L1", "All of the above",
               "Four panels, one verdict, one recommendation", "Report sprawl and inconsistent numbers"),
          ],
          [2.5, 3.2, 1.4, 3.2, 3.4, 2.9], size=7.4, first_col_bold=True,
          caption_text="Chart catalogue: ten chart types, each with a specified audience and a failure it prevents.")

    h2(doc, "4.5  The core charts, one by one")

    h3(doc, "4.5.1  The fan chart: the only honest way to show a forecast")
    para(doc,
         "The fan chart is the primary artefact for a non-specialist reader. It shows history as a solid "
         "line, the forecast as a central path, and three nested bands at 50%, 80% and 90%. The origin is "
         "marked with a vertical rule, so the reader can see exactly where knowledge stops. The bands are "
         "labelled in words (“90% of outcomes should fall inside this band”), not only with a percentage. "
         "The chart does not show a single future; it shows a range of futures and the central path within it.")
    figure(doc, FIG_DIR / "fan_chart.png", width_cm=CONTENT_W,
           caption_text="Fan chart for wheat at the October 2026 origin. The 12-month point forecast is 321 USD/MT; the 90% band spans roughly 231–415 USD/MT.")

    para(doc,
         "The fan chart also carries the most important caveat in the report. The h=12 interval under-covers "
         "in backtest, so the displayed 90% band is best read as an approximate 80% band. The caption says "
         "so. A chart that overstates its own coverage is worse than no chart.")

    h3(doc, "4.5.2  Predicted versus actual: does it track the turns?")
    para(doc,
         "A score can be good while the forecast misses every turning point. The predicted-versus-actual "
         "panel plots the outcome and the forecast on the same time axis, with the absolute error shaded. "
         "Two horizons are shown side by side, because the interesting question is not whether the model "
         "tracks the level but whether it tracks the level as the horizon lengthens. The chart is "
         "deliberately not annotated with a model name; the reader is looking at behaviour, not at "
         "architecture.")
    figure(doc, FIG_DIR / "predicted_vs_actual.png", width_cm=CONTENT_W,
           caption_text="Ensemble forecasts against outcomes for h=1 and h=12. The shaded area is absolute error; the widening gap at h=12 is the horizon penalty made visible.")

    h3(doc, "4.5.3  Error by horizon: two scales, two messages")
    para(doc,
         "The left panel shows MAE in USD/MT, the unit in which a buyer budgets. The right panel shows the "
         "same errors divided by the random-walk error, which is the unit in which a modeller judges skill. "
         "The two panels are deliberately separate rather than sharing a dual axis: a dual axis invites the "
         "reader to infer a relationship between two quantities that are not on the same scale. The gate "
         "line at 1.000 is annotated, and the values are printed on the bars and points.")
    figure(doc, FIG_DIR / "error_by_horizon.png", width_cm=CONTENT_W,
           caption_text="Absolute error grows with the horizon; relative skill does not improve. The right panel is the only fair comparison across horizons.")

    h3(doc, "4.5.4  Calibration: the chart that keeps the interval honest")
    para(doc,
         "The reliability curve plots nominal coverage on the horizontal axis against empirical coverage "
         "on the vertical. A perfectly calibrated model lies on the 45° line. The ensemble tracks the line "
         "at h=1 and falls below it at h=12, which is exactly the failure described in Section 3.5. The "
         "right panel shows the 90% coverage by model and horizon, with the nominal line. The message is "
         "that coverage is engineered by the conformal procedure and then eroded by regime change — a "
         "subtle point that a single “90% interval” label would hide.")
    figure(doc, FIG_DIR / "calibration.png", width_cm=CONTENT_W,
           caption_text="Reliability curves and empirical 90% coverage. The h=12 curve falls below the diagonal: the interval is too confident for the post-2023 error distribution.")

    h3(doc, "4.5.5  Residual diagnostics: what the score cannot show")
    para(doc,
         "The residual panel is a technical chart with a non-technical purpose: it shows whether the model "
         "has left predictable structure on the table. The time series reveals volatility clustering; the "
         "histogram reveals skew and fat tails; the autocorrelation function reveals persistence the model "
         "did not capture; the Q–Q plot reveals departures from normality. A well-scored model with "
         "strong residual autocorrelation is not a finished model; it is a model that has not used all the "
         "information available at the origin.")
    figure(doc, FIG_DIR / "residual_diagnostics.png", width_cm=CONTENT_W,
           caption_text="Residual diagnostics for the ensemble at h=1. Autocorrelation beyond the dashed band means predictable structure remains.")

    h3(doc, "4.5.6  Cross-commodity grid: the anti-pooling chart")
    para(doc,
         "The grid is a heatmap of MASE against the random walk for every crop and horizon, with the best "
         "candidate named in each cell. It is the visual answer to the pooling trap: a reader can see at a "
         "glance that maize and soybeans are green while wheat and rice are amber or red. The chart does "
         "not show a pooled average, because the pooled average is the thing that hides the problem.")
    figure(doc, FIG_DIR / "cross_commodity.png", width_cm=CONTENT_W,
           caption_text="Cross-commodity MASE grid: the same model family transfers to some crops and not others.")

    h3(doc, "4.5.7  Decision curve: accuracy translated into money")
    para(doc,
         "The decision curve plots the realised procurement cost against the buy-now threshold. Three "
         "reference lines make it readable: perfect foresight, the always-wait policy, and the chosen "
         "threshold. The right panel shows the hit rate and the share of price rises captured. The curve "
         "makes the trade-off explicit: a higher threshold buys fewer times but with a better hit rate, "
         "and it misses most of the rises. The optimum is marked, but the caption says it is an in-sample "
         "optimum and must be validated in shadow deployment.")
    figure(doc, FIG_DIR / "decision_curve.png", width_cm=CONTENT_W,
           caption_text="Procurement cost and direction performance as a function of the buy-now threshold. The in-sample optimum is a hypothesis, not a production setting.")

    h2(doc, "4.6  The one-screen dashboard")

    para(doc,
         "The board does not read a report; it reads a screen. The proposed dashboard fits on one page and "
         "answers four questions in a fixed order: what is the forecast, how wrong could it be, how do we "
         "know, and what should we do. The top-left panel is the fan chart. The top-right is the horizon "
         "verdict. The bottom-left is calibration and skill. The bottom-right is the recommendation, "
         "written in plain language. Every panel is generated from the same scorecard, so the numbers "
         "cannot disagree with one another.")

    figure(doc, FIG_DIR / "dashboard_mock.png", width_cm=CONTENT_W,
           caption_text="Proposed one-screen evaluation dashboard. The verdict and the recommendation are generated from the same gate logic as the written report.")

    para(doc,
         "The dashboard is not a substitute for the report. It is the entry point. Each panel links to the "
         "section that explains it, and the export carries the date, the origin and the fold count. A "
         "dashboard without a vintage is a screenshot; a dashboard with one is an audit trail.")

    h2(doc, "4.7  Accessibility and integrity")

    bullet(doc, "The palette is colour-blind safe: dark green, "
                "slate blue and amber, with ticks and crosses carrying pass–fail as well as colour.",
           lead="Colour. ")
    bullet(doc, "Every chart has a sentence-long alt text and a data table in "
                "the appendix. A reader who cannot see the chart can still recover the finding.",
           lead="Alt text. ")
    bullet(doc, "Axis labels carry units; the subtitle carries the vintage and "
                "the fold count. No chart relies on the surrounding paragraph for its scale.",
           lead="Labels. ")
    bullet(doc, "Zero baselines are used for bar charts; line charts are allowed "
                "to zoom, but the zoom is stated in the caption.",
           lead="Baselines. ")
    bullet(doc, "No 3-D, no pie charts for more than three categories, no "
                "rainbow scales, no dual axes, no unlabelled dashed lines.",
           lead="Prohibited. ")
    bullet(doc, "Every chart is reproducible from a script and a frozen data "
                "vintage. A chart that cannot be regenerated is a claim, not evidence.",
           lead="Reproducibility. ")

    h2(doc, "4.8  Anti-patterns and their fixes")

    table(doc,
          ["Anti-pattern", "Why it fails", "Fix used here"],
          [
              ("Point forecast drawn as a solid future line", "Reads as certainty; hides the range", "Fan chart with three labelled bands and a stated coverage caveat"),
              ("Single accuracy number in the title", "Invites overclaiming and hides segment failure", "Benchmark-relative MASE with a confidence interval and a segment table"),
              ("Dual axis for error and percentage", "Suggests a relationship that does not exist", "Two panels, separate scales, explicit captions"),
              ("Pooled average across crops", "One failing crop disappears into the mean", "Crop × horizon heatmap; pooled number shown only beside segments"),
              ("Best model highlighted, rest omitted", "Hides that alternatives are worse than the benchmark", "Full ladder, including ETS and GBDT failures"),
              ("Interval shown without width", "A wide interval can cover by accident", "Coverage and width reported together; Winkler score in the appendix"),
              ("Colour-only pass/fail", "Inaccessible in print and to colour-blind readers", "Ticks, crosses and direct labels alongside colour"),
              ("Chart without vintage", "Cannot be reproduced or compared", "Source line with data vintage, fold count and origin"),
          ],
          [4.0, 6.2, 6.4], size=8.0, first_col_bold=True,
          caption_text="Visual anti-patterns, the failure each one causes, and the fix adopted in this report.")


explanations = {
    1: "Design target assumed the 31 predictors would add signal beyond price persistence; on global benchmark prices they largely did not.",
    3: "The random walk is hardest to beat at the quarterly horizon; the target assumed exogenous cost-push information that the flat-exog design does not deliver.",
    6: "SARIMAX recovers most of the gap, but the measured advantage is 0.9%, not the 34% implied by the target.",
    12: "The target was closest at the long horizon, where trend and seasonality do more of the work; even so, the gap is 20 points of MASE.",
}
