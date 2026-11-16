# Independent evidence audit — RI-0001

**Verdict: NEEDS_TARGETED_SOURCE_REVIEW.** This is an adversarial second pass in
the same AI-assisted task history; it is not an independent human review or an
independently replicated execution. Baseline review commit:
`9793fcf4b97e99619ada6370e3504c856dc21893`. All upstream links refer to
`33492c8135a5e0dceedc21d9ee3ff7432f04ff12`. Catalog status remains DISCOVERED.

## A. Evidence coverage and methodology

Re-fetched the 22 file paths cited by the earlier packet at the pinned SHA and
read each cited code/test span in context; checked control flow rather than using
HTTP success as support. Additional core paths were `orderbook/aggregation.rs`,
`ladder.rs`, `level.rs`, `mod.rs`, and `data/order.rs`. Exactly two additional
adapter paths were read: Binance futures `streams/parse_data.rs` and Binance
`book/sync.rs`, including selected inline tests. No upstream source was executed,
installed or copied. Source comments are statements in code, not proof of
maintainer intent. All upstream tests below are **located and source reviewed;
EXECUTED: NO; PASSED: UNKNOWN**. Full link inventory is in the
[original evidence ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md).

## B. F01–F08 verdicts

Severity assesses risk of misunderstanding the research contract, not a claim
that upstream code is defective. Alternatives and missing paths remain open.

