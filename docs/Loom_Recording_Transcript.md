# Loom recording transcript

**Target length:** 7–8 minutes  
**Recording setup:** Share the full screen. Keep this script open beside the submission folder. Open files only when the matching screen cue appears.

## 0:00–0:35 — Introduction

**Screen:** Open `OFFLINE_EVIDENCE_SCORECARD.png`.

Hello, I’m Kajal. This project evaluates a five-way customer-support router across `order_status`, `refund_request`, `product_issue`, `account_help`, and `other`.

My goal was not only to raise exact-match accuracy. I also measured regressions, class-level quality, output validity, latency, token use, and cost. I kept the supplied workbook analysis and the separate notebook experiment distinct because they use different evaluation artifacts and should not be combined into one causal improvement claim.

## 0:35–1:25 — Evaluation design

**Screen:** Open the workbook on the `README` sheet, then briefly show `Step 1 - Human Eval`.

The required workbook contains 150 supplied support tickets. I reviewed every prediction against the ticket text and expected category. The supplied predictions produced 121 passes and 29 failures, which is 80.67 percent accuracy.

For every failure I recorded the expected category, the observed prediction, and a human-readable failure reason. I then grouped the failures by recurring decision boundary so the prompt change would address a policy pattern rather than memorize individual wording.

## 1:25–2:10 — Failure analysis

**Screen:** Open `Step 2 - Failure Groups`.

The 29 workbook failures fall into four groups. Twelve are refund-intent misses, where explicit money-back language loses to surrounding product or delivery context. Nine are account-journey misses, including login, checkout, or account workflows that are routed elsewhere. Four are shipping-context boundary errors, and four are product-context boundary errors.

The largest actionable pattern is refund intent. This led to a focused rule: when the user explicitly asks for a refund, money back, a price adjustment, or cancellation with money returned, prioritize `refund_request`. Shipping, product, and account routes still apply when the customer is asking for status, replacement, repair, access, or another non-refund action.

## 2:10–2:55 — Prompt revision

**Screen:** Open `Step 3 - Improved Prompt`, then `Step 4 - Test Improved`.

The revised prompt makes the category boundaries explicit and asks the model to decide from the requested outcome. This is a narrow policy change based on grouped failures, not a list of answers.

In a separate workbook-aligned controlled comparison, the original prompt scored 145 out of 150 and the focused prompt scored 146 out of 150. That comparison produced one win, zero regressions, and four remaining failures. It is separate development evidence, so I do not describe it as the supplied workbook moving directly from 121 to 146.

## 2:55–4:05 — Frozen notebook comparison

**Screen:** Open `LangSmith_Evidence/01_aggregate_91_to_98.png`, then `02_eight_wins.png`.

The executed notebook contains a second, frozen 100-case development comparison. On this set, baseline V1 scored 91 percent and focused V2 scored 98 percent, a seven-point increase.

The outcome accounting is important: 90 examples stayed correct, eight changed from wrong to right, one changed from right to wrong, and one remained wrong. These totals reconcile to all 100 examples. The eight wins correct multi-intent cases where refund language had previously overridden the underlying order-status or product-issue request.

## 4:05–4:55 — Regression and why the decision is Review

**Screen:** Open `LangSmith_Evidence/03_one_regression.png`, then `05_regression_trace.png`.

The V2 result is not an automatic pass. The single regression is a misleading wireless-product-description ticket. V1 matched the reference `product_issue`, while V2 predicted `other`.

The regression rate uses previously correct cases as its denominator: one regression divided by 91 V1-correct cases equals 1.10 percent. The pass bar was at most 1 percent, so the dashboard correctly marks the candidate as Review even though overall accuracy reached 98 percent. I would keep the prompt as a candidate, inspect this boundary, and require another independent validation before release.

## 4:55–5:35 — Trace-level evidence

**Screen:** Open `LangSmith_Evidence/04_corrected_trace.png`.

LangSmith preserves the input, structured output, model reasoning, latency, token count, and cost. This corrected trace shows a missing-order ticket moving to `order_status`, which matches the reference. The regression trace shown earlier preserves the counterexample. Together, the aggregate view and trace views make both the gain and its limitation auditable.

## 5:35–6:20 — Operational trade-off

**Screen:** Return to `OFFLINE_EVIDENCE_SCORECARD.png`, then show page 6 of `Customer_Support_Evaluation_Case_Study.pdf` if time permits.

The quality increase costs more. In the notebook comparison, mean latency rose from 0.773 to 0.855 seconds, and p95 latency rose from 1.028 to 1.510 seconds. Mean tokens increased from 241.52 to 476.46. Total cost for 100 runs rose from about 0.00469 dollars to 0.00830 dollars.

The improvement is therefore a quality-versus-cost trade-off, not a free gain. Output validity remained 100 percent in both experiments.

## 6:20–7:05 — Remaining risks and next step

**Screen:** Open page 7 of `Customer_Support_Evaluation_Case_Study.pdf`.

Both comparisons are development evidence. They do not establish organizer-hidden or production performance. The workbook and notebook also follow different policy definitions, so their scores should not be merged.

The notebook set contains seed cases and paraphrases, which limits independence. Later experiments informed by observed benchmark behavior are deliberately excluded from this submission. The next defensible step is to freeze one candidate prompt and evaluate it once on a new, independently authored and adjudicated set, keeping the result whether it passes or fails.

## 7:05–7:35 — Close

**Screen:** Return to the submission folder.

The final package includes the completed workbook, executed notebook, detailed 22-page case study, raw V1 and V2 exports, selected LangSmith screenshots, hashes, and this narration. The main result is a clear accuracy improvement with fully reconciled wins and regressions, accompanied by an explicit Review decision because the regression gate is slightly missed. Thank you.
