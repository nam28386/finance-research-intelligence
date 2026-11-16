"""Offline Phase 02A release gate; does not query or verify upstream sources."""

import argparse
from pathlib import Path
import sys

from tools.validate_catalog import ROOT, load_json, validate_catalog


def discovery_errors(catalog):
    """Keep this release DISCOVERED and prevent repeated repository identities."""
    errors = validate_catalog(catalog)
    if errors:
        return errors
    seen = set()
    for record in catalog["records"]:
        rid = record["research_id"]
        url = record["repository_url"].casefold()
        if url in seen:
            errors.append(f"{rid}: duplicate repository URL")
        seen.add(url)
        history = record["lifecycle_history"]
        if (record["lifecycle_status"] != "DISCOVERED" or len(history) != 1
                or history[0]["from"] is not None or history[0]["to"] != "DISCOVERED"):
            errors.append(f"{rid}: Phase 02A records must remain DISCOVERED")
        if record["source_references"] or record["technical_mechanisms"] or record["test_references"]:
            errors.append(f"{rid}: Phase 02A does not record source-reviewed findings")
    return sorted(errors)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", nargs="?", type=Path, default=ROOT / "research/catalog.json")
    args = parser.parse_args(argv)
    try:
        errors = discovery_errors(load_json(args.catalog))
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: Phase 02A discovery gate: {args.catalog}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
