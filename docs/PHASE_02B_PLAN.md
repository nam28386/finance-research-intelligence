# Proposed Phase 02B source review — NOT YET AUTHORIZED

The following are research questions and inspection targets, not findings. The
links point to observed root trees at the pinned SHAs. Root directory names were
visible as metadata; no source file or upstream test was inspected or executed.
License labels are provisional and require a review of the pinned license and
the exact component before any code reuse.

## 1. NautilusTrader — event and data architecture

[Pinned root](https://github.com/nautechsystems/nautilus_trader/tree/33492c8135a5e0dceedc21d9ee3ff7432f04ff12):
locate engine, data models, replay/live interfaces and recovery code under
`crates/` and `python/`; locate corresponding tests, fixtures and timestamp
contracts before deciding which individual files to examine.

- Questions: ordering, idempotence, clock/availability semantics, event loss and
  recovery, and whether replay/live parity is explicit or merely advertised.
- Falsifier: a claimed parity or deterministic invariant is unsupported by the
  inspected code/tests, requires an unavailable event field, or breaks on a gap.
- Requirements: read-only pinned source; synthetic sequences for any later
  experiment; CPU, memory and data needs UNKNOWN until code inspection.

## 2. hftbacktest — microstructure simulation

[Pinned root](https://github.com/nkaz001/hftbacktest/tree/5f3ec40b2afb764e0fea112f941ed85523ef4e88):
locate order-book reconstruction and queue/latency assumptions under
`hftbacktest/` and `py-hftbacktest/`; locate tests and fixture provenance.

- Questions: L2 versus L3 inputs, cancellation and fill assumptions, event-time
  semantics, model limits, latency and whether outcomes can be reproduced.
- Falsifier: queue position/fills require unobserved order-level events, hidden
  liquidity, participant identity, or unavailable latency assumptions.
- Requirements: a reviewed, synthetic data contract and bounded resources; no
  paid feed or execution access is authorized by this plan.

## 3. RD-Agent — agentic research control

[Pinned root](https://github.com/microsoft/RD-Agent/tree/484776c211e4fbbeef03e0ec00d6bbee7362a4f4):
locate orchestration/evaluation and evidence boundaries under `rdagent/` and
tests under `test/`; inspect provider, execution, and data dependencies first.

- Questions: reproducibility, untrusted-input boundaries, independent evaluation,
  artifact provenance, human gates, and how failed attempts are retained.
- Falsifier: outputs cannot be traced to versioned inputs, evaluation is circular,
  or external instructions can silently change the research contract.
- Requirements: read-only code review initially; provider credentials, network,
  execution environment and cost remain UNKNOWN and are not authorized here.

## Cross-asset and approval gates

For every pilot, document input data/rights, venue, timestamps and availability,
event ordering, contract mapping, market-state observables, missing fields,
assumptions, confounders, falsifiers, and a synthetic verification design.
COMEX MBO/L3, crypto L2/L3 and VN30 aggregated MBP are not equivalent feeds;
anonymous data do not identify institutional actors. Point-in-time availability
must precede a hypothetical decision. Reproduction requires separate approval of
license obligations, commands, dependencies, isolation, data and resource limits.
Human review is required before source promotion, reuse, empirical work, or any
integration. Do not run this plan as part of Phase 02A.
