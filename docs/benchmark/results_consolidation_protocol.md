# Benchmark V2 — Results Consolidation and Scoring Protocol

## 1. Purpose and authority

This protocol defines a deterministic, read-only reconstruction of Benchmark V2
results. The authoritative inputs are Git objects reachable from the frozen tags,
not the current working tree. A future consolidated artifact is a derived result,
not new experimental evidence.

Before consolidation, dereference every annotated tag and record its tag object
and commit. The required source families are the catalog, baseline, evaluation,
configuration, canonicalization, retry/resume, provider-conditions, rerun, and
technical/evaluation freezes. A missing, moved, or inconsistent source makes
`FROZEN_ORIGINS_VALID: NO` and stops consolidation.

## 2. Canonical experiment selection

The catalog defines exactly `CASE-001` through `CASE-030` and the mapping
`EXP-NNN -> CASE-NNN`. It is the exclusive source for case attributes (Ground
Truth provenance, difficulty, category, target family, and contrastive pair).
Ground Truth is never inferred from LLM output.

For each experiment, select exactly one normative status:

| EXP range | normative evaluation source |
| --- | --- |
| 001 | `benchmark-v2-exp-001-evaluated` |
| 002–005 | `benchmark-v2-exp-002-005-evaluated`, with the authorized recovered Ground Truth source |
| 006–010 | `benchmark-v2-exp-006-010-evaluated` |
| 011 | `REQUIRES_REVIEW`, excluded: `PROTOCOL_NONCONFORMITY` |
| 012–015 | `benchmark-v2-exp-012-015-evaluated` |
| 016 | `REQUIRES_REVIEW`, excluded under its frozen normative status |
| 017, 019, 020 | `benchmark-v2-exp-017-019-020-rerun-evaluated`, `rerun-01` only |
| 018 | valid original evaluation in `benchmark-v2-exp-017-020-inference` |
| 021, 023, 024, 025 | `benchmark-v2-exp-021-023-025-evaluated` (the tag content, not its abbreviated name, is authoritative) |
| 022 | `benchmark-v2-exp-022-evaluated` only |
| 026–030 | `benchmark-v2-exp-026-030-evaluated` |

The historical 429 episodes for EXP-017/019/020 remain operational evidence;
they are not classifications and never form a second primary row. EXP-022's
timeout-without-raw attempt is operationally conforming; its attempt-02 is the
selected first valid response.

Each included EXP must resolve to one and only one selected `llm-output.json`.
Any duplicate, absent, or ambiguous selection sets
`PRIMARY_ANALYSIS_DATASET_INTEGRITY: FAIL`.

## 3. Reconstruction gates

For each selected evaluation, verify from frozen blobs: expected configuration
and model, rendered-prompt hash provenance, selected attempt chain, first-valid
policy, raw/output hash linkage, schema validity, and Ground Truth provenance.
Require `CONFIG-GEMINI-02` and the model/configuration named by the frozen
evidence; do not trust a value supplied outside Git. The configured template SHA
is `85135355C8C1A22AEE5F693369538BED7C46E27AA106B9B933E3DC5E4B4E9A3C`.

Mandatory gates are: frozen origins valid; one selected evaluation per included
EXP; valid GT and LLM provenance; model/config consistency; prompt provenance;
and no duplicate counting. If any mandatory gate fails, no final metrics are
valid.

## 4. Scoring

Map `shouldUpdateSnapshot=true` to `SHOULD_UPDATE`, otherwise to
`SHOULD_NOT_UPDATE`. Let `g` be Ground Truth and `p` the mapped LLM class:

```
score = MATCH     if p == g
score = MISMATCH  otherwise
```

`confidence` and `reason` never participate in scoring. They may be reported
only descriptively; confidence is self-reported, uncalibrated, and is not a
validated probability. Any taxonomy derived from `reason` is
`POST_HOC_EXPLORATORY_ANALYSIS`.

Positive class is `SHOULD_UPDATE`: TP=(update, update), FN=(update,
not-update), FP=(not-update, update), TN=(not-update, not-update).

```
N = TP + TN + FP + FN
accuracy = (TP + TN) / N
precision_update = TP / (TP + FP)
recall_update = TP / (TP + FN)
f1_update = 2 * precision_update * recall_update / (precision_update + recall_update)
precision_not_update = TN / (TN + FN)
recall_not_update = TN / (TN + FP)
f1_not_update = 2 * precision_not_update * recall_not_update / (precision_not_update + recall_not_update)
macro_f1 = (f1_update + f1_not_update) / 2
balanced_accuracy = (recall_update + recall_not_update) / 2
```

If a denominator is zero, emit `NOT_APPLICABLE` (or `null`) with its reason;
never substitute zero. Compute with full precision. Display percentages may be
rounded to two decimals, while future results preserve numerator and denominator.

## 5. Inclusion and operational separation

`VALID_EVALUATION` is a derived consolidation predicate, not a persisted
experimental state. A row has `included_in_primary_analysis=true` only when its
final normative status permits inclusion, it is not excluded by
`REQUIRES_REVIEW`, `PROTOCOL_NONCONFORMITY`, or another frozen normative
exclusion, exactly one normative evaluation is selected, and every mandatory
provenance and integrity gate passes. EXP-011 and EXP-016 remain traceable but
excluded; they are neither MATCH nor MISMATCH. This predicate does not rename
historical states, create a change-control state, or modify experimental
artifacts.
Provider limits, retries, timeouts, API errors, and protocol nonconformity are
operational metrics and are never FP, FN, MATCH, or MISMATCH.

Operational summaries may report attempts, calls, timeout-without-response,
historical provider-limit episodes, rerun recovery, and protocol nonconformity.
They must remain separate from the confusion matrix and accuracy.

## 6. Permitted descriptive breakdowns

After gates pass, aggregate selected rows by Ground Truth, catalog difficulty,
catalog category, catalog target family, and catalog contrastive pair. Pair
status is `PAIR_FULLY_CORRECT` when both members are MATCH,
`PAIR_PARTIALLY_CORRECT` when exactly one is MATCH, and `PAIR_NONE_CORRECT`
when both are MISMATCH. If either member is excluded or otherwise absent from
the valid set, status is `PAIR_NOT_APPLICABLE` and the reason is recorded;
missing outcomes are never imputed. Such pair summaries are descriptive, do
not enter the confusion matrix, and do not replace primary accuracy or imply
statistical significance.

Confidence summaries (mean, median, min, max, distribution, and MATCH/MISMATCH
comparison) are descriptive only. The primary statistical scope is descriptive;
this protocol makes no population, significance, superiority, or generalization
claim.

## 7. Future consolidated artifact

A future machine-readable artifact may be stored at
`docs/benchmark/results/benchmark_v2_results.json`, with optional CSV and
derived Markdown. Each row must contain experiment/case IDs, normative status,
inclusion and exclusion reason, authoritative evaluation and GT source,
classification, score, catalog attributes, confidence (descriptive), execution
namespace, and Git provenance.

It must also record catalog and protocol tag/commit IDs, every evaluation-freeze
tag/commit, generation timestamp, schema/version, and sufficient blob hashes to
reproduce selection. It must not depend on untracked worktree files.

## 8. Completion rule

The benchmark is execution-complete when all 30 EXPs have a final normative
status. `ALL_CASES_HAVE_VALID_EVALUATION` remains false while EXP-011 and
EXP-016 are excluded. No imputation is permitted. Primary results are ready for
analysis only when all mandatory reconstruction gates pass.
