# Event time and ordering

All finding IDs refer to the [evidence ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md),
which provides pinned line-level source and test links. Labels and scope are
specific to the inspected code paths; upstream tests were **NOT RUN**.

| Research concept | Observed field / behavior | Limitation |
| --- | --- | --- |
| event_time | `ts_event`: model comment says when event occurred (F01) | Exact exchange clock/adapter provenance UNKNOWN |
| exchange_time | No separately named `exchange_time` was established | Venue `sequence` is an ordering identifier, not a timestamp; source-clock meaning of `ts_event` is adapter-specific |
| receive_time | No distinct field identified in these two structs | Other adapters/types not exhaustively reviewed |
| availability_time | No distinct field established | Cannot assume `ts_init` equals first usable time |
| processing_time | No separate processing-time field established | The model documents `ts_init` as creation time, but a reviewed Binance recovery path can modify it; it is not a universal processing or receive clock |
| decision_time | No field established in reviewed models | Must be separately defined by a future experiment |

F06 **FACT:** the reviewed backtest path sorts and advances by `ts_init`; equal
time stream priorities and pending frontiers have their own rules. It does not
prove `ts_init` was observable at a historical decision. A safe research contract
would require `availability_time(feature) <= decision_time`, plus evidence that
the availability clock and all transformations are valid. This is a proposed
research invariant, not an upstream field or an observed leakage defect.
For a scoped Binance adapter example and its timestamp fallbacks and rewrites,
see [independent QA](08_INDEPENDENT_EVIDENCE_AUDIT.md#e-timestamp-and-availability).

F02/F03 **FACT:** non-snapshot delta updates with regressing metadata can warn
while their operation is applied and metadata high-water is retained; stale L1
quote/trade paths return early. Snapshots and clears have different rules. Gap
identification for live `BookSync` is delegated to venue adapters (F07), and
duplicate/exactly-once behavior is UNKNOWN. `F_LAST` framing is separately
relevant to visibility timing (F05). Proposed falsifiers and reviewed tests are
in the ledger; neither ordering across all components nor exchange-clock accuracy
was verified.
