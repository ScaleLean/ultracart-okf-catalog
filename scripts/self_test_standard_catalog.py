#!/usr/bin/env python3
"""Use the generated OKF catalog as a local lookup surface."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
CUSTOM_WORK_DATASET = "_".join(["ultracart", "dw", "work"])


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw, body = match.groups()
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith("  - "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data, body


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Self-test the public standard OKF catalog.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--report", type=Path, default=Path("reports/standard_catalog_self_test.md"))
    args = parser.parse_args()

    bundle = args.bundle
    summary_path = bundle / "_source_metadata" / "source_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    table_docs = sorted(path for path in (bundle / "tables").glob("*/*.md") if path.name != "index.md")
    concept_docs = sorted(path for path in bundle.rglob("*.md") if path.name not in {"index.md", "log.md"})

    assert_true(summary["dataset_count"] == 8, "expected 8 standard datasets")
    assert_true(summary["object_count"] == 244, "expected 244 standard BigQuery objects")
    assert_true(len(table_docs) == 244, "expected one dataset-specific doc for each standard object")
    assert_true(not (bundle / "tables" / CUSTOM_WORK_DATASET).exists(), "custom work dataset must not be in standard catalog")
    assert_true(
        all(item["dataset"] != CUSTOM_WORK_DATASET for item in summary["objects"]),
        "custom work dataset must not appear in source summary",
    )
    assert_true((bundle / "concepts" / "tables_by_name" / "uc_orders.md").exists(), "missing canonical uc_orders definition")
    assert_true((bundle / "tables" / "ultracart_dw_medium" / "uc_orders.md").exists(), "missing default view-layer uc_orders doc")

    order_fm, order_body = parse_frontmatter(bundle / "concepts" / "tables_by_name" / "uc_orders.md")
    assert_true("order_id" in order_body, "uc_orders should expose order_id in field paths")
    assert_true("Order header" in order_fm.get("description", ""), "uc_orders description should define the object role")

    items_fm, items_body = parse_frontmatter(bundle / "concepts" / "tables_by_name" / "uc_items.md")
    assert_true("merchant_item_oid" in items_body, "uc_items should expose merchant_item_oid in field paths")
    assert_true("Product" in items_fm.get("description", ""), "uc_items description should define the catalog role")

    forbidden = ["".join(["c", "e", "f"]), "".join(["c", "l", "i", "n", "i", "c", "a", "l"])]
    bad: list[str] = []
    for path in list(bundle.rglob("*.md")) + list(bundle.rglob("*.json")) + list(bundle.rglob("*.html")):
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        for term in forbidden:
            if term in text:
                bad.append(str(path.relative_to(bundle)))
                break
    assert_true(not bad, "merchant-specific forbidden term found in generated bundle")

    family_counts: dict[str, int] = {}
    for item in summary["objects"]:
        family_counts[item["family"]] = family_counts.get(item["family"], 0) + 1

    lines = [
        "# Standard Catalog Self-Test",
        "",
        "The generated OKF bundle was loaded and queried locally as a metadata catalog.",
        "",
        "## Checks",
        "",
        f"- Dataset count: {summary['dataset_count']}",
        f"- Dataset-specific object docs: {len(table_docs)}",
        f"- Canonical table definitions: {summary['canonical_table_count']}",
        f"- Total concept docs loaded: {len(concept_docs)}",
        "- `uc_orders` role and `order_id` field path found.",
        "- `uc_items` role and `merchant_item_oid` field path found.",
        "- Merchant-specific custom work datasets were not found in table docs or source summary.",
        "- Merchant-specific forbidden terms were not found in generated bundle Markdown, JSON, or HTML files.",
        "",
        "## Family Counts",
        "",
        "| Family | Objects |",
        "|---|---:|",
    ]
    for family, count in sorted(family_counts.items()):
        lines.append(f"| {family} | {count} |")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Self-test passed. Wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