| ID | Earlier claim → independently observed behavior and test | Assumptions, alternatives, missing paths | Verdict / severity |
| --- | --- | --- | --- |
| F01 | Model comments describe event time, instance-creation time and delta sequence; [constructor test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/data/delta.rs#L257-L288) checks values retained. [Binance recovery](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L235-L252) can raise `ts_init` and fill a missing snapshot event time. | Field descriptions are not immutable end-to-end provenance. Adapter caller clock, actual receipt and availability are UNKNOWN. | **REVISE / MAJOR** |
| F02 | Valid incremental add/update is dispatched before high-water increment; [boundary test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/tests.rs#L2121-L2145) asserts warning cases and maxima, not best bid or exchange truth. | Instrument, side, positive size, L2 ID mapping and flags matter; valid caller-side filtering may prevent arrival. Full clear can reset sequence. | **QUALIFY / MAJOR** |
| F03 | L1 quote/trade paths return before updates for strictly older `ts_event`; [tests](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/tests.rs#L1853-L1925) assert best bid/ask and `ts_last` for two cases. | Tests do not compare every field, equal times, other book types, all callers or real venues. | **QUALIFY / MINOR** |
| F04 | A managed `BookUpdater` makes the historical handler skip its cache write; the [test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/tests/integration/engine/historical.rs#L483-L550) checks update count and requester receipt. | Test does not assert a full-book equality or concurrency safety; unmanaged subscription follows another branch. | **QUALIFY / MINOR** |
| F05 | [Dispatch](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/dispatch.rs#L69-L85) waits for `F_LAST` when configured. [Historical response](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/book.rs#L762-L783) publishes a trailing partial. The two cited unit/integration test bodies check those scoped cases. | A DataEngine test is not a live exchange/network test; historical partial publication is not parity with a still-open buffered frame. No timeout/reconnect guarantee follows. | **QUALIFY / MAJOR** |
| F06 | Backtest `add_data(sort=true)` sorts by `ts_init` and the loop advances by it; [mixed-stream test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/backtest/tests/integration/backtest_engine.rs#L1522-L1559) checks four distinct times. [ReplayKey](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/replay/iterator.rs#L707-L774) uses `ts_init` plus DeFi position fields; heap stream priority/index resolve remaining ties. | Do not assert that all replay ordering is solely `ts_init`. Equal times, producer provenance, pending frontier and market-level parity need independent tests. | **QUALIFY / MAJOR** |
| F07 | `BookSync` tracks snapshot/gap/recovery ownership; [inline tests](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/live/src/book/sync.rs#L303-L348) check scoped transitions. [Binance depth sequencing](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L329-L368) implements spot/futures-specific suppression and recovery. | The Binance implementation is one adapter, not every venue. Snapshot success, callback scheduling, retries and completeness under real disconnects remain unproven. | **QUALIFY / MAJOR** |
| F08 | Subscription comparator uses priority, pattern and handler ID; [test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/common/src/msgbus/core.rs#L1390-L1431) checks one cache-miss matching case. VirtualClock checks nondecreasing advance; a test checks three timer timestamps. | Comparator/timer order does not prove all typed routing, nested reentrancy, equal-time scheduling, parallel delivery, or live/replay equivalence. | **QUALIFY / MINOR** |

No finding is rejected outright; this is not evidence that the system or its
market results are correct. A scoped FACT about code is separate from a
TEST-ASSERTED invariant, an ENGINEERING INFERENCE, a HYPOTHESIS, and UNKNOWN.

## C. Critical and major issues

No confirmed BLOCKING source-access error or verified upstream defect was found.
Four **MAJOR** interpretation risks remain: (1) `ts_init` and occasionally
`ts_event` may be transformed by a particular adapter, (2) high-water metadata
is not evidence that state is exchange-correct, (3) the historical trailing
partial and live buffering paths differ, and (4) replay/tie and adapter recovery
semantics are scoped and unexecuted. F01/F02/F05/F06/F07 in the table map to
these four risk themes. These are research-admissibility concerns, not incident
severity claims about running production systems.

## D. Corrected claims

1. The model documents `ts_init` as instance creation, but the inspected Binance
   recovery path can [raise buffered diff `ts_init`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L238-L252)
   to the snapshot's value; it can also assign snapshot event time from the
   first replayed diff when absent. The [test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L635-L674)
   checks a scoped ordering example. The original packet now qualifies the label.
2. The late-add path is a direct local `OrderBook` path. It does not establish
   that a venue-specific upstream adapter lets the same late update through.
3. `ReplayKey` ordering is not only timestamp in all configurations: DeFi fields
   and stream priority can resolve ties. No end-to-end parity follows.

## E. Timestamp and availability

For the two reviewed model structs, `ts_event` and `ts_init` are fields;
`sequence` is an ordering identifier, not an exchange timestamp. The reviewed
[Binance futures depth parser](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/websocket/streams/parse_data.rs#L204-L234)
receives `ts_init` as a parameter and passes transaction time plus that value to
`parse_millis_or_init`. An inline [aggregate-trade test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/websocket/streams/parse_data.rs#L651-L663)
asserts a fallback for invalid trade timestamps; it does not prove every depth
timestamp path. The parser's caller and actual capture clock were not traced.
At the time of this QA, receive time, first availability, processing and
decision time remained UNKNOWN. A later [targeted follow-up](09_TARGETED_SOURCE_REVIEW.md)
traces the selected Binance callback clock; it does not establish wire receive or
first observable availability. This QA verdict is retained as historical context.
`availability_time(feature) <= decision_time` is a proposed information-integrity
constraint, not an established upstream guarantee or a discovered leakage bug.

## F. Late-delta experiment contract review

Path independently traced: `OrderBookDelta::new_checked` checks positive size
for Add/Update; `apply_delta` checks matching instrument; `apply_delta_unchecked`
skips that check only; `apply_delta_inner` resolves side and dispatches;
`OrderBook::add` preprocesses and mutates the bid ladder before `increment`
warns and updates maxima. See [constructor](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/data/delta.rs#L62-L93),
[book](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/book.rs#L329-L419),
and [add/increment](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/book.rs#L147-L154).
The L2 preprocessor maps identity from a price hash
([source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/aggregation.rs#L45-L80));
the [ladder](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/orderbook/ladder.rs#L244-L292)
handles an ID already mapped at another price. Price/quantity precision, positive
size, identical instrument, buy side, `Add`, L2, flags 0, order ID 0 and direct
call are now explicit in the revised [proposal](06_FALSIFIABLE_EXPERIMENT_PROPOSAL.md).
Distinct price-derived IDs are an assumption if asserting both levels survive;
no collision-free guarantee is inferred from a finite hash.

For A=(98, size 10, seq 5, event/init 2000/2000) followed by B=(99, size 10,
seq 3, event/init 1000/3000), the expected maxima (5, 2000), changed best bid
and warnings are **predictions**, not test results. Controlled WARN capture is
required. Three claims remain separate: (1) metadata maxima in this non-clear
path are source-supported; (2) best-bid mutation under these precise inputs is a
testable inference; (3) correctness of exchange-time state is UNKNOWN. The
upstream warning test checks metadata/warnings, not proposed best bid. Duplicate,
zero sequence, snapshot, clear and adapter-filtered paths need distinct fixtures.

## G. Adapter and recovery gaps

The scoped Binance tracker validates spot/futures update IDs; its
[inline cases](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L527-L580)
assert suppression, bridging and recovery outcomes. It buffers unsynced updates,
and [buffer overflow removes the oldest](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L372-L378)
at the 10,000-entry cap. Its [test](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L919-L932)
checks retention of newer updates, not end-to-end market correctness after
overflow. Exact data loss outcomes depend on subsequent snapshot/bridge paths.
No claim is made for COMEX, other venues, precisely-once behavior or guaranteed
recovery. PRs/issues and maintainer motives were not inspected.

## H. Cross-asset overclaim audit

| Context | Candidate input / clock requirements | Missing information and falsifier |
| --- | --- | --- |
| COMEX Gold MBO | Order IDs, action, side/price/size, sequence, event/receive and availability clocks; venue session/reset and snapshot rules | Hidden liquidity and gaps remain; reject reconstruction assumptions if a gap/snapshot fixture cannot restore observed state |
| Crypto L2/L3 | Venue-specific snapshot/delta IDs, price/size or order IDs, capture/availability clocks and reconnect policy | The Binance example is not universal; falsify with a venue's gap, duplicate and bridge rules |
| VN30 MBP | Vendor-provided price levels, sizes, timestamps, any available sequence, session and delivery semantics | Availability/sequence may be absent; MBP cannot uniquely reconstruct order queues or participant identity. A queue-identity requirement is a falsifier |
| Asset-agnostic | Explicit instrument/event identifiers, revision lineage, event/receive/availability/decision clocks and missing-data rules | Clocks may be unavailable or revised; test late arrival/revisions and reject any feature using unavailable information |

All proposed transfers remain HYPOTHESIS/UNKNOWN, not EMPIRICALLY_SUPPORTED.
No actor identity, performance, alpha or causal conclusion is supported.

## I. License and security

Pinned root and Python LICENSE files contain LGPL v3 text; pinned workspace
`Cargo.toml` declares `LGPL-3.0-only`. This does not prove coverage of all
components or settle redistribution, linking, dependencies, notices or data
rights. Legal/human review is required before reuse. No external code was run or
copied; no paid/private data, credentials or order endpoints were used.

## J. Three lessons and human review

1. **Metadata versus state:** metadata high-water and mutable book state have
   different invariants. A naive system checking only monotonic sequence can
   miss a state change; independently test both after a stale valid update (F02).
2. **Availability versus labels:** creation/initialization labels can change
   during snapshot recovery. A naive join can use a misleading clock; retain raw
   provenance and test event, receive, normalized and decision-time semantics
   separately (F01/F06/F07). This is an inference, not proof of leakage.
3. **Ownership and frame boundaries:** historical response delivery, cache
   mutation and stream completion are distinct. A naive replay may clobber live
   state or treat a partial frame as complete; test managed/unmanaged ownership,
   partial tails and reconnects with controlled fixtures (F04/F05).

Human reviewers should check cited code, adapter boundaries, clock provenance,
the revised fixture, unreviewed venues and license rights before authorizing any
source-review promotion or experiment. A future approved task must explicitly
design a tested discovery-gate migration and append evidence/history; this task
does not alter either. No maintainer intent has been established.

## K. Promotion readiness

**NEEDS_TARGETED_SOURCE_REVIEW.** F01/F02/F05/F06/F07 need the focused evidence
above plus human review; the full range of adapters, producer clocks, recovery
under real conditions, component licenses and execution behavior remains open.
This verdict is not SOURCE_REVIEWED and does not authorize an experiment.
