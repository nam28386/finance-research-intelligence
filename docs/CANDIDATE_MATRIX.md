# Candidate matrix — metadata snapshot v0.1

All entries are **DISCOVERED / SOURCE_NOT_REVIEWED**. Potential mechanisms are
questions suggested by repository descriptions, not verified implementations.
All data, temporal semantics, tests, maintenance, security and empirical evidence
remain UNKNOWN until independently inspected. “Later” is not a negative quality
judgment; the three numbered pilots are an ordered research schedule.

The page-reported license is UNVERIFIED, not legal clearance; UNKNOWN means no
usable identifier was observed. Git refs were queried read-only. Recorded HEADs
may move. See the [discovery protocol](DISCOVERY_PROTOCOL.md) for the exact
searches, timestamps, inclusion rules, scoring weights, and coverage limitations.

| ID / repository | Observed HEAD (full SHA) | Domain / potential investigation | License label | Missing evidence | Phase 02B priority |
| --- | --- | --- | --- | --- | --- |
| RI-0001 [nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | [`33492c8135a5e0dceedc21d9ee3ff7432f04ff12`](https://github.com/nautechsystems/nautilus_trader/commit/33492c8135a5e0dceedc21d9ee3ff7432f04ff12) | Event-driven system, data/replay interfaces | LGPL-3.0 (UNVERIFIED) | Event ordering; recovery; parity; tests; rights | 1 — pilot |
| RI-0002 [nkaz001/hftbacktest](https://github.com/nkaz001/hftbacktest) | [`5f3ec40b2afb764e0fea112f941ed85523ef4e88`](https://github.com/nkaz001/hftbacktest/commit/5f3ec40b2afb764e0fea112f941ed85523ef4e88) | Queue, latency and L2/L3 simulation | MIT (UNVERIFIED) | L2/L3 assumptions; queue/fill inference; tests; rights | 2 — pilot |
| RI-0003 [databento/databento-python](https://github.com/databento/databento-python) | [`f6529f1062e0642fe52334d767a72f2a75244398`](https://github.com/databento/databento-python/commit/f6529f1062e0642fe52334d767a72f2a75244398) | Market-data client and data interfaces | Apache-2.0 (UNVERIFIED) | Data entitlements; timestamp semantics; feed gaps; tests | Later |
| RI-0004 [microsoft/RD-Agent](https://github.com/microsoft/RD-Agent) | [`484776c211e4fbbeef03e0ec00d6bbee7362a4f4`](https://github.com/microsoft/RD-Agent/commit/484776c211e4fbbeef03e0ec00d6bbee7362a4f4) | Research agent orchestration and evaluation | MIT (UNVERIFIED) | Evaluation independence; provenance; execution boundary; cost | 3 — pilot |
| RI-0005 [microsoft/qlib](https://github.com/microsoft/qlib) | [`54355232463878d2eebb91fe0ee5fa7fa1f5976c`](https://github.com/microsoft/qlib/commit/54355232463878d2eebb91fe0ee5fa7fa1f5976c) | Point-in-time quant research pipeline | MIT (UNVERIFIED) | Point-in-time availability; splits; tests; data rights | Later |
| RI-0006 [bmoscon/cryptofeed](https://github.com/bmoscon/cryptofeed) | [`2e05f5a061c1685eabb28b33fe535a020d88a6c6`](https://github.com/bmoscon/cryptofeed/commit/2e05f5a061c1685eabb28b33fe535a020d88a6c6) | Crypto market-data feed interfaces | UNKNOWN | Sequence gaps; exchange semantics; recovery; tests | Later |
| RI-0007 [vnpy/vnpy](https://github.com/vnpy/vnpy) | [`c6e231caf32b7fc97e6459817fff66458cf7e7c4`](https://github.com/vnpy/vnpy/commit/c6e231caf32b7fc97e6459817fff66458cf7e7c4) | Multi-asset platform and VN research interfaces | MIT (UNVERIFIED) | Market rules; adapters; data contracts; tests | Later |
| RI-0008 [phancongdong/orderbook-l2-ofi](https://github.com/phancongdong/orderbook-l2-ofi) | [`b5947d7aa7e6345b42bf9e6179c8ecd71598021f`](https://github.com/phancongdong/orderbook-l2-ofi/commit/b5947d7aa7e6345b42bf9e6179c8ecd71598021f) | L2 reconstruction and OFI | MIT (UNVERIFIED) | Small public history; OFI definition; ordering; tests | Later |
| RI-0009 [fidetolabs/qanat](https://github.com/fidetolabs/qanat) | [`1fbe05222318359467fb105ead1f6393dc358b6a`](https://github.com/fidetolabs/qanat/commit/1fbe05222318359467fb105ead1f6393dc358b6a) | Point-in-time financial data lineage | MIT (UNVERIFIED) | Data revisions; availability; point-in-time semantics; tests | Later |
| RI-0010 [KangOxford/jax-lob](https://github.com/KangOxford/jax-lob) | [`d1f596610b04a09941c7a1b609e5bab541ecfc98`](https://github.com/KangOxford/jax-lob/commit/d1f596610b04a09941c7a1b609e5bab541ecfc98) | Order-book simulation and state updates | UNKNOWN | License; fidelity; market assumptions; tests | Later |

## Provenance and defaults

Repository metadata pages were retrieved around 2026-11-16 13:06 UTC; each
record's `E-001` references its page and `E-002` the observed SHA. The default
branch below was observed via `git ls-remote --symref`; the catalog timestamp
(2026-11-16 13:07:35 UTC) is when the observations were recorded, not a claim
that a source review was completed. A commit link permits later inspection but
does not independently prove that it was HEAD at recording time.

| Repository | Observed default branch | Metadata page retrieval (UTC) |
| --- | --- | --- |
| [nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | `develop` | 2026-11-16T13:06:04+00:00 |
| [nkaz001/hftbacktest](https://github.com/nkaz001/hftbacktest) | `master` | 2026-11-16T13:06:03+00:00 |
| [databento/databento-python](https://github.com/databento/databento-python) | `main` | 2026-11-16T13:06:04+00:00 |
| [microsoft/RD-Agent](https://github.com/microsoft/RD-Agent) | `main` | 2026-11-16T13:06:04+00:00 |
| [microsoft/qlib](https://github.com/microsoft/qlib) | `main` | 2026-11-16T13:06:05+00:00 |
| [bmoscon/cryptofeed](https://github.com/bmoscon/cryptofeed) | `master` | 2026-11-16T13:06:05+00:00 |
| [vnpy/vnpy](https://github.com/vnpy/vnpy) | `master` | 2026-11-16T13:06:05+00:00 |
| [phancongdong/orderbook-l2-ofi](https://github.com/phancongdong/orderbook-l2-ofi) | `main` | 2026-11-16T13:06:05+00:00 |
| [fidetolabs/qanat](https://github.com/fidetolabs/qanat) | `main` | 2026-11-16T13:06:07+00:00 |
| [KangOxford/jax-lob](https://github.com/KangOxford/jax-lob) | `jaxV3` | 2026-11-16T13:06:06+00:00 |

## Explicit exclusions for this round

These exclusions are scope choices based on search snippets, not conclusions
about the projects or their quality. No selected or excluded source was executed.

- `bobeezy/Video-Store-ATM-Point-Of-Sale-System`: the point-in-time query returned
  an unrelated retail/POS result, outside the specified finance research domains.
- `aid435964-hue/lobster-CNN`: the Chinese query returned an ML and LOBSTER-data
  research description; prioritize the metadata-only infrastructure remit, with
  dataset availability/rights and model behavior unresolved.
- `marketlenstrade/marketlens-python`: the reconstruction query returned a
  Polymarket-focused data SDK; defer the narrower venue while selecting the
  specified seeds and complementary general research questions.
- `KangOxford/AlphaTrade`: the simulator query returned a description overlapping
  JAX-LOB; select one candidate for the limited round without asserting identical
  code or treating it as a duplicate.

No other candidates are represented as having been fully assessed. A future
review may reconsider exclusions and expand the sample through a new recorded search.
