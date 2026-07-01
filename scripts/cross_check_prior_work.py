#!/usr/bin/env python3
"""Compare the live-generated OKF bundle against older local notes.

This script is intentionally separate from generation. It checks prior local
evidence after the live BigQuery bundle exists.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-check generated OKF against prior local evidence.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--prior-table-inventory", type=Path, help="Optional CSV with a table_schema column for count comparison.")
    parser.add_argument("--out", type=Path, default=Path("reports/prior_work_cross_check.md"))
    args = parser.parse_args()

    summary_path = args.bundle / "_source_metadata" / "source_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    prior_rows = []
    if args.prior_table_inventory and args.prior_table_inventory.exists():
        with args.prior_table_inventory.open(newline="", encoding="utf-8") as handle:
            prior_rows = list(csv.DictReader(handle))

    live_counts = {ds["dataset_id"]: ds["object_count"] for ds in summary["datasets"]}
    prior_counts: dict[str, int] = {}
    for row in prior_rows:
        prior_counts[row["table_schema"]] = prior_counts.get(row["table_schema"], 0) + 1

    lines = [
        "# Prior Work Cross-check",
        "",
        "This report compares the live-generated OKF source summary against older local UltraCart warehouse evidence. It is not a generation input.",
        "",
        "## Counts",
        "",
        "| Dataset | Live OKF objects | Prior evidence objects | Status |",
        "|---|---:|---:|---|",
    ]
    for dataset in sorted(set(live_counts) | set(prior_counts)):
        live = live_counts.get(dataset, 0)
        prior = prior_counts.get(dataset, 0)
        status = "match" if live == prior else "diff"
        lines.append(f"| `{dataset}` | {live} | {prior} | {status} |")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Differences are not automatically errors; BigQuery may have changed since the prior evidence was captured.",
            "- Use this report to focus human review after the BigQuery-first OKF bundle validates.",
        ]
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
