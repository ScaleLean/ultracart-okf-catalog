#!/usr/bin/env python3
"""Render and dry-run reference BigQuery view SQL."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_VIEW_DIR = Path("examples/bigquery_views")


def render_sql(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{ " + key + " }}", value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run templated example view SQL against BigQuery.")
    parser.add_argument("--source-project", required=True)
    parser.add_argument("--access-dataset", default="ultracart_dw_medium")
    parser.add_argument("--billing-project", required=True)
    parser.add_argument("--target-project", default="example_project")
    parser.add_argument("--target-dataset", default="example_dataset")
    parser.add_argument("--lookback-days", default="365")
    parser.add_argument("--time-zone", default="America/New_York")
    parser.add_argument("--search-text", default="example")
    parser.add_argument("--bq-region", default="us")
    parser.add_argument("--cost-start-date", default="2026-01-01")
    parser.add_argument("--cost-end-date", default="2026-02-01")
    parser.add_argument("--view-dir", type=Path, default=DEFAULT_VIEW_DIR)
    parser.add_argument("--include-marts", action="store_true", help="Also dry-run mart files that depend on rendered base views existing in target_dataset.")
    parser.add_argument("--include-docs", action="store_true", help="Also dry-run public-docs-inspired query examples.")
    parser.add_argument("--include-ops", action="store_true", help="Also dry-run BigQuery operations examples such as INFORMATION_SCHEMA cost checks.")
    args = parser.parse_args()

    values = {
        "source_project": args.source_project,
        "access_dataset": args.access_dataset,
        "billing_project": args.billing_project,
        "target_project": args.target_project,
        "target_dataset": args.target_dataset,
        "lookback_days": args.lookback_days,
        "time_zone": args.time_zone,
        "search_text": args.search_text,
        "bq_region": args.bq_region,
        "cost_start_date": args.cost_start_date,
        "cost_end_date": args.cost_end_date,
    }

    failures: list[str] = []
    prefixes = ["base_"]
    if args.include_marts:
        prefixes.append("mart_")
    if args.include_docs:
        prefixes.append("docs_")
    if args.include_ops:
        prefixes.append("ops_")
    sql_files = sorted(
        path for path in args.view_dir.glob("*.sql")
        if any(path.name.startswith(prefix) for prefix in prefixes)
    )
    if not sql_files:
        print(f"No SQL files found in {args.view_dir}", file=sys.stderr)
        return 1

    for source in sql_files:
        rendered = render_sql(source.read_text(encoding="utf-8"), values)
        cmd = [
            "bq",
            "query",
            f"--project_id={args.billing_project}",
            "--use_legacy_sql=false",
            "--dry_run",
        ]
        result = subprocess.run(cmd, input=rendered, text=True, capture_output=True, check=False)
        if result.returncode == 0:
            print(f"PASS {source.name}")
        else:
            print(f"FAIL {source.name}", file=sys.stderr)
            print(result.stderr.strip(), file=sys.stderr)
            failures.append(source.name)

    if failures:
        print(f"{len(failures)} dry-run failure(s): {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
