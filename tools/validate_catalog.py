"""Validate local catalog metadata; never fetch references or execute source code."""

import argparse
from datetime import datetime
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/research-catalog.schema.json"
STAGES = (
    "DISCOVERED", "SOURCE_REVIEWED", "CONTRACT_EXTRACTED", "REPRODUCED",
    "ADAPTED", "EMPIRICALLY_VALIDATED",
)
GATES = {
    "SOURCE_REVIEWED": {"SOURCE"},
    "CONTRACT_EXTRACTED": {"SOURCE"},
    "REPRODUCED": {"REPRODUCTION"},
    "ADAPTED": {"TEST", "REVIEW"},
    "EMPIRICALLY_VALIDATED": {"EMPIRICAL", "REVIEW"},
}
KEYWORDS = {
    "$schema", "$defs", "$ref", "title", "description", "type", "const", "enum",
    "properties", "required", "additionalProperties", "items", "uniqueItems",
    "minItems", "minLength", "pattern", "format",
}
TYPES = {"object": dict, "array": list, "string": str, "null": type(None), "boolean": bool}


def timestamp(value):
    """RFC3339 subset: seconds, optional fraction, explicit offset; no leap seconds."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)", value):
        raise ValueError("expected date-time with explicit timezone")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def nonfinite(value):
        raise ValueError(f"non-finite JSON number: {value}")

    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=pairs, parse_constant=nonfinite)


def load_schema():
    schema = load_json(SCHEMA_PATH)

    def check(node):
        unsupported = node.keys() - KEYWORDS
        if unsupported:
            raise ValueError(f"unsupported schema keywords: {sorted(unsupported)}")
        if "$ref" in node and node["$ref"] not in {f"#/$defs/{k}" for k in schema["$defs"]}:
            raise ValueError("only known local schema references are supported")
        for group in ("properties", "$defs"):
            for child in node.get(group, {}).values():
                check(child)
        if "items" in node:
            check(node["items"])
        if "format" in node and node["format"] != "date-time":
            raise ValueError("unsupported schema format")

    check(schema)
    return schema


def structure_errors(value, node, schema, path="$root"):
    errors = []
    if "$ref" in node:
        errors += structure_errors(value, schema["$defs"][node["$ref"].split("/")[-1]], schema, path)
    if "type" in node:
        kinds = node["type"] if isinstance(node["type"], list) else [node["type"]]
        if type(value) not in [TYPES[kind] for kind in kinds]:
            return errors + [f"{path}: expected {kinds}"]
    for key in ("const", "enum"):
        if key in node and value not in (node[key] if key == "enum" else [node[key]]):
            errors.append(f"{path}: invalid {key} value")
    if isinstance(value, dict):
        properties = node.get("properties", {})
        for name in node.get("required", []):
            if name not in value:
                errors.append(f"{path}.{name}: required")
        if node.get("additionalProperties") is False:
            for name in sorted(value.keys() - properties.keys()):
                errors.append(f"{path}.{name}: unknown field")
        for name in value.keys() & properties.keys():
            errors += structure_errors(value[name], properties[name], schema, f"{path}.{name}")
    if isinstance(value, list):
        if len(value) < node.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if node.get("uniqueItems") and any(item in value[:i] for i, item in enumerate(value)):
            errors.append(f"{path}: duplicate items")
        for i, item in enumerate(value):
            if "items" in node:
                errors += structure_errors(item, node["items"], schema, f"{path}[{i}]")
    if isinstance(value, str):
        if len(value) < node.get("minLength", 0) or ("pattern" in node and not re.search(node["pattern"], value)):
            errors.append(f"{path}: invalid string format")
        if node.get("format") == "date-time":
            try:
                timestamp(value)
            except ValueError:
                errors.append(f"{path}: invalid date-time")
    return errors


def record_errors(record):
    errors = []
    rid = record["research_id"]

    def fail(message):
        errors.append(f"{rid}: {message}")

    inspected = timestamp(record["inspected_at"])
    evidence = {e["evidence_id"]: e for e in record["evidence"]}
    if len(evidence) != len(record["evidence"]):
        fail("duplicate evidence IDs")
    for e in evidence.values():
        if timestamp(e["recorded_at"]) > inspected:
            fail("evidence postdates inspected_at")

    def kinds(refs):
        return {evidence[ref]["kind"] for ref in refs if ref in evidence}

    def walk(value):
        if isinstance(value, dict):
            refs = value.get("evidence_refs", [])
            if any(ref not in evidence for ref in refs):
                fail("unresolved evidence reference")
            label = value.get("epistemic_status")
            if label in {"FACT", "MEASUREMENT", "INFERENCE"} and not refs:
                fail(f"{label} claim requires evidence")
            if label == "HYPOTHESIS" and not value["falsifiers"]:
                fail("HYPOTHESIS requires falsifiers")
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(record)
    if (record["upstream_commit_sha"] is None) != (record["revision_status"] == "UNKNOWN"):
        fail("revision_status must match null/known upstream SHA")
    if record["repository_url"].endswith(".git"):
        fail("repository_url must omit .git suffix")
    license_info = record["license"]
    if (license_info["identifier"] is None) != (license_info["verification_status"] == "UNKNOWN"):
        fail("license identifier must match verification status")
    if license_info["verification_status"] == "VERIFIED" and "SOURCE" not in kinds(license_info["evidence_refs"]):
        fail("VERIFIED license requires SOURCE evidence")
    for ref in record["source_references"]:
        path = PurePosixPath(ref["path"])
        if path.is_absolute() or ".." in path.parts or "\\" in ref["path"] or ":" in ref["path"] or ref["path"] == ".":
            fail("source path must be repository-relative without traversal")
        if ref["commit_sha"] != record["upstream_commit_sha"]:
            fail("source revision differs from upstream SHA")
        if "SOURCE" not in kinds(ref["evidence_refs"]):
            fail("source reference requires SOURCE evidence")
    if any(ref not in evidence or evidence[ref]["kind"] != "TEST" for ref in record["test_references"]):
        fail("test_references must resolve to TEST evidence")
    all_kinds = {e["kind"] for e in evidence.values()}
    if record["replication_status"] == "PASSED" and "REPRODUCTION" not in all_kinds:
        fail("PASSED replication requires REPRODUCTION evidence")
    for asset in record["applicability_across_assets"]:
        if asset["assessment"] == "SUPPORTED" and "EMPIRICAL" not in kinds(asset["rationale"]["evidence_refs"]):
            fail("SUPPORTED asset applicability requires EMPIRICAL evidence")

    current, resume, highest, previous_time = None, None, 0, None
    for event in record["lifecycle_history"]:
        target, when = event["to"], timestamp(event["at"])
        allowed = {"DISCOVERED"} if current is None else set()
        if current in STAGES:
            index = STAGES.index(current)
            allowed = set(STAGES[index + 1:index + 2]) | {"BLOCKED", "REJECTED", "SUPERSEDED"}
        elif current == "BLOCKED":
            allowed = {resume, "REJECTED", "SUPERSEDED"}
        if event["from"] != current or target not in allowed:
            fail(f"invalid lifecycle transition {event['from']} -> {target}")
        if (previous_time is not None and when < previous_time) or when > inspected:
            fail("history timestamps out of order or after inspected_at")
        if any(timestamp(evidence[ref]["recorded_at"]) > when for ref in event["evidence_refs"] if ref in evidence):
            fail("transition cites evidence recorded later")
        required = {"REVIEW"} if current == "BLOCKED" and target == resume else GATES.get(target, set())
        if not required <= kinds(event["evidence_refs"]):
            fail(f"{target} transition requires evidence kinds {sorted(required)}")
        if target == "BLOCKED":
            resume = current
        if target in STAGES:
            highest = max(highest, STAGES.index(target))
        current, previous_time = target, when
    if current != record["lifecycle_status"]:
        fail("lifecycle_status differs from last history event")
    if highest >= 1 and (record["revision_status"] != "PINNED" or not record["source_references"] or "SOURCE" not in all_kinds):
        fail("SOURCE_REVIEWED requires pinned source and SOURCE evidence")
    if highest >= 2 and any(not record[field] for field in ("technical_mechanisms", "assumptions", "limitations")):
        fail("CONTRACT_EXTRACTED requires mechanisms, assumptions and limitations")
    if highest >= 3 and (record["replication_status"] != "PASSED" or license_info["verification_status"] != "VERIFIED"):
        fail("REPRODUCED requires PASSED replication and VERIFIED license")
    if highest >= 4 and not record["test_references"]:
        fail("ADAPTED requires test references")
    state, decision = record["lifecycle_status"], record["decision"]["status"]
    if (state == "REJECTED") != (decision == "REJECT") or (state == "SUPERSEDED") != (decision == "SUPERSEDE"):
        fail("terminal decision and lifecycle status must match")
    if (state == "SUPERSEDED") != (record["superseded_by"] is not None):
        fail("SUPERSEDED requires superseded_by; other states must leave it null")
    return errors


def validate_catalog(catalog, base=None):
    """Return deterministic diagnostics; base must itself be a valid trusted snapshot."""
    schema = load_schema()
    errors = structure_errors(catalog, schema, schema)
    if errors:
        return sorted(errors)
    records = {record["research_id"]: record for record in catalog["records"]}
    if len(records) != len(catalog["records"]):
        errors.append("catalog: duplicate research IDs")
    for rid, record in records.items():
        errors += record_errors(record)
        for old in record["supersedes"]:
            if old == rid or old not in records or records[old]["superseded_by"] != rid:
                errors.append(f"{rid}: supersedes link must resolve reciprocally")
        target = record["superseded_by"]
        if target is not None and (target == rid or target not in records or rid not in records[target]["supersedes"]):
            errors.append(f"{rid}: superseded_by link must resolve reciprocally")
        seen, cursor = {rid}, target
        while cursor in records:
            if cursor in seen:
                errors.append(f"{rid}: supersession cycle")
                break
            seen.add(cursor)
            cursor = records[cursor]["superseded_by"]
    if base is not None:
        base_errors = validate_catalog(base)
        if base_errors:
            return sorted(errors + [f"base invalid: {error}" for error in base_errors])
        for old in base["records"]:
            rid = old["research_id"]
            if rid not in records:
                errors.append(f"{rid}: prior record cannot be deleted; reject or supersede it")
                continue
            new = records[rid]
            history = old["lifecycle_history"]
            if new["lifecycle_history"][:len(history)] != history:
                errors.append(f"{rid}: prior lifecycle history is immutable")
            new_evidence = {e["evidence_id"]: e for e in new["evidence"]}
            if any(new_evidence.get(e["evidence_id"]) != e for e in old["evidence"]):
                errors.append(f"{rid}: prior evidence is immutable; append a new evidence ID")
            reviewed = any(e["to"] == "SOURCE_REVIEWED" for e in history)
            if reviewed and any(new[k] != old[k] for k in ("repository_url", "upstream_commit_sha", "synthetic")):
                errors.append(f"{rid}: source-reviewed provenance is immutable; use a new research ID")
            if timestamp(new["inspected_at"]) < timestamp(old["inspected_at"]):
                errors.append(f"{rid}: inspected_at cannot move backwards")
    return sorted(errors)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", nargs="?", type=Path, default=ROOT / "research/catalog.json")
    parser.add_argument("--base", type=Path, help="trusted prior catalog for history/provenance checks")
    args = parser.parse_args(argv)
    try:
        errors = validate_catalog(load_json(args.catalog), load_json(args.base) if args.base else None)
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.catalog}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
