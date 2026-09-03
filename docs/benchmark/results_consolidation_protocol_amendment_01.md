# Benchmark V2 — Results Consolidation Protocol Amendment 01

## Status and scope

**Amendment type:** `POST_EXPERIMENT_PROVENANCE_SCOPE_AMENDMENT`.

This document complements `docs/benchmark/results_consolidation_protocol.md`
frozen at `benchmark-v2-results-consolidation-protocol`
(`6a2c37446ca9de22b4538f62f0540408b47a708a`; blob
`5380a1bb25a1b6d00e4e1f4d484b22c74a7935ee`). It does not edit or replace
the original protocol except, where they conflict, for provenance and
presentation rules for descriptive case attributes.

This is a post-experiment correction of provenance scope and result
presentation. It was motivated by a forensic review finding that the frozen
catalog does not provide complete, deterministic coverage of `difficulty`,
`category`, `targetFamily`, or a general per-case `contrastivePair` attribute.
It must not be represented as a rule that existed before the experiment.

Absence of sufficient provenance for a descriptive analysis does not authorize
retrospective reconstruction, inference, imputation, or promotion of later
metadata to historical authority. Such an analysis is
`NOT_AVAILABLE_FOR_REPRODUCIBLE_AGGREGATION`.

## Non-amendment of experimental evidence

This amendment changes none of the following: the 30-case catalog; EXP-to-CASE
mapping; Ground Truth; `SHOULD_UPDATE` and `SHOULD_NOT_UPDATE`; LLM outputs;
normative evaluation selection; EXP-011 and EXP-016 status; rerun handling for
EXP-017/019/020; EXP-018 and EXP-022 selection; first-valid-response policy;
model, configuration, prompt, exclusions, MATCH/MISMATCH, positive class,
confusion matrix, formulae, primary metrics, operational metrics, confidence,
or reason.

Consequently, no primary numerical result may change because of this amendment.
Model/config consistency, prompt provenance, and first-valid policy remain
mandatory; this amendment does not relax known implementation gaps for them.

## Primary Reproducible Results

`PRIMARY_RESULTS_REPRODUCIBLE` is `PASS` only when every original provenance
and integrity gate necessary for the following results passes:

- catalog, included, and excluded totals and excluded list;
- Ground Truth, selected LLM class, MATCH/MISMATCH, and mismatch IDs;
- TP, FP, FN, TN, accuracy, precision, recall, F1, macro-F1, and balanced
  accuracy;
- operational conditions defined by the original protocol; and
- directly preserved confidence as descriptive information only.

This gate is independent of complete provenance for `difficulty`, `category`,
and `targetFamily`. It does not weaken any gate required for primary results.

## Descriptive attribute availability

`DESCRIPTIVE_ATTRIBUTE_PROVENANCE_COMPLETE` is derived, never presumed. It is
`YES` only when frozen, deterministic sources cover every required row for each
of `difficulty`, `category`, and `targetFamily`, with reproducible provenance.

When applicable coverage is not complete:

```text
DIFFICULTY_BREAKDOWN_STATUS = NOT_AVAILABLE_FOR_REPRODUCIBLE_AGGREGATION
CATEGORY_BREAKDOWN_STATUS = NOT_AVAILABLE_FOR_REPRODUCIBLE_AGGREGATION
TARGET_FAMILY_BREAKDOWN_STATUS = NOT_AVAILABLE_FOR_REPRODUCIBLE_AGGREGATION
```

No partial subgroup percentages may be presented as benchmark-wide results.
No value may be inferred from a mutation, test name, endpoint, diff, working
tree, LLM answer, or retrospective classification.

A future JSON may omit these fields or use `null` together with an explicit
availability status and reason. A future Markdown report must state why the
corresponding breakdown is unavailable rather than display a partial table.

## Predeclared contrastive-pair set

The former model of a `contrastivePair` attribute for every CASE is replaced by
an explicitly predeclared contrastive-pair set. Its sole normative source is
the pre-evaluation frozen configuration revision:

| Field | Value |
| --- | --- |
| tag | `benchmark-v2-gemini-config-v2` |
| tag type | lightweight |
| commit | `98b568d21330fee1365c3247916011ab5ec0bcf4` |
| chronology | `PRE_EVALUATION` |
| paths | `docs/benchmark/evaluation_protocol.md`; `docs/benchmark/change_control.md` |

Those documents explicitly declare the protected pairs. The set consists only
of pairs recovered from those frozen documents; it is not derived from
evaluation metadata, an LLM result, or a claim that all other CASEs have a
negative pair attribute.

`PREDECLARED_CONTRASTIVE_PAIR_PROVENANCE_VALID` is `PASS` only if the frozen
documents can be located, parsed deterministically, and mapped to selected
normative EXP results. Existing states remain `PAIR_FULLY_CORRECT`,
`PAIR_PARTIALLY_CORRECT`, `PAIR_NONE_CORRECT`, and `PAIR_NOT_APPLICABLE`.

Contrastive results remain descriptive, do not enter the confusion matrix, and
do not imply statistical significance or alter primary accuracy.

## Frozen origins by result scope

`FROZEN_ORIGINS_VALID` must be evaluated against sources necessary for the
result set actually being materialized. For Primary Reproducible Results,
unavailable descriptive-attribute provenance does not invalidate verified
Ground Truth, evaluation selection, LLM classification, matrix, or metrics.
Conversely, any requested descriptive output remains unavailable until its own
frozen provenance is complete.

The three independent statuses are:

```text
PRIMARY_RESULTS_REPRODUCIBLE = PASS | FAIL
DESCRIPTIVE_ATTRIBUTE_PROVENANCE_COMPLETE = YES | NO
PREDECLARED_CONTRASTIVE_PAIR_PROVENANCE_VALID = YES | NO
```

## Reporting implications

The TCC may report primary metrics, the confusion matrix, mismatches,
operational conditions, and—only when its dedicated gate passes—the
predeclared contrastive-pair analysis as reproducible quantitative results.

It must not report breakdowns by difficulty, category, or target family as
reproducible benchmark results while their complete frozen provenance is
unavailable. These attributes must not be recovered retrospectively merely to
enrich discussion.

## Change-control statement

This amendment records an incompatibility between the original consolidation
specification and evidence actually preserved in frozen Git objects. It creates
no experimental evidence and changes no Ground Truth, LLM output,
inclusion/exclusion decision, or scoring rule. Future implementation must
derive availability gates from frozen sources and preserve the provenance
supporting each result.
