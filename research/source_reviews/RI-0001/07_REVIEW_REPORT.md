# Review report — Phase 02B.1

Baseline: `236b5aee70c35e2017335ad96e19a2e069bec182`. Upstream pinned revision:
`33492c8135a5e0dceedc21d9ee3ff7432f04ff12`. All evidence is bounded to selected
files and line ranges in the [ledger](00_SCOPE_AND_EVIDENCE_LEDGER.md); the
review does not authorize lifecycle promotion. Catalog RI-0001 remains DISCOVERED.

Eight source-grounded observations cover timestamps, delta versus L1 stale
handling, cache ownership, frame boundaries, replay scheduling, recovery and
delivery order. The [test matrix](04_TACIT_ENGINEERING_DECISIONS.md) identifies
test source reviewed and the untested edges. Upstream code and tests were NOT RUN.
No issue or PR explanation was reviewed; maintainer motivation is UNKNOWN.

## License and security

The pinned [root LICENSE](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/LICENSE)
and [Python LICENSE](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/python/LICENSE)
contain GNU LGPL version 3 text. The pinned
[workspace Cargo.toml](https://github.com/nautechsystems/nautilus_trader/blob/33492c8135a5e0dceedc21d9ee3ff7432f04ff12/Cargo.toml#L50-L58)
declares `LGPL-3.0-only`. The applicability of workspace metadata to every
component, other notices, dependencies and linking/redistribution obligations
were not exhaustively checked. Any reuse requires human/legal review; this is not
a legal conclusion. No upstream implementation, credentials, private data or
market data were added, and no upstream installer or project code was executed.

## Human decisions and gaps

Review the scoped findings, source/test links, license and missing adapter evidence.
Before any later `SOURCE_REVIEWED` proposal, decide whether this partial coverage
is sufficient, which additional source/test/adapter evidence is required, and how
to append evidence and a lifecycle transition without rewriting history. The
Phase 02A-only discovery validator currently rejects promotion; a later approved
task must separately design and test the release-gate migration. This task does
not change the catalog, schema, governance or either validator.

The [experiment](06_FALSIFIABLE_EXPERIMENT_PROPOSAL.md) remains unexecuted until
rights, harness, dependencies and resource limits are approved. Market-level
validity, participant identity, economic significance and causal identification
remain UNKNOWN. Local tests and remote CI results are reported separately in the
task handoff; no unobserved result is implied here.

## Local validation performed

- `python3 -m unittest discover -s tests -v`: PASS, 30 local tests; upstream
  project's tests were not executed.
- `python3 -m tools.validate_catalog`: PASS.
- `python3 -m tools.validate_discovery`: PASS.
- GitHub HTTP access to 22 unique pinned file permalinks: 200; cited line ranges
  were checked against the fetched pinned file contents.
- The protected catalog, schema, validators and governance file matched the
  starting main during validation. Remote PR CI is NOT RUN until observed.
