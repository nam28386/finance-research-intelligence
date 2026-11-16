# Proposed experiment — late delta versus book metadata

**PROPOSAL ONLY; NOT EXECUTED.** This is one bounded software experiment, not
a market experiment or trading signal. See F02 and its pinned source/test in the
[ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md).

- **Question:** Can a direct L2 book update with older venue metadata change
  visible state while `sequence` and `ts_last` remain at their prior high-water?
- **Hypothesis:** Given the reviewed direct-book path, a valid non-snapshot late
  add is applied; lower sequence/time produce a warning and do not reduce the
  stored high-water. Venue adapters may impose a different policy before entry.
- **Synthetic input contract:** One instrument, L2 MBP, buy side, positive size,
  valid price precision, `action`, `flags`, `sequence`, `ts_event`, `ts_init`.
  Set both timestamps explicitly; do not treat `ts_init` as proven availability.
- **Sequence:** Start empty. Add bid 98, size 10, sequence 5, `ts_event=2000`,
  `ts_init=2000`, ordinary non-snapshot flags. Then add bid 99, size 10,
  sequence 3, `ts_event=1000`, `ts_init=3000`, same valid ordinary flags.
- **Expected under the scoped hypothesis:** After the late add, best bid is 99,
  stored sequence remains 5, stored event-time high-water remains 2000, and a
  lower-sequence/older-time warning is observable. Verify actual flags, constructor
  requirements and book type before execution; these are predicted outcomes.
- **Falsifiers / failure:** A valid late add is rejected, best bid is unchanged,
  metadata regresses, warnings differ under controlled logging, or an observed
  prerequisite invalidates this scenario. Report results rather than modifying
  the fixture to match a desired outcome. Snapshot/clear paths are outside scope.
- **Information set:** Synthetic events only; real venue feed, receipt and
  availability times, queue identity and live transport are unavailable.
- **Manifest:** research ID, full upstream commit, independent test-harness
  revision, license decision, OS/runtime/dependencies, synthetic input hash,
  exact commands, clock/flag interpretation, outputs, logs and failure artifacts.
- **Bound:** One process, two synthetic events, no network during the run, no
  market feed or credentials; set CPU/memory/time limits after inspecting the
  build and dependencies. A human must approve rights, commands, dependencies,
  isolation and resource limits before execution. Upstream tests remain NOT RUN.

Even a successful run would establish only scoped software behavior. It would not
establish measurement validity, exchange behavior, P&L, causality or actor identity.
