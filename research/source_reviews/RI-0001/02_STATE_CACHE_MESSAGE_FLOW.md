# State, cache and message flow

The [ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md) contains full pinned evidence,
limitations and tests. This map is bounded to the paths actually read:

```text
live DataEvent → message-bus DataEngine endpoint → process_data → process_data_ref
backtest row → simulated venue routing → process_data_ref → typed handlers
book-delta publication → BookUpdater → cached OrderBook → optional derived quote
```

The live runner's [`handle_data_event`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/live/src/runner.rs#L543-L558)
sends market `Data` to the engine endpoint. The registered endpoint invokes
[`process_data`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/mod.rs#L386-L393),
which delegates non-DeFi variants to [`process_data_ref`](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/mod.rs#L1759-L1803).
The backtest path invokes the borrowed method after venue routing
([F06 source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/backtest/src/engine.rs#L979-L1008)).
Adapter normalization and every business consumer were not traced.

For book data, the updater applies a delta batch to the cached book and, when
configured, derives a quote after a successful application
([source](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/crates/data/src/engine/book.rs#L925-L979)).
F04 describes the distinct historical response ownership guard; it does not
prove all cache operations are atomic or safe across threads. F08 describes
subscription ordering, not a global ordering of all market events.

F02–F03 identify observed state transitions for selected book updates. Error
branches include instrument mismatch and unresolved/ambiguous side conditions;
some unknown no-side updates/deletes are skipped. Missing data reconstruction,
duplicate semantics, transaction rollback, position/order ownership, and adapter
concurrency are UNKNOWN. A future fixture must compare the actual state and
observable output, not only metadata high-water or an `Ok` return.
