# Rules and Standards in the Supreme Court of Canada — replication data

Data and prompts for **Norman Siebrasse, "AI-Assisted Pairwise Comparison for Large-Scale Jurisprudential Analysis: The Fifty-Year Shift from Rules to Standards in the Supreme Court of Canada"**, *Journal of Empirical Legal Studies* (forthcoming). The article's online Appendix is published with it as supplementary material.

The article ranks 3373 Supreme Court of Canada decisions from 1974 to 2024 on a rules–standards spectrum by asking an AI model which of two decisions sets out the more rule-like test, many thousands of times, and aggregating the comparisons with the Bradley–Terry model. This repository contains every comparison made, the resulting case-level dataset on which the article's analyses run, the two prompts exactly as used, and a version of the comparison prompt for readers who want to try the rubric on cases they know.

Everything here is released under the Creative Commons Attribution 4.0 licence (see `LICENSE`). If you use the data, please cite the article.

## Contents

```
data/
  cases.csv                            case-level analysis dataset, 3373 cases (1974–2024)
  cases_extension_1960_1973.csv        case-level dataset for the 1048 pre-1974 cases
  bt_scores_extended_1960_2024.csv     Bradley–Terry scores for all 4421 cases on one scale
  comparisons_final.csv                the 53,355 comparisons behind the final ranking
  comparisons_original.csv             the 46,635 comparisons behind the ranking at convergence
  comparisons_extension_1960_1973.csv  the 14,867 comparisons that integrate the pre-1974 cases
  consistency_pro.csv                  954 pairs × 8 repetitions, Gemini 2.5 Pro, full text
  consistency_pro_reasons_only.csv     the same 954 pairs × 8, Gemini 2.5 Pro, reasons only
  consistency_flash.csv                the same 954 pairs × 8, Gemini 2.5 Flash
  consistency_gpt56_sol.csv            350 of the pairs × 8, GPT-5.6 Sol (high reasoning effort)
  consistency_gpt52.csv                350 of the pairs × 8, GPT-5.2 (no reasoning)
prompts/
  comparison_prompt.py                 the comparison prompt, as run (Appendix A3)
  screening_prompt.py                  the informativeness screening prompt, as run (Appendix A4)
  comparison_prompt_web.md             the comparison prompt adapted for use by hand
  comparison_prompt_web_instructions.pdf   how to use it, and how it differs from the production prompt
README.md
LICENSE
```

The decision texts themselves are not in the repository: see *Provenance*.

## Provenance

