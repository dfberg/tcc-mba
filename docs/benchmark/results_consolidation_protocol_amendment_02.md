# Benchmark V2 — Results Consolidation Protocol Amendment 02

## Status, authority, and scope

**Amendment type:** `POST_EXPERIMENT_PRIMARY_MAPPING_PROVENANCE_SCOPE_AMENDMENT`.
This is also a `PROVENANCE_SCOPE_CORRECTION` created after the experiment in
response to a provenance gap found during results reconstruction.

This amendment complements the original Results Consolidation and Scoring
Protocol frozen at `benchmark-v2-results-consolidation-protocol`
(`6a2c37446ca9de22b4538f62f0540408b47a708a`; blob
`5380a1bb25a1b6d00e4e1f4d484b22c74a7935ee`) and Amendment 01. It changes
only the source and scope of provenance for the EXP-to-CASE mapping. It does
not replace either authority in any other respect.

## Correction of the catalog assumption

The original protocol stated that the frozen catalog deterministically defined
`EXP-NNN -> CASE-NNN`. Forensic review established that
`benchmark-v2-catalog` preserves planned `CASE-*` records and reserves `EXP-*`
for later executions, but does not explicitly materialize that mapping. The
catalog must not be used as a fictional source of an EXP-to-CASE relation.

The correction does not create a mapping. For mappings that were already
preserved, the normative source is the per-EXP `metadata.json` in the frozen
technical freeze that precedes the corresponding LLM inference. Its evidence
must include the source tag, dereferenced commit, metadata path, metadata blob
SHA-256, `experimentId`, `caseId`, and pre-inference chronology.

Source preference is, in order:

1. an explicit technical freeze before the relevant LLM inference;
2. another explicitly pre-inference frozen source preserving the same mapping;
3. no retrospective inference.

Multiple contemporaneous sources that identify different CASEs for one EXP are
a fail-closed conflict. Working-tree metadata and evaluation metadata created
after an available technical freeze are not mapping authorities.

## Prohibition of retrospective mapping

Identifier suffixes, mutation content, test names, Ground Truth, LLM output,
confidence, reason, ordinal position, and present-day researcher knowledge are
not evidence of an EXP-to-CASE relation. In particular, `EXP-016 -> CASE-016`
must not be inferred merely from matching numbers.

The recorded forensic evidence establishes explicit, LLM-independent,
pre-inference mapping metadata for every included EXP and for EXP-011. It does
not establish sufficiently frozen CASE mapping provenance for EXP-016. No
relationship is created, repaired, or imputed for EXP-016 by this amendment.

## Primary and full-catalog gates

`PRIMARY_EXP_CASE_MAPPING_PROVENANCE_VALID` is PASS only when every EXP with
`includedInPrimaryAnalysis = true` has one explicit, frozen, pre-inference,
LLM-independent EXP-to-CASE mapping; the mappings are conflict-free and none
is retrospectively inferred. A missing or conflicting mapping for any included
EXP fails the primary analysis dataset integrity and, consequently,
`PRIMARY_RESULTS_REPRODUCIBLE`.

`FULL_CATALOG_CASE_MAPPING_PROVENANCE_COMPLETE` is separate. It is YES only
when all 30 EXPs have such provenance. Its failure does not invalidate primary
metrics when the primary mapping gate passes; it limits full-catalog CASE
traceability. `PRIMARY_RESULTS_REPRODUCIBLE` depends on
`PRIMARY_EXP_CASE_MAPPING_PROVENANCE_VALID`, not on full-catalog completeness.

## EXP-011 and EXP-016

EXP-011 retains its recorded CASE mapping and its existing
`PROTOCOL_NONCONFORMITY` exclusion. This amendment changes neither fact.

EXP-016 remains `REQUIRES_REVIEW` and
`includedInPrimaryAnalysis = false` under its existing independent normative
status. When no sufficient frozen mapping is available, its CASE is represented
as unavailable (for example, `caseId = null` with a mapping-unavailable
status); it receives no MATCH, MISMATCH, confusion-matrix cell, Ground Truth
imputation, or new exclusion rationale.

## Non-amendment of evidence and results

This amendment changes no Ground Truth, selected evaluation, rerun treatment,
first-valid policy, model/configuration requirement, prompt provenance,
LLM-output provenance, confidence handling, scoring class, MATCH/MISMATCH,
confusion matrix, or metric formula. Amendment 01 remains unchanged, including
its descriptive-attribute availability rules and predeclared contrastive-pair
model.

The primary set continues to require 28 included normative evaluations, valid
Ground Truth and predictions, a valid mapping for each included EXP, and every
other mandatory provenance gate. No primary numerical result changes merely
because this provenance-source correction is recorded.

## Reporting and post-experiment limitation

This amendment is post-experiment. It is defensible only because the included
mappings were already frozen independently of LLM results, have no observed
conflicts, and EXP-016 was already outside primary analysis for an independent
normative reason. It does not assert complete 30-EXP CASE traceability.

Future JSON must distinguish primary mapping validity from full-catalog mapping
completeness and preserve per-EXP mapping provenance. Future Markdown and the
TCC methodology/validity discussion must state that mapping provenance is
complete for included primary EXPs, while EXP-016's CASE association could not
be recovered from frozen evidence and was not inferred retrospectively.
