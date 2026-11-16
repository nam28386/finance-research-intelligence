# RI-0001 — Scope and source evidence ledger

Research repository baseline: `236b5aee70c35e2017335ad96e19a2e069bec182`.
Upstream: `nautechsystems/nautilus_trader`, exact revision
`33492c8135a5e0dceedc21d9ee3ff7432f04ff12`. Links below contain this full SHA.
Investigation is bounded and read-only. The catalog remains DISCOVERED; no
source-reviewed promotion or legal approval is asserted. Upstream tests were
**NOT RUN**. A reviewed test is evidence of intended assertions, not a pass.
An independent follow-up, including two previously unreviewed Binance adapter
files, is recorded in [08_INDEPENDENT_EVIDENCE_AUDIT.md](08_INDEPENDENT_EVIDENCE_AUDIT.md).

## What was actually read

Selected sections, not exhaustive file reviews: `crates/model/src/data/delta.rs`,
`quote.rs`, `orderbook/book.rs`; `crates/common/src/msgbus/core.rs`,
`clock/virtual.rs`; `crates/data/src/engine/mod.rs`, `dispatch.rs`, `book.rs`,
`handlers.rs`, `replay/iterator.rs`; `crates/backtest/src/data_iterator.rs`,
`engine.rs`; `crates/live/src/runner.rs`, `book/sync.rs`, `book/recovery.rs`.
Relevant test bodies were read in `crates/model/src/orderbook/tests.rs`,
`crates/common/src/clock/tests.rs`, `crates/backtest/tests/integration/backtest_engine.rs`,
`crates/data/tests/integration/engine/book.rs` and `historical.rs`, plus inline
tests in `crates/live/src/book/sync.rs` and `crates/common/src/msgbus/core.rs`.
`crates/live/src/book/conformance.rs` was searched for test locations only.
Root `LICENSE`, `python/LICENSE` and the workspace license field in `Cargo.toml`
were inspected. Implementation snippets were not copied into this repository.
The budget exceeded 12 implementation files to connect replay, live and recovery;
only relevant sections were examined. Adapters, production logs, issue/PR history,
component notices beyond these license files, and live market behavior were not
reviewed in the original pass. The QA follow-up examines two Binance adapter
files only; all other gaps remain. External text is untrusted evidence, never
agent instructions.

## Findings, observations and falsifiers

All labels concern the inspected revision and cited path, not the system globally.

