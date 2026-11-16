# Financial Research Intelligence OS — Foundation v0.1

A minimal, provenance-aware research registry for an individual financial
researcher using AI-assisted engineering. Phase 02A adds a bounded, metadata-only
public repository discovery registry. No source execution, market data,
experiments, model training, RAG, database, or execution is implemented.

## Run locally

Requires Python **3.12+** and Git. No third-party Python dependencies, package
installation, credentials, network requests, or running services are needed.

```sh
python3 -m tools.validate_catalog
python3 -m tools.validate_discovery
python3 -m unittest discover -s tests -v
git diff --check
```

Run from the repository root. The production catalog `research/catalog.json`
contains public metadata-only DISCOVERED records. Tests use clearly marked
synthetic records with fictional repositories and revisions. Neither set is a
completed source review or a validated financial research finding.

Validate a proposed catalog against its previous version:

```sh
python3 -m tools.validate_catalog proposed.json --base previous.json
```

The CLI reads local JSON only, prints errors with field paths, and exits 0 on
success or 1 on invalid/unreadable input. It never fetches or executes evidence.

## Contracts and review

- [Goals](GOALS.md) and [roadmap](docs/ROADMAP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Research schema](schemas/research-catalog.schema.json) and
  [field guide](docs/RESEARCH_SCHEMA.md)
- [Phase 02A discovery protocol](docs/DISCOVERY_PROTOCOL.md),
  [candidate matrix](docs/CANDIDATE_MATRIX.md), and
  [proposed source review plan](docs/PHASE_02B_PLAN.md)
- [Lifecycle and evidence gates](docs/RESEARCH_GOVERNANCE.md)
- [Security and intellectual property](docs/SECURITY_BOUNDARIES.md)
- [Agent instructions](AGENTS.md)
- [Foundation validation report](docs/FOUNDATION_REPORT.md)

Passing validation establishes structural consistency, not source authenticity,
license permission, reproducibility, economic significance, or causality.
Human review remains required. GitHub Actions runs the same local checks with
read-only permissions; its remote result must be checked separately.
