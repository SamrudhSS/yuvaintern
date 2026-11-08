# -*- coding: utf-8 -*-

"""Section 6: defect-specific method playbooks."""



from docbase import h1, h2, h3, para, bullet, table, callout, code_block

from facts import PM, YM, LOG, pct, num





def section_6(doc):

    h1(doc, "6.  Method Playbooks", page_break=True)



    para(doc,

         "Section 5 says what happens and in what order. This section says why each method was "

         "chosen, what it preserves, what it costs, and when it should be replaced. The playbooks are "

         "written to be argued with: each states the conditions under which a different method would "

         "be correct.")



    # ------------------------------------------------------------------ 6.1

    h2(doc, "6.1  Missing data")

    para(doc,

         "The first question is not 'which imputation method' but 'why is the value missing'. In "

         "agricultural panels the mechanism is often observable, which makes classification more "

         "reliable than in clinical or survey data.")



    h3(doc, "6.1.1  Mechanisms in agricultural terms")

    table(doc,

          ["Mechanism", "Meaning", "Agricultural example", "Consequence"],

          [

              ("MCAR", "Missingness independent of everything observed or unobserved", "A file failed to transfer for a random month", "Complete-case analysis is unbiased, though wasteful"),

              ("MAR", "Missingness explained by observed variables", "Small states report less often; reporting depends on state and crop", "Conditional imputation can be unbiased if the model is right"),

              ("MNAR", "Missingness depends on the unobserved value", "High prices discourage reporting; only low prices are filed", "No imputation from the observed data is unbiased; flag and sensitivity-test"),

          ],

          [2.0, 5.4, 6.0, 5.2], size=8.0, first_col_bold=True,

          caption_text="Missingness mechanisms and what each permits. MNAR is common in price reporting and is the reason flags are mandatory.")



    para(doc,

         "The strategy classifies by cause where the cause is recorded and treats unexplained gaps as "

         "MNAR-until-shown-otherwise. That is conservative on purpose. A model that imputes an "

         "unexplained gap at the series mean assumes MAR without evidence, and in a price series the "

         "assumption is frequently wrong: markets with missing quotes are often the thin markets whose "

         "prices differ most.")



    h3(doc, "6.1.2  Seven methods compared")

    table(doc,

          ["Method", "Preserves", "Destroys / risks", "Cost", "Use when"],

          [

              ("Listwise deletion", "Nothing artificial; simple", "Power; biases if not MCAR; breaks panel balance", "Low", "Gap is long, unexplained, and the series is not critical"),

              ("Median / mean", "Central tendency", "Variance, covariance, seasonality, time structure", "Low", "Almost never for a time series; acceptable for a static covariate with <2% missing"),

              ("Last observation carried forward", "Level at the last observation", "Trend and turning points; creates flat runs", "Low", "Only for a stock variable known not to change between observations"),

              ("Linear interpolation", "Local level and slope between anchors", "Curvature; invents values across long gaps", "Low", "Short internal gaps (â‰¤3 months) in a smooth series"),

              ("Seasonal-naive fill", "Seasonal shape", "Level drift; copies last year's shock", "Low", "Strongly seasonal series with a stable year-on-year pattern"),

              ("KNN / MICE", "Cross-variable and temporal structure", "Runtime; model dependence; over-smoothing; hard to audit", "High", "Many correlated indicators and a gap pattern that is demonstrably MAR"),

              ("Model-based (state space)", "Trend, season, uncertainty", "Specification risk; complexity", "High", "Target series where an interval is needed, not just a point"),

          ],

          [4.0, 4.2, 5.2, 1.6, 4.6], size=7.9, first_col_bold=True,

          caption_text="Imputation methods. The chosen method for MYP-26 is interpolation, bounded to short internal gaps; the rest are fallbacks with stated preconditions.")



    para(doc,

         "Interpolation is chosen for the reference panel because the gaps are short, the series are "

         "smooth at monthly frequency, and the method is transparent: a reviewer can see the two "

         "anchors and the straight line between them. MICE would produce a more sophisticated number "

         "with no way to audit it, and on a gap of one or two months it would add complexity without "

         "adding information.")



    para(doc,

         "There is one case where interpolation is clearly wrong: a price series with a structural "

         "break inside the gap, such as a policy announcement or a market closure that lasted the "

         "whole gap. The rule cannot know about the announcement, which is why the imputed cells are "

         "flagged and the sensitivity analysis in §6.1.4 is run on every indicator that uses them.")



    h3(doc, "6.1.3  Bounds and guardrails")

    para(doc,

         "An imputed value is a claim about an unobserved quantity, and the claim should be bounded "

         "by what is physically possible. Every imputed price is checked against four bounds before "

         "it is written:", space_after=4)

    bullet(doc, "the value lies between the two observed anchors. Interpolation satisfies this by "

                "construction; a model-based method may not.", lead="Anchor bound — ")

    bullet(doc, "the value lies inside the crop–state plausible band used by R14. A price of ₹40,000 "

                "per quintal for wheat is not made more credible by being imputed.",

           lead="Domain bound — ")

    bullet(doc, "the imputed value does not move the series more than 25% from the mean of its "

                "anchors. A larger move implies the gap spans a regime change, and the gap should be "

                "left missing.", lead="Movement bound — ")

    bullet(doc, "no imputation is applied to the target variable, to a suppressed cell, or to a "

                "structural absence. These are exclusions, not bounds.", lead="Eligibility bound — ")



    para(doc,

         f"On MYP-26 the guardrails bind on {PM['imputed_cells']} cells, "

         f"{pct(PM['imputation_share'])} of the panel. All are internal gaps of three months or less; "

         f"no long gap and no edge gap was filled. {PM['market_closed_cells']} zero prices were "

         "classified as structural and left missing, which is why the completeness figure after "

         "cleaning is 98.5% rather than 100%: the remaining 1.5% is information, not failure.",

         size=9.5, italic=True, color="5C6B62")



    h3(doc, "6.1.4  Sensitivity analysis")

    para(doc,

         "The effect of imputation is measured, not assumed. The pipeline produces three versions of "

         "every indicator that uses an imputed cell: the primary series, a series with the imputed "

         "cells dropped, and a series with the imputed cells replaced by the series median. If a "

         "headline result changes sign or significance between the three, the result is reported as "

         "imputation-dependent.", space_after=4)

    table(doc,

          ["Version", "Construction", "What a difference proves"],

          [

              ("Primary", "Imputed values included, flagged", "The result as reported"),

              ("Drop-imputed", "Imputed cells set to missing; indicator computed on observed only", "Whether the result depends on invented values"),

              ("Median-fill", "Imputed cells replaced by the series median", "Whether the result depends on the imputation method rather than the data"),

          ],

          [3.2, 7.4, 5.4], size=8.1, first_col_bold=True,

          caption_text="Three-way sensitivity check for any indicator that consumes imputed values.")



    callout(doc, "A rule of thumb that survives contact with real data",

            "If more than 5% of a series is imputed, do not report a point forecast from it without "

            "an interval that includes the imputation uncertainty. If more than 10% is imputed, drop "

            "the series from the model and report the coverage gap instead.",

            space_after=8)



    # ------------------------------------------------------------------ 6.2

    h2(doc, "6.2  Outliers and transcription errors")

    para(doc,

         "An outlier is a value that is surprising given a model of how the data is generated. That "

         "definition makes the model explicit, which is useful: a value can be an outlier under one "

         "model and perfectly ordinary under another. The strategy uses three screens in increasing "

         "order of context, and treats their outputs differently.")



    h3(doc, "6.2.1  Three screens")

    table(doc,

          ["Screen", "Statistic", "Strength", "Weakness", "Role"],

          [

              ("Univariate robust", "Modified z on log price; MAD scale", "Immune to the values being tested; simple", "Ignores seasonality and cross-market information", "First pass; catches decimal slips and unit errors"),

              ("Distributional", "IQR fences (1.5× and 3×)", "Familiar; no distributional assumption", "Sensitive to a strongly seasonal series; arbitrary fences", "Cross-check, not a decision rule"),

              ("Contextual / residual", "STL or seasonal-naive residual; neighbour corroboration", "Separates a seasonal peak from an error; uses time structure", "Needs a stable seasonal pattern and enough history", "Second pass; resolves ambiguous flags"),

          ],

          [3.4, 5.0, 4.2, 4.0, 4.0], size=7.9, first_col_bold=True,

          caption_text="Three outlier screens. No single screen is trusted; a flag is confirmed or dismissed by the next.")



    para(doc,

         "The contextual screen is what distinguishes this strategy from a generic z-score filter. A "

         "festival spike and a decimal slip can have the same univariate z. The spike is corroborated "

         "by adjacent months and by other markets; the slip is not. The screen below formalises the "

         "comparison.", space_after=4)



    code_block(doc, [

        "# contextual corroboration for a flagged value",

        "neighbour_median = median(series[t-1], series[t+1])       # same crop-state",

        "cross_market      = median(price[other states, crop, t])",

        "ratio_local       = value / neighbour_median",

        "ratio_cross       = value / cross_market",

        "",

        "if 0.7 <= ratio_local <= 1.4 and 0.7 <= ratio_cross <= 1.4:",

        "    flag = 'spike_genuine'        # retain; it is a real market event",

        "elif is_mechanical(value, series_median):",

        "    flag = 'corrected'            # unit or decimal place determines the value",

        "else:",

        "    flag = 'outlier_unresolved'   # retain visibly; exclude from training",

    ], size=8.1)



    h3(doc, "6.2.2  Typo or event? A decision matrix")

    table(doc,

          ["Evidence", "Mechanical error", "Genuine event", "Decision"],

          [

              ("Ratio to series median near 0.01, 0.1 or 10", "Yes", "Unlikely", "Correct by factor; log"),

              ("Corroborated by adjacent month", "No", "Yes", "Retain; flag genuine"),

              ("Corroborated by other markets", "No", "Yes", "Retain; flag genuine"),

              ("Matches a documented event (festival, drought, policy)", "No", "Yes", "Retain; annotate the event"),

              ("Isolated, no corroboration, no mechanical factor", "Maybe", "Unlikely", "Flag unresolved; exclude from training"),

              ("Outside the physical domain", "Yes", "No", "Correct if factor is diagnostic, else reject"),

          ],

          [6.4, 3.4, 3.2, 4.0], size=8.1, first_col_bold=True,

          caption_text="Decision matrix for an anomalous value. The default when evidence is absent is to flag, not to delete.")



    para(doc,

         f"In the reference run R06 had already corrected the decimal slips and unit-drift cells "

         f"before the outlier screen ran, so the screen inherited a series in one unit and at one "

         f"scale. A genuine spike was still flagged and retained, and {PM['outliers_flagged']} values "

         "were flagged unresolved. Two of the seven planted digit errors stayed inside the robust "

         "band because the seasonal variation in their series was large enough to inflate the MAD "

         "scale. That is the honest limit of a univariate screen, and it is why the contextual "

         "screen is specified as the second pass rather than as an optional refinement.")



    h3(doc, "6.2.3  Treatment policy")

    bullet(doc, "correct only when the cause determines the value. A unit error and a one-place "

                "decimal slip are determinate; a digit change from 4,000 to 4,800 is not.",

           lead="Correct — ")

    bullet(doc, "retain and flag values that are surprising but corroborated. The flag travels with "

                "the value into every downstream table.", lead="Retain — ")

    bullet(doc, "flag and exclude uncorroborated values from model training, while leaving them "

                "visible in the clean table. Exclusion is a modelling decision; deletion is a data "

                "decision, and they are not the same.", lead="Exclude — ")

    bullet(doc, "never winsorise a price by default. Winsorising replaces the most informative "

                "observations with a percentile and makes the series look better behaved than it was.",

           lead="Do not — ")



    # ------------------------------------------------------------------ 6.3

    h2(doc, "6.3  Entity and unit harmonisation")

    h3(doc, "6.3.1  Crop master and fuzzy matching")

    para(doc,

         "The crop master holds a canonical code, the notified name, common synonyms and a variety "

         "flag. Matching is exact on a normalised string first (case-folded, whitespace-collapsed, "

         "punctuation removed), then fuzzy with a similarity threshold, then manual. The thresholds "

         "matter because a false merge is worse than a missed merge: merging 'Rice' and 'Paddy' "

         "silently changes what is being priced, while failing to merge them produces an obvious "

         "duplicate series that someone will notice.")

    table(doc,

          ["Similarity", "Action", "Example"],

          [

              ("1.00 after normalisation", "Automatic map", "'SOYABEAN' â†’ SOYBEAN"),

              ("0.92 – 0.99", "Automatic map with log entry", "'Wheat FAQ' → WHEAT, variety=FAQ"),

              ("0.80 – 0.91", "Manual review queue", "'Onion (Nashik)' → ONION, market attribute"),

              ("< 0.80", "No match; reject the row", "'Bajra' is a different crop, not a typo"),

          ],

          [4.0, 6.0, 6.0], size=8.1, first_col_bold=True,

          caption_text="Fuzzy-matching thresholds. The asymmetric cost of a false merge sets the conservative cut-off.")



    h3(doc, "6.3.2  Geography with effective dates")

    para(doc,

         "Names change; codes persist. Every geography row carries an LGD code and a validity "

         "interval. A district split in 2018 has one parent code valid to the split date and two child "

         "codes valid after it. Aggregating across the split requires an explicit mapping decision, "

         "not a string replace.")

    table(doc,

          ["Raw name", "Period", "Canonical resolution", "Method"],

          [

              ("Telangana (new state)", "2014 onward", "LGD 36, carved from Andhra Pradesh", "Effective-dated map"),

              ("Maharastra", "All", "Maharashtra, LGD 27", "Spelling map"),

              ("MP", "All", "Madhya Pradesh, LGD 23", "Abbreviation map"),

              ("Ahmednagar", "2018 onward", "Ahilyanagar, same LGD code", "Rename; code unchanged"),

              ("Pune (rural)", "All", "Pune district, with a market attribute", "Name is not a district key"),

          ],

          [4.0, 2.8, 6.4, 3.4], size=8.1, first_col_bold=True,

          caption_text="Geography resolutions. The code is the key; the name is a label with a validity period.")



    h3(doc, "6.3.3  Units and currency")

    table(doc,

          ["Quantity", "Common source units", "Canonical", "Conversion"],

          [

              ("Price", "INR/kg, INR/quintal, INR/tonne", "INR/quintal", "1 quintal = 100 kg = 0.1 tonne"),

              ("Production", "tonnes, '000 tonnes, lakh tonnes", "'000 tonnes", "1 lakh = 100; 1 tonne = 0.001 '000 t"),

              ("Area", "acres, hectares, '000 hectares", "hectares", "1 ha = 2.471 acres"),

              ("Yield", "kg/ha, t/ha, quintal/ha", "t/ha", "1 t/ha = 10 quintal/ha = 1,000 kg/ha"),

              ("Currency", "USD, EUR, INR", "INR", "Dated RBI reference rate; store the rate with the row"),

              ("Deflation", "Nominal INR", "Real INR (2011-12 base)", "CPI or WPI, with the index vintage recorded"),

          ],

          [2.6, 5.4, 3.4, 5.6], size=8.1, first_col_bold=True,

          caption_text="Conversion table. Factors live in code and in the unit table, never in a comment.")



    para(doc,

         "Currency conversion has a subtlety that unit conversion does not: the rate is dated. A USD "

         "price converted at today's rate and joined to a 2019 INR series mixes a 2019 quantity with a "

         "2026 relative price. The rate must be the one in force at the observation date, and it must "

         "be stored with the row so the conversion is reversible.")



    # ------------------------------------------------------------------ 6.4

    h2(doc, "6.4  Duplicates, conflicts and survivorship")

    para(doc,

         "Survivorship is the rule that decides which row lives when two rows describe the same fact. "

         "It is a policy, not a data property, and it must be written before the first conflict is "

         "encountered. The MYP-26 order is:", space_after=4)

    bullet(doc, "source precedence: the designated series for that indicator wins over a secondary "

                "aggregator.", lead="1 — ")

    bullet(doc, "vintage: the release that was current at the retrieval date wins over an older "

                "snapshot, unless the analysis is explicitly point-in-time.", lead="2 — ")

    bullet(doc, "completeness: the row with more non-null fields wins.", lead="3 — ")

    bullet(doc, "recency: the later retrieval wins.", lead="4 — ")

    bullet(doc, "stable tie-break: the lower row identifier wins, so the outcome is deterministic.",

           lead="5 — ")



    para(doc,

         "Conflicts across sources are not resolved by averaging. An average of two disagreeing "

         "sources is a number that neither source published, and it hides the disagreement that a "

         "reader needs to see. The strategy records both values, uses the precedence winner, and "

         "reports the difference in the reconciliation table.", space_after=4)



    table(doc,

          ["Indicator", "Precedence 1", "Precedence 2", "Tolerance", "On breach"],

          [

              ("Production", "DES", "FAOSTAT", "5%", "Investigate; report both; do not average"),

              ("Wholesale price", "Agmarknet", "data.gov.in mirror", "3%", "Use Agmarknet; record difference"),

              ("Yield", "DERIVED (production ÷ area)", "DES reported yield", "5%", "Prefer derived; log discrepancy"),

              ("Trade", "UN Comtrade", "ITC Trade Map", "5%", "Investigate HS-code and period alignment"),

              ("Exchange rate", "RBI reference rate", "World Bank", "1%", "Use RBI; store both"),

          ],

          [3.6, 4.0, 4.0, 2.2, 5.2], size=8.0, first_col_bold=True,

          caption_text="Source precedence by indicator. The tolerance is the point at which a difference stops being rounding.")



    # ------------------------------------------------------------------ 6.5

    h2(doc, "6.5  Revisions, vintages and suppression")

    para(doc,

         "Official agricultural estimates are revised, sometimes more than once. An advance estimate "

         "for 2024 published in July 2024 is not the same fact as the revised estimate published in "

         "February 2026, even though both are labelled '2024'. A dataset that keeps only the latest "

         "value has thrown away the information needed to backtest honestly.")

    table(doc,

          ["Release", "Published", "Production (illustrative)", "Available for a July 2024 forecast?"],

          [

              ("Advance", "2024-07-14", "1,480 kt", "Yes, at the release date"),

              ("Second", "2024-10-01", "1,450 kt", "No"),

              ("Revised", "2026-02-15", "1,502 kt", "No"),

          ],

          [2.6, 3.0, 5.4, 5.8], size=8.1, first_col_bold=True,

          caption_text="A revision triangle in miniature. A point-in-time join selects only the releases knowable at the forecast origin.")



    para(doc,

         "The as-of join is the mechanism: for each forecast origin, select the latest release whose "

         "publication date is on or before the origin. This is a single SQL predicate, and it is the "

         "difference between a backtest that means something and one that flatters the model.",

         space_after=4)

    code_block(doc, [

        "SELECT f.*",

        "FROM   fact_yield f",

        "JOIN   forecast_origin o",

        "       ON f.crop_code = o.crop_code",

        "      AND f.state_lgd = o.state_lgd",

        "      AND f.crop_year = o.crop_year",

        "WHERE  f.available_at <= o.origin_date",

        "QUALIFY ROW_NUMBER() OVER (",

        "        PARTITION BY f.crop_code, f.state_lgd, f.crop_year",

        "        ORDER BY f.available_at DESC) = 1;",

    ], size=8.1)



    para(doc,

         "Suppression is handled by doing nothing to the value and everything to the metadata. A "

         "withheld cell stays null, is flagged suppressed, and is excluded from any total that would "

         "imply a value. It is not inferred from a published total, because the arithmetic difference "

         "is exactly what the suppression was designed to prevent.")

    para(doc,

         "The same discipline applies to discontinued series. A series that stops in 2022 is not "

         "missing at random after 2022; it has ended. It is flagged discontinued, retained for "

         "history, and excluded from the current-period feature set. Imputing a discontinued series "

         "forward is the most confident way to be wrong.")





