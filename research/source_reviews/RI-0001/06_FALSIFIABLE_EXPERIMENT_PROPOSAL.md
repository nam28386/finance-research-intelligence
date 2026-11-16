# Proposed experiment — late delta versus book metadata

**PROPOSAL ONLY; NOT EXECUTED.** This is one bounded software experiment, not
a market experiment or trading signal. See F02 and its pinned source/test in the
[ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md).

- **Question:** Can a direct L2 book update with older venue metadata change
  visible state while `sequence` and `ts_last` remain at their prior high-water?
- **Hypothesis:** Given the reviewed direct-book path, a valid non-snapshot late
  add is applied; lower sequence/time produce a warning and do not reduce the
  stored high-water. Venue adapters may impose a different policy before entry.
- **Synthetic input contract:** One identical book/delta instrument ID, an
  empty L2_MBP book, `BookAction::Add`, buy side, positive quantity, valid and
  consistent price/size precision, input order ID 0, and `flags=0` for each
  standalone `apply_delta` call. No snapshot, clear, batch or venue adapter is
  involved. Include `sequence`, `ts_event`, and `ts_init` explicitly; `ts_init`
  is not assumed to be availability. Capture WARN logs with the log level and
  filtering configured to include the book module.
- **Sequence:** Start empty. Add bid 98, size 10, sequence 5, `ts_event=2000`,
  `ts_init=2000`, flags 0. Then add bid 99, size 10,
  sequence 3, `ts_event=1000`, `ts_init=3000`, flags 0.
- **Expected under the scoped hypothesis:** After the late add, best bid is 99,
  stored sequence remains 5, stored event-time high-water remains 2000, and a
  two warnings are captured, one for each regression. These are predicted
  outcomes, not executed results. L2 maps order identity from price using a
  deterministic hash: checking that both price levels survive additionally
  assumes distinct generated IDs. The best-bid hypothesis must not infer an
  exchange-correct book from the result. See the independent QA for code paths.
- **Falsifiers / failure:** A valid late add is rejected, best bid is unchanged,
  metadata regresses, warnings differ under controlled logging, or an observed
  prerequisite invalidates this scenario. Report results rather than modifying
  the fixture to match a desired outcome. Snapshot/clear paths are outside scope.
  Distinguish input invalidity, logging setup failure and code-observation mismatch
  instead of treating all failures as evidence of an exchange-data error.
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
