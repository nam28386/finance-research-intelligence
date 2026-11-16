# Financial Research Intelligence OS — Foundation v0.1

A minimal, provenance-aware research registry for an individual financial
researcher using AI-assisted engineering. **Phase 01 only**: no repository
discovery, market data, experiments, model training, RAG, database, or execution.

## Run locally

Requires Python **3.12+** and Git. No third-party Python dependencies, package
installation, credentials, network requests, or running services are needed.

```sh
python3 -m tools.validate_catalog
python3 -m unittest discover -s tests -v
git diff --check
```

Run from the repository root. The production catalog `research/catalog.json` is
intentionally empty. Tests use clearly marked synthetic records with fictional
repositories and revisions; they are not completed financial research.

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
- [Lifecycle and evidence gates](docs/RESEARCH_GOVERNANCE.md)
- [Security and intellectual property](docs/SECURITY_BOUNDARIES.md)
- [Agent instructions](AGENTS.md)
- [Foundation validation report](docs/FOUNDATION_REPORT.md)

Passing validation establishes structural consistency, not source authenticity,
license permission, reproducibility, economic significance, or causality.
Human review remains required. GitHub Actions runs the same local checks with
read-only permissions; its remote result must be checked separately.