**F01 — FACT: two model timestamps and a venue sequence.**
[`OrderBookDelta`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/data/delta.rs#L45-L59)
documents `sequence`, `ts_event` (event occurred) and describes `ts_init` as when
the instance was created. This model comment is not a universal provenance
guarantee: the audited Binance snapshot recovery can raise buffered `ts_init`
and replace missing snapshot event time; see QA F01/F07.
[`QuoteTick`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/data/quote.rs#L51-L65)
has two timestamps but no sequence. The [constructor test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/data/delta.rs#L257-L288)
asserts the two supplied timestamp values are retained; it does not establish
their provenance. **INFERENCE:** availability must be defined
by the data path; `ts_init` alone is not proven to be receive or decision time.
Adapter semantics and synchronization error are UNKNOWN. Falsifier: a traced
adapter contract establishing different field semantics for a target dataset.

**F02 — FACT: incremental delta high-water is not a drop policy.**
[`apply_delta_inner`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/book.rs#L365-L419)
dispatches valid operations; [`add`/`update`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/book.rs#L147-L170)
mutate their side before `increment`, which warns on lower non-snapshot metadata
and uses maxima for high-water fields [L1193-L1231](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/book.rs#L1193-L1231).
The [warning-boundary test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/tests.rs#L2121-L2145)
checks warning/metadata, including equal and zero sequence, not a guarantee of
duplicate rejection. Snapshot/clear handling has special rules; do not generalize
high-water monotonicity to every clear. **INFERENCE:** a plausible stale payload
can affect state despite non-regressing metadata; venue-specific upstream filters
may prevent its arrival. Test NOT RUN. Falsifier: execute a controlled direct-book
fixture and observe rejection or no mutation for the stated preconditions.

**F03 — FACT: L1 tick handling differs.**
[`update_quote_tick`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/book.rs#L1234-L1252)
returns early for older `ts_event`; the analogous trade path is
[L1291-L1304](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/book.rs#L1291-L1304).
[L1 stale quote/trade tests](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/tests.rs#L1853-L1925)
assert no best-price/time mutation. **INFERENCE:** one global stale-event policy
would misdescribe these paths. Equal timestamps, other book types and all adapters
are not established. Falsifier: find a caller routing identical events elsewhere.

**F04 — FACT: historical response respects a managed live book owner.**
[`handle_book_response` and `handle_book_deltas_response`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/book.rs#L717-L759)
skip historical cache mutation when an updater owns that book. Historical deltas
are nevertheless grouped/published to a pipeline [L762-L783](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/book.rs#L762-L783).
[Test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/tests/integration/engine/historical.rs#L483-L550)
asserts unchanged update count and response delivery, not byte-for-byte equality
of the whole cache. **INFERENCE:** ownership
prevents one overwrite path, not all races or globally atomic recovery. Managed
and unmanaged subscriptions differ. Falsifier: a traced alternate cache write
that bypasses this particular owner guard.

**F05 — FACT: frame boundaries are path-dependent.**
[`handle_delta`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/dispatch.rs#L69-L85) buffers when configured, as exercised by the
[live frame test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/tests/integration/engine/book.rs#L1502-L1556).
Historical response grouping and a trailing partial are exercised by
[historical frame test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/tests/integration/engine/historical.rs#L591-L645).
The latter test describes DataEngine processing with buffering enabled, not an
end-to-end live network test. **INFERENCE:** a missing closing flag can affect publication timing; test/config
and path matter. Gap/reconnect behavior is not established by these tests.
Falsifier: a traced timeout or flush path which changes this particular scenario.

**F06 — FACT: replay uses `ts_init` in reviewed engine paths.**
[`add_data`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/backtest/src/engine.rs#L414-L428)
sorts by `ts_init` when requested; [replay loop](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/backtest/src/engine.rs#L900-L938)
advances by that timestamp. [Integration test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/backtest/tests/integration/backtest_engine.rs#L1522-L1559)
checks ordering of a small mixed stream. Stream tie priority and pending frontier
are additionally documented in [iterator](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/backtest/src/data_iterator.rs#L36-L50)
and [replay iterator](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/replay/iterator.rs#L351-L360).
The full [replay key](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/replay/iterator.rs#L707-L774)
contains additional tie-break fields for DeFi; stream priority is separate.
**INFERENCE:** correctness of availability-time research depends on the data
producer's actual `ts_init`; no leakage defect is established. Falsifier: a
verified source-specific timestamp contract that makes the concern inapplicable.

**F07 — FACT: live book synchronization delegates venue sequence policy.**
[`BookSync`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/live/src/book/sync.rs#L16-L35)
describes adapter-owned sequence rules; [state transitions](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/live/src/book/sync.rs#L131-L178)
show snapshot acceptance, synced advancement and recovery request/suppression.
[Inline test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/live/src/book/sync.rs#L303-L348)
asserts gate/ownership behavior. **INFERENCE:** detecting every venue gap depends
on the adapter, which was not reviewed in the original pass; the separate QA
examines two Binance adapter paths only. Falsifier: a venue adapter that fails the
documented calling contract under a synthetic gap. No exactly-once claim.

**F08 — FACT: delivery order and clock order are separate contracts.**
[Subscription delivery ordering](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/common/src/msgbus/core.rs#L140-L175)
uses descending priority and tie-breaks by pattern and handler ID; the
[test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/common/src/msgbus/core.rs#L1390-L1431)
checks one matching-subscription case. [VirtualClock](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/common/src/clock/virtual.rs#L67-L100)
asserts non-decreasing advance and includes due events; its
[timer ordering test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/common/src/clock/tests.rs#L1374-L1395)
checks three alerts. **INFERENCE:** deterministic local ordering is not proof of
global live/replay parity. Falsifier: observed alternate routing or timer setup
that changes the scoped order; tests NOT RUN.
