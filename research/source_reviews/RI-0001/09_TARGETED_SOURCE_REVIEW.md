# RI-0001 — Targeted source evidence closure

Baseline branch commit `23794e49a783c9ab64c87b45709b9c5fc317f800`; upstream
`nautechsystems/nautilus_trader` at
`33492c8135a5e0dceedc21d9ee3ff7432f04ff12`. This is bounded source inspection,
not execution or promotion. Labels below describe code at that revision and
the stated path only. Upstream tests: **NOT RUN**. Catalog stays DISCOVERED.

## Scope and actual files inspected

Twelve additional paths were fetched at the pinned SHA; selected relevant
sections, not every line, were read: Binance futures WebSocket `streams/handler.rs`,
`client.rs`, `dispatch.rs`, `messages.rs`, `common/parse.rs`, `futures/data.rs`,
`book/recovery.rs`, `book/pacing.rs`, `crates/adapters/binance/Cargo.toml`,
`crates/data/src/engine/config.rs`, `crates/model/src/enums.rs`, and
`crates/core/src/time.rs`. Previously reviewed `parse_data.rs`, Binance
`book/sync.rs`, shared `BookSync`/`BookRecovery`, DataEngine `dispatch.rs`,
`book.rs`, `mod.rs` and their selected tests were revisited. External content
was treated as untrusted data. The streams `dispatch.rs` was searched for
call sites only and `messages.rs` was inspected only for its license header;
neither is represented as a complete implementation review. No source code was
run or copied here.

## A. Timestamp lineage — selected Binance Futures path

