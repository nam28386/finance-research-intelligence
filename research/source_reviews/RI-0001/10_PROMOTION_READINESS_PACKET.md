# RI-0001 — Scoped human source-review decision packet

## Proposed decision

**READY_FOR_HUMAN_SOURCE_REVIEW of the bounded evidence packet** — a request
for a human decision, not an approval, lifecycle state change or claim that
every uncertainty is closed. The prior independent QA verdict
`NEEDS_TARGETED_SOURCE_REVIEW` is preserved as the result at that time; the
[targeted follow-up](09_TARGETED_SOURCE_REVIEW.md) supplies additional evidence
for a narrower set of Binance futures and DataEngine paths. A reviewer may still
reject this recommendation or require more evidence. RI-0001 remains DISCOVERED.

## Accepted scope for the reviewer

- Upstream commit `33492c8135a5e0dceedc21d9ee3ff7432f04ff12`; selected code
  paths and tests only, including two Binance adapter files from QA and twelve
  additional targeted paths listed in the follow-up. No upstream execution.
- **Supported scoped code facts:** model timestamp fields; direct-book stale
  metadata versus state boundary; L1 stale tick behavior; managed cache guard;
  selected `F_LAST` publication paths; replay timestamp and tie-key structure;
  Binance Futures handler clock placement; selected Binance spot/futures ID
  rules; recovery owner, snapshot bridge, capped buffer and explicit reset.
  Consult the [original ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md),
  [adversarial QA](08_INDEPENDENT_EVIDENCE_AUDIT.md) and
  [targeted evidence/decision matrix](09_TARGETED_SOURCE_REVIEW.md) for exact
  sources, counterexamples, tests and conditions.
- **Requires qualification:** `ts_init` is not universally receive or first
  availability time; sequence high-water does not certify book state; historical
  partial publication does not certify replay/live parity; adapter acceptance
  and recovered exchange correctness are different claims.

## Unknowns and boundaries

The following may remain unknown without invalidating the narrow static-code
observations: exact packet arrival, unknown callback schedules, unreviewed
adapters and exchange implementations, uninspected issues/maintainer motives,
full transitive license notices, and whether tests pass at runtime. They must be
visible to reviewers and must not be replaced by assumptions.

The same unknowns **block stronger claims** about first information availability,
complete sequence/gap detection, exactly-once delivery, verified recovery,
market-state equivalence, execution fidelity, software performance, economic
value, causality or cross-asset transfer. MBP cannot uniquely identify individual
queue orders; anonymous data do not identify institutions. No market finding is
validated by this review.

## Future experiments — proposals, NOT RUN

Separate authorization must specify rights, isolated environment, pinned code,
dependencies, input hashes, clock lineage, versions, resource caps and artifacts.

1. **Late delta / direct book:** run the bounded two-event fixture in
   [06](06_FALSIFIABLE_EXPERIMENT_PROPOSAL.md); check book state, high-water and
   warnings independently. Include a separate adapter-filtered control; no
   exchange correctness claim follows from either result.
2. **Time and framing:** inject known local/raw/event times, invalid venue time,
   buffered `F_LAST` tail, explicit reset and separately simulated reconnect.
   Record whether and when each path publishes or clears the partial frame.
3. **Recovery overflow:** exceed the 10,000-update cap with synthetic sequence
   IDs, provide bridging/non-bridging snapshots, compare emitted and downstream
   full state against an independent reference, and retain failed attempts.

The upstream test assertions discussed in the source packet are **SOURCE
REVIEWED / NOT RUN**, not proof that any of the above experiments passed.

## IP and governance decision

Root/Python LGPL v3 text and workspace `LGPL-3.0-only` metadata were observed;
the Binance crate inherits workspace metadata. Scope, dependencies, linking,
redistribution and data rights require a human/legal decision for the actual
future use. Reading an idea does not approve copying or linking implementation.

A human should decide whether the **scoped** source observations are sufficient,
which missing evidence is required, and whether to authorize a later controlled
promotion proposal. That separate task would need to append evidence/history and
design a tested migration for the Phase 02A-only discovery gate. It must not
rewrite existing research history or infer empirical validity. This packet does
not modify catalog, schema, validators or governance, and does not promote
RI-0001 or authorize experiments.
