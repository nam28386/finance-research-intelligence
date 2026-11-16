"""Phase 02A release checks with offline synthetic fixtures."""

from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import unittest

from tools.validate_catalog import ROOT, load_json, validate_catalog
from tools.validate_discovery import discovery_errors

FIXTURES = Path(__file__).parent / "fixtures"


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.fixture = load_json(FIXTURES / "valid_unknown.json")

    def test_unknown_revision_and_license_are_valid(self):
        self.assertEqual([], discovery_errors(self.fixture))
        record = self.fixture["records"][0]
        self.assertIsNone(record["upstream_commit_sha"])
        self.assertEqual("UNKNOWN", record["license"]["verification_status"])

    def test_rejects_duplicate_repository_case_insensitively(self):
        other = deepcopy(self.fixture["records"][0])
        other["research_id"] = "RI-0002"
        other["repository_url"] = other["repository_url"].replace("synthetic-example", "Synthetic-Example")
        self.fixture["records"].append(other)
        self.assertTrue(any("duplicate repository URL" in e for e in discovery_errors(self.fixture)))

    def test_no_scientific_promotion(self):
        promoted = load_json(FIXTURES / "valid_lifecycle.json")
        self.assertEqual([], validate_catalog(promoted))
        self.assertTrue(any("must remain DISCOVERED" in e for e in discovery_errors(promoted)))

    def test_rejects_source_findings_in_discovery(self):
        record = self.fixture["records"][0]
        record["technical_mechanisms"] = [deepcopy(record["decision"]["rationale"])]
        self.assertTrue(any("source-reviewed findings" in e for e in discovery_errors(self.fixture)))

    def test_prior_empty_catalog_is_compatible(self):
        base = {"schema_version": "0.1.0", "records": []}
        self.assertEqual([], validate_catalog(self.fixture, base))

    def test_ten_synthetic_discoveries(self):
        catalog = {"schema_version": "0.1.0", "records": []}
        for i in range(1, 11):
            record = deepcopy(self.fixture["records"][0])
            record["research_id"] = f"RI-{i:04d}"
            record["repository_url"] = f"https://github.com/synthetic-example/fixture-{i}"
            catalog["records"].append(record)
        self.assertTrue(all(record["synthetic"] for record in catalog["records"]))
        self.assertEqual([], discovery_errors(catalog))

    def test_cli_rejects_promoted_fixture(self):
        result = subprocess.run([sys.executable, "-m", "tools.validate_discovery",
                                 str(FIXTURES / "valid_lifecycle.json")],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(1, result.returncode)
        self.assertIn("must remain DISCOVERED", result.stderr)


if __name__ == "__main__":
    unittest.main()
