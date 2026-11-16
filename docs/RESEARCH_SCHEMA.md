# Research catalog contract v0.1.0

The normative structure is the local Draft 2020-12 [JSON Schema](../schemas/research-catalog.schema.json).
The root contains exactly `schema_version: "0.1.0"` and `records: []`. Unknown
properties are rejected. Required lists may be empty until their lifecycle gate.

| Fields | Contract |
| --- | --- |
| `research_id`, `synthetic` | Unique stable `RI-0001` style ID; synthetic fixtures explicitly true |
| `repository_url` | HTTPS `github.com/owner/repository`, no credentials, query, fragment, trailing slash, or `.git` suffix |
| `upstream_commit_sha`, `revision_status` | Full lowercase 40-hex SHA + PINNED, or null + UNKNOWN; never `main`, shortened SHA, or made-up revision |
| `inspected_at` | Latest metadata/source review time, RFC3339 timestamp with explicit UTC offset |
| `license` | Identifier (e.g. SPDX expression) or null; UNKNOWN / UNVERIFIED / VERIFIED; evidence refs; identifier format is not legal verification |
| `research_domain` | Nonempty array of specific research domains |
| `source_references` | Repository-relative path, locator (symbol/lines), revision matching record, SOURCE evidence IDs; no files fetched |
| `technical_mechanisms`, `assumptions`, `limitations` | Arrays of labeled claims: statement, epistemic_status, evidence_refs, falsifiers |
| `evidence` | Locally unique `E-001` IDs; kind, inert reference, summary, recorded_at; kinds SOURCE / TEST / REPRODUCTION / EMPIRICAL / REVIEW |
| `test_references` | IDs resolving specifically to TEST evidence |
| `replication_status` | NOT_ATTEMPTED / PASSED / FAILED / BLOCKED; PASSED requires REPRODUCTION evidence |
| `applicability_across_assets` | Asset class, UNKNOWN / HYPOTHESIZED / SUPPORTED / NOT_APPLICABLE, labeled rationale; SUPPORTED requires EMPIRICAL evidence |
| `unresolved_questions` | Explicit remaining questions, including blockers |
| `decision` | DEFER / RETAIN / REJECT / SUPERSEDE with labeled rationale |
| `supersedes`, `superseded_by` | In-catalog reciprocal IDs; terminal state and cycle checks |
| `lifecycle_status`, `lifecycle_history` | Current state and append-only transition events; see governance |

Every claim is explicitly labeled FACT / MEASUREMENT / INFERENCE / HYPOTHESIS /
UNKNOWN. Unknown revision uses JSON null, not the string `"UNKNOWN"`. An unknown
license has null identifier; UNVERIFIED has a proposed identifier; VERIFIED also
needs SOURCE evidence. Do not infer reuse permission from a populated field.

Evidence IDs are scoped to their record, not the whole catalog. References may
identify public URLs or public-safe artifact paths and are never opened by the
validator. Evidence timestamps cannot postdate inspection or a transition citing
them. Source paths cannot be absolute or traverse parent directories.

The standard-library validator implements only the schema keywords used here:
local `$ref`, `$defs`, type, const, enum, properties, required,
additionalProperties, items, uniqueItems, minItems, minLength, pattern and
date-time format (plus descriptive metadata). Unsupported keywords fail closed.
It is **not** a general JSON Schema engine. Cross-field evidence, lifecycle,
revision, supersession, and optional base-comparison rules are additional Python
checks. Validation is offline and cannot prove that a SHA exists, a citation is
true, a reviewer approved, or a research claim is scientifically valid.

For revisions after source review, create a new research ID and link the old
record rather than mutating its provenance. Before review, UNKNOWN may be resolved
to a real SHA. Version semantics explicitly and propose migrations when changing
the schema. Do not silently accept unknown schema versions.
