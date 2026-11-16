"""Deterministic structural, provenance, lifecycle, and CLI contract tests."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools import validate_catalog as validator

FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name="valid_unknown.json"):
    return validator.load_json(FIXTURES / name)


class CatalogTests(unittest.TestCase):
    def assert_invalid(self, catalog, message, base=None):
        errors = validator.validate_catalog(catalog, base)
        self.assertTrue(any(message in error for error in errors), errors)

    def test_production_catalog_is_valid_without_synthetic_research(self):
        catalog = validator.load_json(validator.ROOT / "research/catalog.json")
        self.assertEqual([], validator.validate_catalog(catalog))
        self.assertFalse(any(record["synthetic"] for record in catalog["records"]))

    def test_positive_fixtures(self):
        for name in ("valid_unknown.json", "valid_lifecycle.json"):
            with self.subTest(fixture=name):
                catalog = fixture(name)
                self.assertTrue(all(record["synthetic"] for record in catalog["records"]))
                self.assertEqual([], validator.validate_catalog(catalog))

    def test_negative_fixture_skips_lifecycle_gates(self):
        self.assert_invalid(fixture("invalid_transition.json"), "invalid lifecycle transition")

    def test_structural_errors(self):
        cases = [
            ("missing ID", lambda r: r.pop("research_id"), "research_id: required"),
            ("missing state", lambda r: r.pop("lifecycle_status"), "lifecycle_status: required"),
            ("bad ID", lambda r: r.update(research_id="invented"), "research_id: invalid"),
            ("bad state", lambda r: r.update(lifecycle_status="COMPLETE"), "lifecycle_status: invalid"),
            ("extra field", lambda r: r.update(confidence=1), "confidence: unknown field"),
            ("type", lambda r: r.update(synthetic="yes"), "synthetic: expected"),
            ("empty domain", lambda r: r.update(research_domain=[]), "too few items"),
            ("whitespace", lambda r: r["decision"]["rationale"].update(statement="  "), "invalid string format"),
            ("empty history", lambda r: r.update(lifecycle_history=[]), "too few items"),
        ]
        for name, mutate, message in cases:
            with self.subTest(case=name):
                catalog = fixture()
                mutate(catalog["records"][0])
                self.assert_invalid(catalog, message)

    def test_catalog_shape_version_and_duplicate_ids(self):
        for catalog, message in [
            ([], "expected"), ({}, "required"),
            ({"schema_version": "2.0", "records": []}, "invalid const"),
            ({"schema_version": "0.1.0", "records": [None]}, "expected"),
        ]:
            with self.subTest(catalog=catalog):
                self.assert_invalid(catalog, message)
        catalog = fixture()
        catalog["records"].append(deepcopy(catalog["records"][0]))
        self.assert_invalid(catalog, "duplicate research IDs")

    def test_repository_urls(self):
        for url in ["http://github.com/a/b", "https://evil.example/a/b", "https://github.com/a/b/",
                    "https://user:password@github.com/a/b", "https://github.com/a/b?token=x",
                    "https://github.com/a/b#fragment", "git@github.com:a/b", "https://github.com/a/b.git",
                    "https://github.com/a/b\n"]:
            with self.subTest(url=url):
                catalog = fixture()
                catalog["records"][0]["repository_url"] = url
                self.assert_invalid(catalog, "repository_url")

    def test_revision_unknown_and_sha_contract(self):
        for sha, status in [(None, "PINNED"), ("a" * 40, "UNKNOWN"), ("UNKNOWN", "UNKNOWN"),
                            ("main", "PINNED"), ("abc123", "PINNED"), ("A" * 40, "PINNED")]:
            with self.subTest(sha=sha, status=status):
                catalog = fixture()
                catalog["records"][0].update(upstream_commit_sha=sha, revision_status=status)
                self.assert_invalid(catalog, "revision" if sha is None or len(sha) == 40 and sha.islower() else "upstream_commit_sha")

    def test_timestamp_contract(self):
        for value in ["2026-01-01", "2026-01-01T00:00:00", "2026-02-30T00:00:00Z",
                      "2026-01-01T00:00:00+24:00", "2026-01-01T00:00:00+07:60"]:
            with self.subTest(value=value):
                catalog = fixture()
                catalog["records"][0]["inspected_at"] = value
                self.assert_invalid(catalog, "date-time")
        catalog = fixture()
        catalog["records"][0]["inspected_at"] = "2026-01-01T07:00:00+07:00"
        self.assertEqual([], validator.validate_catalog(catalog))

    def test_evidence_resolution_and_kinds(self):
        cases = [
            (lambda r: r["evidence"].append(deepcopy(r["evidence"][0])), "duplicate evidence"),
            (lambda r: r["technical_mechanisms"][0].update(evidence_refs=["E-999"]), "unresolved evidence"),
            (lambda r: r.update(test_references=["E-001"]), "resolve to TEST"),
            (lambda r: r.update(test_references=[]), "ADAPTED requires test"),
            (lambda r: r["license"].update(evidence_refs=["E-002"]), "VERIFIED license"),
            (lambda r: r["evidence"][2].update(kind="TEST"), "PASSED replication"),
            (lambda r: r["lifecycle_history"][4].update(evidence_refs=["E-002"]), "requires evidence kinds"),
        ]
        for mutate, message in cases:
            with self.subTest(message=message):
                catalog = fixture("valid_lifecycle.json")
                mutate(catalog["records"][0])
                self.assert_invalid(catalog, message)

    def test_claims_require_evidence_or_falsifiers(self):
        for label, message in [("FACT", "requires evidence"), ("MEASUREMENT", "requires evidence"),
                               ("INFERENCE", "requires evidence"), ("HYPOTHESIS", "requires falsifiers")]:
            with self.subTest(label=label):
                catalog = fixture()
                catalog["records"][0]["decision"]["rationale"]["epistemic_status"] = label
                self.assert_invalid(catalog, message)

    def test_source_paths_and_revision(self):
        for path in ["/tmp/source.py", "../source.py", "src/../../file", "C:\\source.py", "."]:
            with self.subTest(path=path):
                catalog = fixture("valid_lifecycle.json")
                catalog["records"][0]["source_references"][0]["path"] = path
                self.assert_invalid(catalog, "repository-relative")
        catalog = fixture("valid_lifecycle.json")
        catalog["records"][0]["source_references"][0]["commit_sha"] = "b" * 40
        self.assert_invalid(catalog, "source revision differs")

    def test_source_review_and_contract_gates(self):
        cases = [
            (lambda r: r.update(source_references=[]), "SOURCE_REVIEWED requires"),
            (lambda r: r.update(technical_mechanisms=[]), "CONTRACT_EXTRACTED requires"),
            (lambda r: r.update(assumptions=[]), "CONTRACT_EXTRACTED requires"),
            (lambda r: r.update(limitations=[]), "CONTRACT_EXTRACTED requires"),
            (lambda r: r.update(replication_status="FAILED"), "REPRODUCED requires"),
            (lambda r: r["license"].update(verification_status="UNVERIFIED"), "REPRODUCED requires"),
        ]
        for mutate, message in cases:
            with self.subTest(message=message):
                catalog = fixture("valid_lifecycle.json")
                mutate(catalog["records"][0])
                self.assert_invalid(catalog, message)

    def test_license_and_asset_support(self):
        catalog = fixture()
        catalog["records"][0]["license"]["identifier"] = "MIT"
        self.assert_invalid(catalog, "license identifier")
        catalog = fixture()
        catalog["records"][0]["applicability_across_assets"][0]["assessment"] = "SUPPORTED"
        self.assert_invalid(catalog, "requires EMPIRICAL")

    def test_history_state_and_chronology(self):
        catalog = fixture()
        record = catalog["records"][0]
        record["lifecycle_status"] = "BLOCKED"
        self.assert_invalid(catalog, "differs from last history")
        catalog = fixture("valid_lifecycle.json")
        record = catalog["records"][0]
        record["lifecycle_history"][1]["at"] = "2025-01-01T00:00:00Z"
        self.assert_invalid(catalog, "timestamps out of order")
        self.assert_invalid(catalog, "evidence recorded later")
        record["evidence"][0]["recorded_at"] = "2027-01-01T00:00:00Z"
        self.assert_invalid(catalog, "evidence postdates")

    def test_blocked_resume_and_terminal_states(self):
        catalog = fixture("valid_lifecycle.json")
        record = catalog["records"][0]
        def event(previous, target, refs=None):
            return {"from": previous, "to": target, "at": record["inspected_at"],
                    "reason": "Synthetic state test.", "evidence_refs": refs or []}
        record["lifecycle_history"] += [event("EMPIRICALLY_VALIDATED", "BLOCKED"),
                                        event("BLOCKED", "EMPIRICALLY_VALIDATED", ["E-005"])]
        self.assertEqual([], validator.validate_catalog(catalog))
        record["lifecycle_history"][-1]["to"] = record["lifecycle_status"] = "REPRODUCED"
        self.assert_invalid(catalog, "invalid lifecycle transition")
        catalog = fixture()
        record = catalog["records"][0]
        record["lifecycle_history"].append(event("DISCOVERED", "REJECTED"))
        record["lifecycle_status"] = "REJECTED"
        self.assert_invalid(catalog, "terminal decision")
        record["decision"]["status"] = "REJECT"
        self.assertEqual([], validator.validate_catalog(catalog))
        record["lifecycle_history"].append(event("REJECTED", "DISCOVERED"))
        record["lifecycle_status"] = "DISCOVERED"
        self.assert_invalid(catalog, "invalid lifecycle transition")

    def test_supersession_resolution_and_cycles(self):
        catalog = fixture()
        old = catalog["records"][0]
        new = deepcopy(old)
        new["research_id"] = "RI-0002"
        new["supersedes"] = ["RI-0001"]
        catalog["records"].append(new)
        old.update(lifecycle_status="SUPERSEDED", superseded_by="RI-0002")
        old["decision"]["status"] = "SUPERSEDE"
        old["lifecycle_history"].append({"from": "DISCOVERED", "to": "SUPERSEDED",
                                         "at": old["inspected_at"], "reason": "Synthetic replacement.", "evidence_refs": []})
        self.assertEqual([], validator.validate_catalog(catalog))
        new["supersedes"] = []
        self.assert_invalid(catalog, "reciprocally")
        new["supersedes"] = ["RI-0001"]
        new["superseded_by"] = "RI-0001"
        old["supersedes"] = ["RI-0002"]
        self.assert_invalid(catalog, "supersession cycle")

    def test_base_preserves_records_history_and_reviewed_revision(self):
        base = fixture("valid_lifecycle.json")
        self.assertEqual([], validator.validate_catalog(deepcopy(base), base))
        catalog = deepcopy(base)
        catalog["records"] = []
        self.assert_invalid(catalog, "cannot be deleted", base)
        catalog = deepcopy(base)
        catalog["records"][0]["lifecycle_history"][0]["reason"] = "Rewritten."
        self.assert_invalid(catalog, "history is immutable", base)
        catalog = deepcopy(base)
        record = catalog["records"][0]
        record["upstream_commit_sha"] = record["source_references"][0]["commit_sha"] = "b" * 40
        self.assert_invalid(catalog, "provenance is immutable", base)
        self.assert_invalid(base, "base invalid", {})

    def test_base_accepts_valid_promotion(self):
        self.assertEqual([], validator.validate_catalog(fixture("valid_lifecycle.json"), fixture()))

    def test_base_preserves_evidence(self):
        base = fixture("valid_lifecycle.json")
        catalog = deepcopy(base)
        catalog["records"][0]["evidence"][0]["summary"] = "Rewritten observation."
        self.assert_invalid(catalog, "prior evidence is immutable", base)

    def test_identifiers_reject_trailing_newline(self):
        for field, value in [("research_id", "RI-0001\n"), ("upstream_commit_sha", "a" * 40 + "\n")]:
            with self.subTest(field=field):
                catalog = fixture()
                catalog["records"][0][field] = value
                self.assert_invalid(catalog, "invalid string format")

    def test_json_rejects_ambiguous_inputs(self):
        for text in ['{"records": [], "records": []}', '{"x": NaN}', '{', '{"x": Infinity}']:
            with self.subTest(text=text), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "bad.json"
                path.write_text(text)
                with self.assertRaises(ValueError):
                    validator.load_json(path)

    def test_schema_fails_closed_on_new_keywords(self):
        schema = validator.load_schema()
        schema["properties"]["records"]["contains"] = {"type": "object"}
        with patch.object(validator, "load_json", return_value=schema):
            with self.assertRaisesRegex(ValueError, "unsupported schema keywords"):
                validator.load_schema()

    def test_cli_exit_statuses_and_offline_operation(self):
        for name, expected in [("valid_unknown.json", 0), ("valid_lifecycle.json", 0),
                               ("invalid_transition.json", 1), ("missing.json", 1)]:
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, "-m", "tools.validate_catalog", str(FIXTURES / name)],
                                        cwd=validator.ROOT, capture_output=True, text=True)
                self.assertEqual(expected, result.returncode, result.stderr)
                self.assertIn("PASS:" if expected == 0 else "FAIL:", result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
        with patch("socket.socket", side_effect=AssertionError("network forbidden")):
            self.assertEqual([], validator.validate_catalog(fixture("valid_lifecycle.json")))


if __name__ == "__main__":
    unittest.main()
