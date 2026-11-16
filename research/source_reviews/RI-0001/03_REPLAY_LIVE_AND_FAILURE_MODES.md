# Replay, live and failure modes

Source and tests for F01–F08 are pinned in the [ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md).

| Dimension | Replay / historical evidence | Live evidence | Status and limit |
| --- | --- | --- | --- |
| Software path | Backtest calls `process_data_ref` after venue routing (F06) | Live runner routes `DataEvent::Data` to `process_data`, which delegates non-DeFi paths to `process_data_ref` | Shared selected handler path; full software parity UNKNOWN |
| Data / framing | Historical deltas are split on `F_LAST`, trailing partial published (F05) | Configured buffering waits for `F_LAST` in reviewed test (F05) | Framing is path/config dependent; data parity UNKNOWN |
| Time / scheduling | `ts_init` drives reviewed replay loop (F06); virtual clock has nondecreasing advance (F08) | Live runner uses asynchronous event channels; end-to-end timestamp mapping not traced | Timestamp parity UNKNOWN |
| State | Historical response skips overwrite of live-managed cached book (F04) | BookUpdater maintains selected cached book path | State parity and race freedom UNKNOWN |
| Side effects | Backtest routes to a simulated venue before engine processing | Live event/command transport has different external interaction | Execution fidelity UNKNOWN; no order submission tested |

F07 **FACT:** `BookSync` starts Waiting; accepted snapshot permits Synced, and a
reported gap moves it to Recovering. A running recovery or armed deadline can
suppress a duplicate recovery request. Venue sequence decisions and wire buffers
belong to adapters; no universal gap detector has been proven. The reviewed
[`BookRecovery::run`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/live/src/book/recovery.rs#L145-L228)
implements bounded initial retries followed by a slower retry loop until snapshot
acceptance or cancellation, subject to adapter-provided callbacks. This does not
prove eventual recovery if a snapshot never arrives.

Failures, duplicate events, stale caches, partial-state rollback, restart and
reconnect behavior across a real venue remain UNKNOWN. Live transport, market-data
capture and realistic execution were not run. The source explains selected guards;
it does not establish end-to-end exactly-once or market-level fidelity.
