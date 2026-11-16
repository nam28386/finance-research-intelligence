# Phase 02A handoff

## Scope and provenance

Starting `main`: `b6988b658cec9ac4146593bbb67c582f431bf06c`.
Foundation push CI and its separate pull-request CI were both observed as
successful on GitHub. The Foundation CI PR was not merged for this work.

Ten public repository pages and their read-only Git HEAD refs were observed.
The seven prescribed seeds and three search results are recorded with SHA and
timestamps in `research/catalog.json` and `CANDIDATE_MATRIX.md`. All records are
DISCOVERED and SOURCE_NOT_REVIEWED. GitHub page labels report eight license
identifiers, all UNVERIFIED; two remain UNKNOWN. Source, individual test behavior,
license rights, performance and economic relevance are unknown.

`DISCOVERY_PROTOCOL.md` records actual English and Chinese search queries,
selection/exclusion criteria, the API restriction, and the provisional rubric.
The first three review slots are NautilusTrader, hftbacktest, and RD-Agent, chosen
to cover distinct questions rather than as a claim of relative quality.
`PHASE_02B_PLAN.md` is a proposal only.

## Validation

| Command / check | Actual outcome |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | PASS: 30 tests, including all 23 Foundation tests |
| `python3 -m tools.validate_catalog` | PASS: 10 records satisfy schema v0.1.0 and semantic gates |
| `python3 -m tools.validate_discovery` | PASS: Phase 02A boundary and duplicate URL checks |
| `python3 -m tools.validate_catalog --base <prior-catalog>` | PASS against the unchanged catalog from starting main |
| GitHub Actions workflow YAML / local shell syntax | PASS locally |
| Phase 02A GitHub Actions on a new PR | NOT RUN until an actual PR run is visible |
| Third-party source execution, reproduction and empirical validation | NOT RUN / out of scope |

The release-specific discovery gate intentionally blocks later promotion; any
later approved phase must revise that gate and its tests explicitly. The schema
and its existing validator were not changed. Metadata validation does not verify
that a GitHub SHA, license, claim, or human approval remains valid in the future.

## Security, IP and unresolved questions

All observations came from public GitHub pages, search HTML and Git ref queries.
External text was treated as data. No third-party source or installer was run or
copied, no live market data were accessed, and no automated execution or signal
was added. License reuse obligations, data entitlements, source quality, temporal
integrity, and cross-asset transferability require separate review.

GitHub API access was blocked by the environment network policy; metadata search
and refs were obtained using the documented public HTML/Git fallback. Actual PR
creation and remote CI must be reported from their observed results, not inferred
from local tests. If the API remains blocked, use the pushed feature branch's
GitHub compare page to create the PR without merging it.