The decisions are the English-language versions of all Supreme Court of Canada decisions in the **A2AJ Canadian Case Law** dataset (Rehaag, Wallace and McCarten 2025, https://huggingface.co/datasets/a2aj/canadian-case-law), downloaded on **13 June 2025**. The base dataset comprises every decision in that download with a `document_date` of 1 January 1974 or later: 4458 decisions. Three categories were excluded: 2 French-language decisions that appeared in error in the English-language set (the dataset has since been corrected and they no longer appear), 43 procedural orders, and 1040 decisions that the screening prompt (`prompts/screening_prompt.py`) found to contain no legal test amenable to analysis. The remaining **3373** decisions are the article's dataset (§ 2.1 of the article).

The pre-Charter extension (§ 3.5.2) adds every informative decision from 1960 to 1973 from the same source, screened in the same way: **1048** decisions.

`ParqRow` is the case identifier throughout this repository. It is the row index of the decision in the A2AJ download of 13 June 2025, which was frozen for the project; row indices are not stable across versions of the dataset, so a current download will not match. For matching the posted files to decision texts, key on the citation (`Citation` in `cases.csv`, `True_CitationA`/`True_CitationB` in the comparison files, `citation_en` and `url_en` in the extension file) rather than on `ParqRow`.

## Which ranking the article uses

All results in the article and Appendix are computed from the **final ranking**: the Bradley–Terry model estimated on all 53,355 comparisons in `comparisons_final.csv` with the choix library's iterative Luce spectral ranking estimator (`choix.ilsr_pairwise`, choix 0.3.6, α = 10⁻⁸; ties entered as a win for each case). That ranking is the `RankNum` column of `cases.csv` (1 = most standard-like, 3373 = most rule-like) and its scores are the `BT_Score` column. Running the estimator as specified below on `comparisons_final.csv` reproduces all 3373 ranks exactly.

`cases.csv` also carries two earlier rankings, for the comparisons reported in Appendix A1.1 and A1.2.2: `RankNum_preconsistency`, the same estimator applied to the 46,635 comparisons in `comparisons_original.csv` (reproducible from that file), and `RankNum_original`, the ranking at convergence, estimated by an iterative maximum-likelihood algorithm with Laplace smoothing implemented in code written for the project. That code is not posted, so `RankNum_original` is provided for reference only.

No case-level standard errors are posted for the final ranking. The article's uncertainty statements concern annual means and are computed from the spread of cases within years (§ 2.2.2), not from case-level standard errors; the latter can be computed from `comparisons_final.csv` if needed.

## The data files

### Comparison files

`comparisons_final.csv`, `comparisons_original.csv`, `comparisons_extension_1960_1973.csv` and the five `consistency_*.csv` files share one row format: one row per comparison, the two decisions as presented to the model (A and B), the model's structured output, and run metadata.

| Column | Meaning |
|---|---|
| `ParqRowA`, `ParqRowB` | Case identifiers of Decision A and Decision B |
| `True_CitationA`, `True_CitationB` | Neutral or SCR citation of each decision |
| `CaseA_TestA`, `CaseB_TestB` | The model's summary of the most important test it identified in each decision (the `name` field of the output) |
| `BaselineA`, `BaselineB` | The model's statement of the test's baseline — statute, common law or both, with the provision or leading case |
| `SubjectOutA`, `SubjectOutB` | The subject the model selected for the test, from the decision's cleaned official subjects (§ 2.3.1) |
| `JudgeA`, `JudgeB` | The author of the reasons containing the test, as identified by the model |
| `Score` | The model's comparison score: 2 or 1 (Test A more rule-like), 0 (approximately equal), −1 or −2 (Test A more standard-like). Only the sign is used in estimation (Appendix A1.2.1) |
| `Score_Desc` | The verbal description corresponding to the score |
| `Model` | Model identifier as returned by the API |
| `Prompt_Tokens`, `Thoughts_Tokens`, `Candidates_Tokens`, `Total_Tokens` | Token counts for the request: prompt, model reasoning, output, total |
| `RunTag` | The batch in which the comparison was run. `R1_retrieve` … `R63_retrieve`: the adaptive sampling rounds (§ 2.2.2). `Duplicate_Long`, `Duplicate_Medium`, `Duplicate_Short`: 2,000 repeat comparisons of pairs already in the dataset, selected by the length of the decisions (1,000 long pairs — both decisions long, one extremely long, or a large length mismatch — 500 at the 40th–60th percentile of combined length, and 500 of the shortest), run in August 2025 as an early check on consistency and on length bias; their outcomes entered the dataset like any other comparison. `Consistency`: in `comparisons_final.csv` only, the 6,720 outcomes of the 840 original consistency pairs (§ 2.2.3) |
| `EdgeId` | Pair identifier, `ParqRowA_ParqRowB` |
| `YearA`, `YearB`, `YearGap` | Decision years and their difference |
| `RetestFlag` | 1 if the pair was a targeted retest during convergence testing (§ 2.2.2), else 0 |

Additional columns in particular files:

- `consistency_pro.csv` — `Stage`: `original_840` for the 840 pairs whose 6,720 outcomes were added to the dataset before the final estimation, `top-up_114` for the 114 pairs added later to the close strata, whose outcomes were not (§ 2.2.3 n 27; Appendix A1.2.2). The endogeneity check in A1.2.2 depends on this distinction.
- `consistency_pro_reasons_only.csv` — `Series`: run label.
- `consistency_gpt56_sol.csv` — `Reasoning_Effort` (`high`). `consistency_gpt52.csv` and `consistency_gpt56_sol.csv` lack the `RunTag`, `EdgeId` and year columns; pairs are identified by `ParqRowA` and `ParqRowB`. The GPT-5.2 run used the production prompt with the following block appended after the case information, to obtain reliably parseable output (Appendix n 7); the substantive guidelines were unchanged:

  ```
  ***REMINDER: OUTPUT FORMAT***
  Respond with ONLY a valid JSON object. No introduction, no explanation, no markdown formatting. Begin your response with { and end with }.
  ```

**How the comparison files relate.** `comparisons_original.csv` holds the 46,635 comparisons at which convergence was declared. `comparisons_final.csv` = those 46,635 + the 6,720 outcomes of the 840 original consistency pairs (`consistency_pro.csv`, `Stage = original_840`). Those 6,720 rows carry `RunTag = Consistency` in the final file. The top-up pairs' outcomes appear only in `consistency_pro.csv`. `comparisons_extension_1960_1973.csv` holds the 14,867 comparisons used to place the 1048 pre-1974 cases on the final ranking's scale (mixed pairs of old and new cases, and pairs of new cases from different periods); they were not used to re-estimate the 3373 original cases.

**Consistency strata.** The consistency sample was stratified by rank distance in the final ranking: B1 0–10, B2 11–25, B3 26–50, B4 51–100, B5 101–250, B6 251–500, B7 501–1000, B8T1 1001–1500, B8T2 1501–2000, B8T3 > 2000. The files do not carry a stratum column: compute the absolute difference between the two cases' `RankNum` in `cases.csv` and apply these cut-offs, which reproduces the stratum assignment of all 954 pairs exactly. The Flash run and both Pro runs cover all 954 pairs. The two OpenAI runs cover the same 350 pairs, 50 from each of seven strata: B5, B6, B7, B8T1, B8T2, B8T3, and 50 drawn from the 200 pairs of B1–B4 pooled (rank distance 1–100). Table A4 of the Appendix reports B6–B8T3; the pooled close stratum and B5 are in the files but not reported, because at those separations the ranking itself is not resolved and agreement with it is uninformative (Appendix A1.2.3). The cross-model agreement figures in the article (§ 2.2.3, Table A4) accordingly use only pairs more than 250 ranks apart.

### `cases.csv` — the case-level dataset (3373 rows)

Everything in § 3 of the article and Part A2 of the Appendix runs off this file.

| Column | Meaning |
|---|---|
| `ParqRow` | Case identifier |
| `RankNum` | Final rank, 1 (most standard-like) to 3373 (most rule-like) |
| `RankNum_preconsistency` | Rank from the same estimator applied to the 46,635 pre-consistency comparisons (Appendix A1.1, A1.2.2) |
| `RankNum_original` | Rank at convergence, from the superseded iterative estimator; reference only (Appendix A1.1) |
| `BT_Score` | Final Bradley–Terry score (log-odds scale) |
| `NumComparisons`, `NumOpponents` | Number of comparisons involving the case; number of distinct cases it was compared with |
| `Citation`, `Case_name`, `Decision_date`, `Year` | Citation, style of cause, date of release, year |
| `CharCount` | Characters in the full text as downloaded, including headnote |
| `ReasonsCharCount` | Characters from the first occurrence of "delivered by", "delivered orally by", "delivered the following judgment orally" or "rendered by" to the end of the text, including trailing material (disposition, solicitors, notes); used to extract the reasons-only texts for the comparison in Appendix A1.2.4, and not otherwise used in the analyses. It equals the sum of `Count1`–`Count6` in 3025 cases and differs by 100 characters or less in 265. In 83, mostly from 1974–1983, the first match is misplaced: before the reasons in 50, overstating the count, and after the opening opinion in 33, understating it. The length variable in § 3.4 and § 3.5.4 is `Count_Author_Test` |
| `Subject` | The subject(s) of the test as selected by the model across the case's comparisons, after cleaning (§ 2.3.1) — the subjects listed in `SubjectWeights`, in the same order, separated by a pipe, e.g. `Statutes \| Transportation`. This is not the menu of subjects offered to the model, which can differ (Appendix A1.3) |
| `SubjectWeights` | The same subjects with fractional weights, in alphabetical order, e.g. `Constitutional:0.62;Criminal_law:0.38`, reflecting how often the model selected each across the case's comparisons, subject to the hand decisions flagged by `IsManual` |
| `PrimarySubject` | The subject with the largest weight |
| `Author_Test` | Author of the reasons containing the most important test, as identified by the model (the modal value across the case's comparisons) |
| `Count_Author_Test` | Characters in that set of reasons — the length variable used in § 3.4 and § 3.5.4 |
| `Panel`, `PanelSize` | Judges sitting, `\|`-separated; their number |
| `Author1` … `Author6`, `Type1` … `Type6`, `Join1` … `Join6`, `Count1` … `Count6` | Each set of reasons in the decision: its author, its type (Majority, Concurrence, Dissent or Unanimous; `TheCourt` for reasons attributed to The Court rather than a named judge, see § 2.3.2; and `Order`, for one case — an order of a single judge granting a stay of execution, which passed the informativeness screen because it articulates and applies a test), the judges joining it, and its character count |
| `IsManual`, `ManualConfidence` | 1 for the 65 cases whose final subject assignment required a decision made by hand, and the confidence recorded for it (High, Medium or Low); otherwise `IsManual` is 0 and `ManualConfidence` is `N/A`. There are three groups: the 41 cases with no official subject for which the AI supplied no usable subject, assigned from the headnote and keywords (Appendix A1.3 n 24); 13 further cases with no official subject, in which the AI's selections — many of them `[Subject not found]` or catchword variants of official subjects — were resolved by hand to an official subject (A1.3 n 23); and 11 cases from 1997–2010 with three or more official subjects, only two of which were offered to the model, in which the weights were set by hand from the AI's selections (A1.3 n 21) |

### `cases_extension_1960_1973.csv` — the pre-1974 cases (1048 rows)

Same conventions where the columns coincide. These cases were placed on the final ranking's scale by a constrained Bradley–Terry fit that froze the scores of the 3373 original cases (Appendix A2.3); they have `BT_Score` and `BT_SE` but no rank, and the article's extended series (Figure 5, Figures A6–A7) is therefore in scores. `BT_SE` is the standard error from the constrained fit; because the main-run scores were held fixed, it conditions on them and understates the total uncertainty. Subjects for the extension cases were assigned as for the main dataset (§ 2.3.1): the model was asked, in each comparison, which subject the test it identified belonged to, and `SubjectWeights` records how often each was selected, with `Subject` and `PrimarySubject` as in `cases.csv`. The model was offered only the first of a case's official subjects — 62 of the 1048 cases have more than one — but it selected from the full official list where the keywords in the decision text showed a second subject, as it did in the main run, so the weights reflect the official subjects, not only the one offered. The weights reproduce from `SubjectOutA` and `SubjectOutB` in `comparisons_extension_1960_1973.csv`, after the 44 cases whose official subject was one of the four retired labels — the three dissolved categories and International Law, which was split (§ 2.3.1) — are reassigned case by case as in the main dataset; the reassignment is reflected in the posted file, and the 44-case mapping is available from the author on request. Reasons are listed as `Author1` … `Author9`, `Type1` … `Type9`, `Join1` … `Join9`. The panel data for these cases were extracted with a revised version of the code used for `cases.csv`, which additionally codes a reason type of Plurality for the largest grouping in a decision in which no opinion commands a majority; `cases.csv`, on which the article's figures rest, codes such reasons as Majority. Other columns: `citation_en`, `name_en`, `document_date_en`, `url_en`, `has_english_text`, `Language` (from the A2AJ download); `char_count`, `ReasonsCharCount`; `Unanimous`, `panel_size`, `Panel`, `Did_not_participate`, `Judgment`, `Notes`; `is_informative` (the screening result; all rows are `True`).

### `bt_scores_extended_1960_2024.csv` (4421 rows)

`ParqRow`, `Year`, `BT_Score`, `BT_SE`, `Citation`, `is_new` for all 4421 cases on the common scale; `is_new` is `TRUE` for the 1048 inserted cases and `FALSE` for the 3373 frozen ones. `BT_SE` is given for the inserted cases only (see the note on the extension file) and is blank for the frozen cases. This file is derivable by stacking the score columns of the two case files; it is provided because it is the direct input to the extended-series analyses.

## Code

I have not posted analysis code. The ranking is a single call to a standard library and the analyses are standard methods; every method and parameter is stated in the specification below. That is the level at which I think the results should hold. Where the specification leaves an implementation choice open — the LOESS routine, the bootstrap seed, the optimizer — I varied it in the course of the work and it made no difference to the conclusions. If you find a choice that does, that is a real result and I would like to hear about it.

Two kinds of replication are possible with what is here. You can re-run the analysis: the data files and the specification are enough for an AI coding assistant to do the whole of it, and that is how the final ranking was checked before posting — reproduced from `comparisons_final.csv` and the call given below. Everything computed directly from the ranking (the ranks, the annual means, the subject and judge means, the length slopes, the tables of scores and ties) should reproduce exactly; quantities read from smoothed series (the peak and trough values, the composition and length shares, the breakpoint fits) should reproduce to the precision at which the article reports them, since LOESS implementations differ at the margin. You can also re-run the measurement. The prompt is the instrument, it is posted exactly as run, and the decisions are freely available, so the comparisons can be regenerated for any pair, any sample, or the whole dataset, with the same model or another; the `consistency_*` files are that exercise on 954 pairs across four models.

The material, and the prompt in particular, is released under the Creative Commons Attribution 4.0 licence and may be modified and extended. A replication need not reproduce the prompt's typographical errors, which are corrected in `prompts/comparison_prompt_web.md`. Discrepancies and results: norman.siebrasse@gmail.com.

## Specification of the estimation and analyses

The parameters of every estimation and analysis in the article, stated once, with pointers to the section that reports the result.

**Bradley–Terry ranking (§ 2.2.2; Appendix A1.1).** Input: for each comparison, the two case identifiers and the direction of the result (`Score` > 0: A wins; < 0: B wins); the intensity of the score (±1 vs ±2) is discarded. A tie (`Score` = 0) is entered as one win in each direction — which gives a tie twice the weight of a decisive comparison; entering ties at half weight instead moves cases by a median of 3 ranks and leaves annual mean ranks essentially unchanged (correlation 0.99998; no annual mean moves by more than 3 ranks) (Appendix A1.2.1 n 5). Estimation: `choix.ilsr_pairwise(n_items, data, alpha=1e-8)`, choix version 0.3.6 (Maystre and Grossglauser 2015). The regularization α = 10⁻⁸ is applied because the unregularized estimate (α = 0) fails when some cases have won or lost every comparison in which they appeared; results are insensitive to α (at 10⁻⁶ no case moves more than 6 ranks; at 10⁻⁴ the median shift is 29 ranks and annual mean ranks correlate at 0.9995). Scores are log-strengths with mean zero. Ranks are assigned from the scores, 3373 to the highest (most rule-like). Estimating instead by weighted logistic regression (scikit-learn `LogisticRegression`, one indicator per case, no intercept, C = 10, ties as half a win each) moves cases by a median of 23 ranks, with annual mean ranks correlating at 0.9997 (§ 2.2.2 n 25).

**Pre-Charter extension (§ 3.5.2; Appendix A2.3).** A constrained Bradley–Terry fit on `comparisons_extension_1960_1973.csv`: the Bradley–Terry log-likelihood over the 1048 new cases' parameters only, with the 3373 final scores held fixed as offsets; ties as half a win each; L2 penalty with C = 10 on the new parameters; optimized with scipy `minimize(method="L-BFGS-B")`. Standard errors are from the inverse penalized Hessian and condition on the fixed scores. Annual means for 1960–1973 are insensitive to the penalty (within 0.36 log-odds with the penalty removed). The extended series is analysed in scores, not ranks.

**Annual series and smoothing (§ 3.1).** The unit of analysis is the mean rank (or score, for the extended series) of all cases released in a calendar year. Smoothed curves are LOESS with span 0.3, except Figure 8 (span 0.2).

**Confidence bands (§ 2.2.2; Figures 1, A5).** 95% bootstrap bands from 2,000 replicates, resampling cases with replacement within each year, conditional on the estimated ranking.

**Subject means (§ 3.2) and judge bias (§ 3.3).** Subject mean rank = fractionally weighted mean of `RankNum` over the cases assigned to the subject (`SubjectWeights`), reported for subjects with more than 50 cases. Judge adjusted bias = mean over the judge's cases of (`RankNum` − expected rank given the case's subjects), reported for judges with more than 25 cases; the 88 cases in which different comparisons attributed the test to different judges are excluded (§ 3.3 n 38).

**Length effect (§ 3.4; Appendix A2.2).** OLS of `RankNum` on log10(`Count_Author_Test`), the length of the reasons containing the test; pooled slope −566 ranks per tenfold increase. Within-period slopes are reported in § 3.4 n 39.

**Composition analysis (§ 3.5.3; Appendix A2.4).** Shift–share: predicted mean rank for a year = Σ over subjects of (subject mean rank × the subject's fractional share of the year's cases); residual = observed − predicted. Subject means are computed under three baselines — early (1980–1989), pooled (1974–2024) and late (2015–2024) — with subjects thinly represented in the baseline window aggregated into a residual category. The composition share of the decline is measured on the smoothed series from the 1982 peak to the 2024 endpoint. The projected composition series for 1960–1982 in Figure 5 uses pre-Charter (1974–1981) subject means, level-aligned to the observed series over 1960–1974.

**Length decomposition (§ 3.5.4; Appendix A2.5).** Predicted rank from length alone, using two baseline slopes: pre-Charter, −560, and late-Charter, −396 ranks per tenfold increase in `Count_Author_Test`; residual = observed − predicted. The length-associated share of the decline is measured as for composition.

**Structural breaks (§ 3.5.5; Appendix A2.5).** Bai–Perron on the annual mean Bradley–Terry scores of the extended series, k = 2 (breaks 1981 and 2001; BIC marginally prefers k = 3). Chow test scan over candidate break years on the annual means of the extended series (1960–2024), and on case-level scores; both place the primary break at 1987. The same tests applied to the length-adjusted residual under both baseline slopes.

## Not included

The data behind the context-window diagnostics of Appendix A1.2.5 (the 966-comparison nonlinearity test and the 100-case Pro/Flash comparison) are held in several working files and are available from the author on request. The human validation comparisons (§ 2.2.4) are described in the article and not posted; the pairs used and the results are available on request. The per-year series plotted in the figures are not posted separately; every figure can be regenerated from `cases.csv` and the extended-scores file with the parameters given below.

## Trying the prompt yourself

`prompts/comparison_prompt_web.md` is the comparison prompt adapted for use through a web interface; `prompts/comparison_prompt_web_instructions.pdf` explains how to use it and lists every difference from the production prompt. Upload the prompt file and the full text of two decisions to a capable model and ask it to compare them.

## Citation

Siebrasse, Norman. [year]. "AI-Assisted Pairwise Comparison for Large-Scale Jurisprudential Analysis: The Fifty-Year Shift from Rules to Standards in the Supreme Court of Canada." *Journal of Empirical Legal Studies* [volume]: [pages]. Data: https://github.com/nsiebrasse/rules-standards-scc.

Estimator: Maystre, L., and M. Grossglauser. 2015. "Fast and Accurate Inference of Plackett–Luce Models." *Advances in Neural Information Processing Systems* 28. Software: https://github.com/lucasmaystre/choix.

Decision texts: Rehaag, S., S. Wallace, and C. McCarten. 2025. "A2AJ Canadian Case Law." Dataset. Hugging Face. https://huggingface.co/datasets/a2aj/canadian-case-law.

## Contact

Norman Siebrasse, Professor of Law, University of New Brunswick — norman.siebrasse@gmail.com
