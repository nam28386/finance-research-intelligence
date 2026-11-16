# Phase 02A discovery protocol — v0.1

## Question and boundaries

Which public repositories merit a later, human-approved investigation of event
systems, order-book research, temporal integrity, institutional finance, or
agentic research engineering? Discovery creates candidates, not validated
mechanisms. A project's description is its own claim, not independent evidence.

This phase reads public GitHub repository/search pages and Git remote refs only.
No third-party repository was cloned, installed, or executed. API access was
blocked by the environment's restricted egress; browser-facing GitHub HTML and
Git HTTPS read-only responses supplied the observed metadata instead. The exact
page presentation and search ranking may change; queries and timestamps below
describe the observed snapshot, not a reproducible search ordering guarantee.

## Search log

At 2026-11-16 13:05:38–13:05:39 UTC, use GitHub repository search, first result
page only. Search ordering is GitHub's default; star counts are not a criterion.
Result counts are observations at retrieval, not evidence of research quality.

| Language | Query / reproducible URL | Results observed |
| --- | --- | --- |
| English | [order book reconstruction](https://github.com/search?q=order+book+reconstruction&type=repositories) | 167 |
| English | [market microstructure backtest](https://github.com/search?q=market+microstructure+backtest&type=repositories) | 77 |
| English | [point in time financial data](https://github.com/search?q=point+in+time+financial+data&type=repositories) | 85 |
| Chinese | [限价订单簿 回测](https://github.com/search?q=%E9%99%90%E4%BB%B7%E8%AE%A2%E5%8D%95%E7%B0%BF+%E5%9B%9E%E6%B5%8B&type=repositories) | 2 |
| English | [order book simulator](https://github.com/search?q=order+book+simulator&type=repositories) | 784 |

The seven named task seeds were added directly. From actual first-page results,
select `phancongdong/orderbook-l2-ofi` (order-book reconstruction query),
`fidetolabs/qanat` (point-in-time query), and `KangOxford/jax-lob` (simulator
query). Vietnamese text appeared in the first selected result, but no separate
Vietnamese-language query was run. No inference is made about the maturity of a
project merely because it matched a search.

## Collection and selection

1. Inspect public repository metadata pages for canonical identity and public
   visibility. Treat page descriptions as unverified maintainer claims.
2. Resolve HEAD with `git ls-remote --symref https://github.com/OWNER/REPO.git HEAD`.
   This is a read-only ref lookup, not a source-code inspection. Record the full
   SHA, observed default branch, and UTC recording timestamp. If unavailable,
   store null with `UNKNOWN`; never infer a revision from another source.
3. Record UI-reported license identifiers as **UNVERIFIED**; use null/UNKNOWN
   when missing. A label is not a legal review or proof that the pinned revision
   grants a particular right. Do not copy third-party code or datasets.
4. Include the seven user-specified seeds and three domain-relevant additional
   candidates. Deduplicate canonical owner/repository identities case-insensitively.
   Limit this round to ten selected candidates and the first page of each query.
5. Keep unknown evidence unknown. Do not rank by stars, silently omit rejection
   reasons, mark a candidate SOURCE_REVIEWED, or treat a SHA as empirical proof.

Repository pages and refs were queried between 13:06:03 and 13:06:07 UTC; catalog
records were recorded at 13:07:35 UTC. Default branches are listed in the matrix.
Because Git refs and pages can move, the recorded SHA denotes the observed HEAD;
the page-reported license is not asserted to have been verified at that SHA.

## Scoring design and evidence coverage

The future rubric has maximum weights: domain relevance **25**, mechanism and
architecture potential **20**, engineering maturity **20**, measurement and
temporal relevance **15**, cross-asset potential **10**, and maintenance/license/
security **10**. Do not assign a numeric score without an explicit criterion,
evidence, and human review; unobserved criteria are UNKNOWN, never zero quality.
Coverage is tracked independently: this round has repository page + Git ref
metadata, while source, tests, operational safety, empirical evidence, and legal
review remain UNKNOWN for all ten. Descriptive metadata does not establish that
an implementation meets its advertised properties.

The ordered pilot queue is a **research scheduling preference**, not a scored
ranking: NautilusTrader, hftbacktest, and RD-Agent cover distinct user-prioritized
questions in event systems, microstructure simulation, and research orchestration.
Their relative quality and performance remain unknown. See `CANDIDATE_MATRIX.md`.

## Release validation and later work

Run `python3 -m tools.validate_catalog`, `python3 -m tools.validate_discovery`,
`python3 -m unittest discover -s tests -v`, and compare with a trusted prior
catalog via `python3 -m tools.validate_catalog --base PATH`. These checks are
offline. The Phase 02A gate deliberately requires only DISCOVERED records and no
source-reviewed findings. A later, separately approved source review must revise
that release gate and its tests explicitly before any lifecycle promotion; it
must not silently suppress failures or change schema semantics.
