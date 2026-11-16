# Practical engineering lessons and test traceability

The [ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md) provides commit-pinned sources,
tests, assumptions and per-finding falsifiers. The observations below describe
implementation/tests, not a verified maintainer motivation. No issue or PR
discussion was inspected; maintainer-stated motivation is **UNKNOWN**.

| ID | Code-to-test observation | Engineering inference and gap | Future synthetic fixture |
| --- | --- | --- | --- |
| F02 | `OrderBook::apply_delta` / `increment` → warning-boundary test checks warnings and high-water | Non-regressing metadata alone is insufficient to show non-regressing book state; adapter filtering is unreviewed | Insert a late valid bid at a better price and check both book and metadata |
| F03 | L1 quote/trade update methods → stale tick tests check unchanged best prices | Book type and ingestion path change stale policy; no universal stale rule established | Equal-time, older-time and out-of-order cases for each book type |
| F04 | Historical response handler → live-owned-cache test checks update count and response delivery | Separate request delivery from ownership of the live cache; no global race-freedom claim | Interleave request completion and successive live deltas |
| F05 | Delta dispatch / historical framing → `F_LAST` buffer tests | Frame boundary and partial tail affect what a subscriber sees and when | Missing terminator, reconnect and late fragment per supported path |
| F06 | `BacktestEngine::add_data` / replay loop → mixed stream ordering and unsorted-run tests | Recorded initialization time and tie-break rules are part of reproducibility | Equal `ts_init`, reversed `ts_event`, and partial-source frontier |
| F07 | `BookSync::gap` / `accept_snapshot` → inline gate and recovery ownership tests | The shared sync state machine does not itself establish venue-specific gap rules | Adapter-specific sequence gap, concurrent recovery and failed snapshot |
| F08 | Bus subscription comparator / virtual clock → subscription and timer-order tests | Handler order and timer order are distinct from market-event ordering | Equal-priority handlers with equal-time events and nested publication |

For the referenced examples: **TEST LOCATED = yes; TEST SOURCE REVIEWED = yes;
TEST EXECUTED = no; TEST PASSED = unknown.** Review of a single case does not
establish complete coverage. Cache race behavior, failure propagation, every
adapter and performance benchmarks were not verified.
