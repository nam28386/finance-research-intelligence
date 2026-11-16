# Architecture v0.1

```text
Discovery → Source Evidence → Mechanism/Contract Extraction → Reproduction
          → Validation → Knowledge Registry → Optional Project Integration
```

Phase 01 implements metadata contracts and review gates for these stages, not
their execution. There is one local JSON registry, no service or database.

| Boundary | Future input → output | Phase 01 representation |
| --- | --- | --- |
| Discovery | Human-approved scope → candidate | URL, domain, DISCOVERED record |
| Source Evidence | Pinned source → cited observations | SHA, source refs, license, evidence |
| Contract Extraction | Observations → falsifiable mechanism | Labeled claims, assumptions, limits, falsifiers |
| Reproduction | Approved contract/environment → run artifacts | Replication status, REPRODUCTION evidence |
| Validation | Frozen design + run → bounded conclusions | EMPIRICAL evidence, independent review |
| Knowledge Registry | Reviewed records → versioned knowledge | `research/catalog.json`, history, supersession |
| Project Integration | Approved knowledge → separate project proposal | Future interface only; no repository writes |

`schemas/research-catalog.schema.json` is the structural contract.
`tools/validate_catalog.py` evaluates its explicitly supported JSON Schema subset
and applies cross-field/lifecycle rules. No input reference is resolved over the
network. `--base` additionally preserves prior records and append-only histories.
`tests/` exercises synthetic valid/invalid catalogs and CLI behavior.

Future experiment interfaces must preserve research ID, hypothesis, source/data
versions and rights, code revision, runtime, event/availability/decision clocks,
feature/label definitions, time-safe splits, costs, metrics, artifacts, failures,
and falsifiers. Unknown inputs block dependent claims. These interfaces are
documented requirements, not implemented pipelines.

Schema changes require a version increment and migration/review plan. Research
meaning, data acquisition, empirical interpretation, and integration remain human
decisions. No agent output is authoritative evidence merely because it is stored.
