# Cross-asset transferability — hypotheses, not validation

Evidence for selected reusable mechanisms and their limits is in the
[ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md). All transfer assessments are
**HYPOTHESIS / UNKNOWN**, not `SUPPORTED`; no dataset or adapter was tested.

| Context | Potential reusable boundary | Required schema, clock and adapter checks | Missing observables / falsifier |
| --- | --- | --- | --- |
| COMEX Gold MBO/L3 | Event/sequence metadata, bounded state update, recovery ownership (F01/F04/F07) | Map exchange sequence, session resets, order IDs, snapshot/recovery semantics and source/receive availability; validate venue feed contract | Hidden/iceberg liquidity, feed gaps and timestamp provenance may defeat reconstruction; falsify with sequence-gap and snapshot fixtures |
| Crypto futures L2/L3 | Adapter-owned sequence policy and per-book state (F07) | Validate snapshot/delta bridge, venue sequence ranges, reconnect behavior, exchange vs receive clocks and contract mapping per venue | L2 cannot identify individual orders; checksum and sequencing rules may differ; falsify with venue-specific gap/reorder fixtures |
| VN30 futures MBP | Price-level state boundary and explicit availability clocks (F01/F03) | Match vendor/exchange depth, aggregation, session, symbol and packet semantics; create a separate MBP measurement model | Aggregate levels do not uniquely reconstruct order queues or actor identity; reject any design requiring unobserved individual events |
| Asset-agnostic research | Explicit event/creation time, cache ownership, replay manifest and test discipline (F01/F04/F06) | Preserve event, receive, availability and decision clocks, data rights, revisions and temporal joins | No reviewed source guarantees information availability or market-level replay parity; falsify with late/revised event fixtures |

None of these transfers establishes alpha, economic value, institutional actor
identity, exchange order priority or execution fidelity. An adapter contract,
synthetic tests, dataset provenance and a separately approved empirical design
are prerequisites to any stronger statement.