| Stage / epistemic status | Observed data and source | Scope and unresolved question |
| --- | --- | --- |
| SOURCE EVENT TIME — FACT | Futures depth parser passes the venue message `transaction_time` through [`parse_millis_or_init`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/websocket/streams/parse_data.rs#L204-L234). The [helper](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/common/parse.rs#L77-L113) uses `ts_init` on a failed conversion. | The venue's actual clock accuracy, meaning and synchronization remain UNKNOWN; fallback is not an exchange timestamp. |
| LOCAL ASSIGNMENT — FACT | Raw frame bytes are forwarded through a [channel](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/websocket/streams/client.rs#L680-L697), deserialized to a depth message by the [handler](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/websocket/streams/handler.rs#L334-L364), forwarded to the [output channel](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/websocket/streams/client.rs#L730-L764), and yielded through the [stream](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/websocket/streams/client.rs#L555-L567). The [client loop](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/data.rs#L1294-L1320) calls `handle_ws_message`, which [reads the clock](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/data.rs#L678-L700) before depth parsing and book buffering. | This establishes the first `ts_init` assignment **observed in this normalized-message path**, after queues/deserialization, not packet arrival or the first timestamp anywhere in the transport. |
| CLOCK — FACT | Futures client selects [`get_atomic_clock_realtime`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/data.rs#L180-L194). In realtime mode [`AtomicTime`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/core/src/time.rs#L185-L203) uses a [system-derived monotonic CAS](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/core/src/time.rs#L305-L338). | Clock synchronization/error, runtime mode and packet timestamp are unmeasured. Simulation configuration and clock mode can matter. Monotonic assignment is not network-arrival order across all channels. |
| INSTANCE CREATION — FACT | The delta model documents `ts_init` as creation time; the caller supplies the observed value to the parser. | This does not guarantee an immutable timestamp of the earliest original object or raw frame. |
| SNAPSHOT/RECOVERY TRANSFORM — FACT | [REST snapshot](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/data.rs#L1016-L1043) obtains `ts_init` after `depth_paced` returns. [Recovery](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L235-L252) may raise buffered diff `ts_init` and may fill a missing snapshot event time from a diff. | The futures [snapshot parser](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/data.rs#L1063-L1077) falls back to local `ts_init` on missing/invalid transaction time, yet the returned `DepthSnapshot` sets `has_event_time: true`. That flag alone is not proof of venue time. |
| MESSAGE EMISSION ORDER — FACT / INFERENCE | The recovery source emits snapshot before accepted buffered diffs and raises their `ts_init` floor to snapshot `ts_init`; [test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L635-L674) asserts a sample. | Emission sequence in this path is not a universal strict-timestamp or historical availability guarantee; equal timestamps and other producers remain possible. |
| FIRST OBSERVABLE AVAILABILITY — UNKNOWN | No source reviewed identifies when the information first became usable by a particular strategy/researcher. | Queueing, transport, clock offsets, retransmission and feature transformations require independent measurement. `availability_time(feature) <= decision_time` is a proposed research contract. |

## B. Admission boundaries — selected Binance Futures depth stream

**FACT:** [`handle_ws_message`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/data.rs#L731-L803)
requires a cached instrument and depth subscription, drops frames during a
pending unsubscribe drain, uses a separate partial-snapshot branch, returns on
depth parse error, and sends normal depth updates with first/final/previous IDs
to `BookSyncTracker`. A diff with no levels carries no deltas but still enters
sequence processing. These are code paths, not observed network behavior.

**FACT:** The [tracker](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L129-L175)
buffers when unsynced; when synced it sends accepted updates, suppresses
suppressed ones, and clears/rebuffers and claims recovery on a reported gap.
[Spot/Futures policy](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L329-L368)
differs: spot suppresses final ID `<= last` and detects `first > last+1`;
futures initially bridges the snapshot and, once linked, requires `prev_final`
to equal the last accepted ID. The [test cases](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L527-L580)
assert selected outcomes but were NOT RUN. For linked futures, do not claim
every duplicate is suppressed: the branch primarily checks the previous ID.

**INFERENCE:** these adapter rules can prevent some bad sequence events from
reaching this normal downstream path. They do not prove all invalid timestamps,
duplicates or malformed state are filtered. Direct `OrderBook::apply_delta`
can be called independently; the proposed direct-book late-delta fixture is
not a test of Binance admission. Partial snapshots take a separate path. Other
callers, venue feeds and COMEX policy remain UNKNOWN. A future fixture must
assert emitted data *and* full resulting state across each boundary.

## C. `F_LAST` and frame lifecycle

[`RecordFlag::F_LAST`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/model/src/enums.rs#L2050-L2058)
is the last message in a book event or packet for an instrument. Its numerical
bit is 128; this says nothing about correctness of a venue adapter's flagging.

| State | Scoped behavior and evidence | Limit / next check |
| --- | --- | --- |
| FRAME BUFFERED | With `buffer_deltas=true`, [DataEngine](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/dispatch.rs#L69-L85) accumulates a delta and returns before publication when no `F_LAST`. | No elapsed-time flush was established in this inspected handler; absence elsewhere is UNKNOWN. |
| FRAME COMPLETED | The same handler removes and publishes the buffer on `F_LAST`; [test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/tests/integration/engine/book.rs#L1502-L1556) checks a sequence. With buffering disabled, the handler publishes each delta as a single batch. | Test is not a network or exchange test. Frame correctness depends on upstream flags and configuration. |
| TRAILING PARTIAL PUBLISHED | [Historical response path](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/book.rs#L762-L783) publishes a remaining partial frame after processing the response; [test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/tests/integration/engine/historical.rs#L591-L645) checks `[2,2,1]`. | Publication does not mean the partial is complete; this differs from the open buffered path. |
| FRAME DROPPED OR RESET | Explicit [`DataEngine::reset`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/mod.rs#L528-L557) calls [`clear_book_state`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/book.rs#L402-L418), which clears the delta buffer and frame scratch storage. | This is a reset path, not proof that every disconnect triggers a DataEngine reset or that a partial is flushed before clearing. |
| RECONNECT / TIMEOUT — UNKNOWN | Binance futures reconnect calls [`book_sync.reset_on_reconnect`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/data.rs#L965-L975). | Whether that event clears/flushed an incomplete DataEngine frame was not established. No universal timeout guarantee was located in bounded scope. |

Falsifier/future verification: inject an unterminated frame, explicit reset and
separate reconnect; observe buffer and publication via a deterministic harness.
This proposal has not been executed. No global replay/live equivalence follows.

## D. Recovery milestones and overflow

1. **RECOVERY REQUESTED:** tracker returns a claimed episode when a gap or
   unsynced input requires it; the futures caller attempts `spawn_recovery`
   ([caller](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/futures/data.rs#L775-L803)).
2. **RECOVERY RUNNING:** [`spawn_recovery`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/recovery.rs#L35-L101)
   reserves snapshot weight, runs shared recovery, and performs a paced fetch;
   failed task spawning and cancellation remain distinct outcomes. Shared
   [`BookRecovery::run`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/live/src/book/recovery.rs#L145-L228)
   has an initial retry budget and a slower ceiling loop. The pacing reservation
   wait precedes starting that runner; timeout behavior is config-dependent.
3. **BUFFER BRIDGED / SNAPSHOT ACCEPTED:** [`accept_snapshot`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L185-L252)
   checks current ownership and validates buffered diffs before it accepts and
   emits snapshot followed by selected diffs. A bridge failure is retryable.
4. **BOOK STATE VERIFIED:** **UNKNOWN**. Acceptance and emitted messages are not
   independent proof the downstream book matches the exchange or a reference.

The [10,000-update cap](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L49-L51)
and [oldest eviction](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L372-L378)
are source-supported. [Overflow test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/sync.rs#L919-L932)
checks buffer retention; [retry test source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/src/book/recovery.rs#L220-L252)
checks a two-fetch bridge case, not an overflow-to-state correctness invariant.
Both tests are NOT RUN. A future synthetic test must exceed the cap, retain an
independent authoritative event stream, exercise both bridge/retry outcomes,
reconstruct downstream state including quantity and sequence, compare it to an
independent reference, and preserve cancellation/reconnect/failure artifacts.

## E. License and IP — limited component scope

The previously inspected root and `python/LICENSE` contain LGPL v3 text; root
[Cargo workspace metadata](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/Cargo.toml#L50-L58)
declares `LGPL-3.0-only`. The reviewed [Binance crate](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/adapters/binance/Cargo.toml#L1-L8)
inherits the workspace license and reviewed source headers identify LGPL v3.
No differing notice was observed in these selected declarations/headers; this
does not establish absence of exceptions in unreviewed components, vendored
dependencies or build features. Reading ideas differs from copying, linking,
redistributing or running code; legal/human review must determine the obligations
for any proposed activity. This is not legal advice or permission to reuse.

## F. Evidence decision matrix

| Question | Earlier claim → new evidence | Supported / excluded scope | Remaining UNKNOWN | Verdict | Next test or decision |
| --- | --- | --- | --- | --- | --- |
| A: timestamp | `ts_init` origin unknown → selected callback clock and recovery transform traced (§A) | Selected Binance futures normalized messages only; no universal receive/availability label | Wire arrival, queue delay, clock sync and decision availability | REQUIRE_QUALIFICATION | Synthetic delay/fallback/snapshot lineage plus independent clock provenance |
| B: admission | Direct book can apply stale delta → selected adapter validates venue IDs (§B) | Traced futures diff and spot/futures sequencing; partial snapshot is separate | Other callers, malformed venue state, every duplicate and other exchanges | REQUIRE_QUALIFICATION | Feed direct-book and adapter-controlled cases separately |
| C: frames | Historical tail may publish while buffered path waits → `F_LAST` and explicit reset traced (§C) | Selected DataEngine handlers; not all network and recovery paths | Reconnect-to-DataEngine buffer linkage, timeout behavior outside scope | REQUIRE_QUALIFICATION | Unterminated frame, explicit reset and reconnect fixture |
| D: recovery | Overflow evicts oldest; snapshot may bridge → paced retry and ownership sequence traced (§D) | Selected Binance tracker and shared recovery; no exchange correctness | State after overflow, callback liveness, cancellation and real disconnect effects | REQUIRE_QUALIFICATION | Independent full-state reference after overflow, retry and bridge |
| E: license | LGPL v3/workspace label → Binance crate inheritance inspected (§E) | Selected files and package metadata; not legal authorization | Other component notices, linking/redistribution, data rights | REQUIRE_QUALIFICATION | Human/legal review for the actual proposed use |
| Source scoped facts | Code line and test assertions reviewed (§A–E) | Implementation at pinned revision only | Runtime and market behavior, adapter coverage | ACCEPT_SCOPED_FACT | Human verify cited paths and conditions |
| Market-level claims | No market data or experiment | Excluded from this task | Economic/statistical/causal and execution fidelity | UNKNOWN_OUT_OF_SCOPE | Separate approved research design and data rights |

No BLOCKING_CONTRADICTION was established in inspected paths. This does not
constitute a claim that no contradiction exists elsewhere. See the
[readiness packet](10_PROMOTION_READINESS_PACKET.md) for the human decision.
