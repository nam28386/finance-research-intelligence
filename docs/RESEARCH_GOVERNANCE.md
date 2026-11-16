# Research governance

## Epistemic labels

| Label | Meaning |
| --- | --- |
| FACT | Directly documented source observation with a citation |
| MEASUREMENT | Observed output with method, units, sample, and artifact evidence |
| INFERENCE | Interpretation conditional on cited evidence and assumptions |
| HYPOTHESIS | Untested mechanism with observable implications and falsifiers |
| UNKNOWN | Missing or unresolved knowledge; never an invented value |

Claims use these labels explicitly. FACT, MEASUREMENT, and INFERENCE require
evidence IDs. HYPOTHESIS requires a falsifier. An evidence pointer is an auditable
lead, not automatic verification of its content. Synthetic fixtures are examples.

## Lifecycle and promotion

Normal transitions advance one step. Every history begins `null → DISCOVERED`.
Each event records an offset-aware timestamp, reason, and evidence IDs. The
current state must equal the last event; timestamps cannot move backwards or
postdate `inspected_at` (the latest review of the record).

| Promotion | Minimum machine gate | Human review criteria |
| --- | --- | --- |
| DISCOVERED | Valid metadata, explicit revision unknown/pinned | In-scope question; acquisition not authorized by registration |
| SOURCE_REVIEWED | Pinned SHA, source refs, SOURCE evidence | Inspect exact revision; verify citations, license status, relevance |
| CONTRACT_EXTRACTED | Prior gate + mechanisms, assumptions, limitations | Explicit variables, measurement validity, observables, confounders, falsifiers |
| REPRODUCED | Prior gates + VERIFIED license, PASSED replication, REPRODUCTION evidence | Approved rights/environment; reproducible commands, artifacts, original-vs-rerun comparison |
| ADAPTED | Prior gates + TEST and REVIEW evidence | Document semantic changes, target asset constraints and tests |
| EMPIRICALLY_VALIDATED | Prior gates + EMPIRICAL and REVIEW evidence | Frozen estimand/design, data lineage, information-time audit, leakage-safe splits, uncertainty, robustness and economic limits |

The event making each promotion must cite its required evidence kinds. Metadata
must also satisfy the highest normal stage ever reached, including when blocked
or rejected, so old evidence cannot be silently removed.

Any normal state may move to BLOCKED, REJECTED, or SUPERSEDED with a reason.
BLOCKED may return only to the last normal state and must cite REVIEW evidence;
it may instead become REJECTED or SUPERSEDED. REJECTED and SUPERSEDED are terminal.
A revised inquiry gets a new ID and links, rather than erasing the old outcome.

`decision.status` is DEFER, RETAIN, REJECT, or SUPERSEDE. Terminal decisions must
match terminal lifecycle states. SUPERSEDED records have a `superseded_by` ID;
the replacement lists the old ID in `supersedes`. Links are reciprocal, resolve
inside the catalog, cannot self-link, and cannot form cycles.

Use `--base` in reviews to prevent deletion of prior records, history/evidence
rewrites, or changing an already source-reviewed repository/revision under the same ID.
Existing evidence entries are immutable; append corrections under new evidence IDs.
This comparison requires a trusted base; validating a snapshot alone cannot
detect an author rewriting its entire history. CI compares against the PR base
catalog when it exists. The initial foundation has no prior catalog to compare.

## Separate achievements

Software tests establish behavior of code. Reproduction establishes that a
specified result can be rerun. Empirical validation evaluates a bounded claim
against data and a stated design. Causal identification additionally requires an
identification strategy and defensible assumptions; **no lifecycle state certifies
causality**. Code running, positive P&L, or persuasive LLM text proves none of the
other achievements.

Keep failed tests, negative findings, unknown rights, blocked data, rejected
mechanisms, and superseded results. Never relabel them as success. Human review
must precede promotion, code reuse, consequential contract changes, integration,
or publication. The validator checks metadata; it cannot enforce human identity,
truth, branch protection, or GitHub approval policy.
