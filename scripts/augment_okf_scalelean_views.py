#!/usr/bin/env python3
"""Augment an UltraCart OKF bundle with live downstream BigQuery views.

This is a post-generation augmentation. It uses live BigQuery metadata from
`INFORMATION_SCHEMA.VIEWS` and `INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`, parses
view definitions only to infer dependencies, and never writes full SQL text into
the OKF bundle.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from typing import Any


UTC = dt.timezone.utc
SENSITIVE_FIELD_RE = re.compile(
    r"(email|address|phone|payment|card|cvv|token|password|secret|ip_address|"
    r"customer|billing|shipping|conversation|transcript|media|payload)",
    re.I,
)
RELEVANT_VIEW_RE = re.compile(r"(ultracart|`?uc_[A-Za-z0-9_]+|src_uc|stg_uc|z_imp_uc)", re.I)
TABLE_REF_RE = re.compile(r"`([A-Za-z0-9_-]+)\.([A-Za-z0-9_]+)\.([A-Za-z0-9_*.-]+)`")


def run_bq_json(args: list[str]) -> Any:
    cmd = ["bq", "--format=json", *args]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "BigQuery command failed:\n"
            f"  {' '.join(cmd)}\n"
            f"stderr:\n{proc.stderr.strip()}"
        )
    text = proc.stdout.strip()
    if not text:
        return None
    return json.loads(text)


def run_query(sql: str, billing_project: str) -> list[dict[str, Any]]:
    return run_bq_json(
        [
            "query",
            "--nouse_legacy_sql",
            "--max_rows=1000000",
            "--project_id",
            billing_project,
            sql,
        ]
    ) or []


def bq_resource(project: str, dataset: str | None = None, table: str | None = None) -> str:
    base = f"https://bigquery.googleapis.com/v2/projects/{project}"
    if dataset is None:
        return base
    if table is None:
        return f"{base}/datasets/{dataset}"
    return f"{base}/datasets/{dataset}/tables/{table}"


def safe_slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")
    return cleaned or "unnamed"


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def yaml_quote(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = ("" if value is None else str(value)).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def write_doc(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_quote(item)}")
        else:
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_plain(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def bundle_source_project(bundle: Path) -> str | None:
    summary_path = bundle / "_source_metadata" / "source_summary.json"
    if not summary_path.exists():
        return None
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    source_project = summary.get("source_project")
    return str(source_project) if source_project else None


def link_for_source_ref(bundle: Path, source_project: str | None, project: str, dataset: str, table: str) -> str | None:
    if "*" in table:
        return None
    if source_project:
        if project != source_project:
            return None
    elif not project.startswith("ultracart-dw"):
        return None
    candidate = bundle / "tables" / safe_slug(dataset) / f"{safe_slug(table)}.md"
    if candidate.exists():
        return f"/tables/{safe_slug(dataset)}/{safe_slug(table)}.md"
    return None


def link_for_downstream_view(dataset: str, view: str) -> str:
    return f"/downstream_views/scale-lean/{safe_slug(dataset)}/{safe_slug(view)}.md"


def field_count(fields: list[dict[str, Any]]) -> int:
    return len({row.get("field_path") or row.get("column_name") for row in fields})


def sensitivity_for_fields(fields: list[dict[str, Any]]) -> tuple[str, list[str]]:
    hits = sorted(
        {
            str(row.get("field_path") or row.get("column_name") or "")
            for row in fields
            if SENSITIVE_FIELD_RE.search(str(row.get("field_path") or row.get("column_name") or ""))
        }
    )
    if hits:
        return "restricted_metadata_only", hits
    return "standard_metadata", []


def schema_markdown(fields: list[dict[str, Any]]) -> str:
    if not fields:
        return "_No field metadata was returned for this view._"
    rows = []
    seen: set[str] = set()
    for row in fields:
        field_path = row.get("field_path") or row.get("column_name") or ""
        if not field_path or field_path in seen:
            continue
        seen.add(field_path)
        rows.append(
            "| `{}` | {} | {} |".format(
                md_escape(field_path),
                md_escape(row.get("data_type") or ""),
                md_escape(row.get("description") or ""),
            )
        )
    return "\n".join(["| Field path | Type | Description |", "|---|---|---|", *rows])


def discover_datasets(project: str) -> list[str]:
    rows = run_bq_json(["ls", "--max_results=10000", "--project_id", project]) or []
    return sorted(row["datasetReference"]["datasetId"] for row in rows)


def discover_views(project: str, dataset: str, billing_project: str) -> tuple[list[dict[str, Any]], str | None]:
    try:
        views = run_query(
            f"""
            SELECT
              table_name,
              view_definition,
              check_option,
              use_standard_sql
            FROM `{project}.{dataset}.INFORMATION_SCHEMA.VIEWS`
            ORDER BY table_name
            """,
            billing_project,
        )
        fields = run_query(
            f"""
            SELECT
              table_name,
              field_path,
              data_type,
              description
            FROM `{project}.{dataset}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`
            ORDER BY table_name, field_path
            """,
            billing_project,
        )
    except RuntimeError as exc:
        return [], str(exc)

    fields_by_view: dict[str, list[dict[str, Any]]] = {}
    for row in fields:
        fields_by_view.setdefault(row["table_name"], []).append(row)

    relevant: list[dict[str, Any]] = []
    for view in views:
        definition = view.get("view_definition") or ""
        if not RELEVANT_VIEW_RE.search(definition) and not RELEVANT_VIEW_RE.search(view["table_name"]):
            continue
        refs = sorted(set(TABLE_REF_RE.findall(definition)))
        relevant.append(
            {
                "project": project,
                "dataset": dataset,
                "view": view["table_name"],
                "fields": fields_by_view.get(view["table_name"], []),
                "refs": [
                    {"project": ref[0], "dataset": ref[1], "table": ref[2]}
                    for ref in refs
                ],
                "uses_standard_sql": view.get("use_standard_sql"),
            }
        )
    return relevant, None


def write_project_doc(bundle: Path, project: str, generated_at: str, views: list[dict[str, Any]]) -> None:
    datasets = sorted({view["dataset"] for view in views})
    body = [
        f"`{project}` is the downstream BigQuery project reviewed for UltraCart-consuming views.",
        "",
        "This OKF concept was created from live BigQuery view metadata. Full view SQL is not stored; dependencies are parsed into links and reference tables.",
        "",
        "# Downstream Coverage",
        "",
        f"- Relevant views discovered: `{len(views)}`",
        f"- Datasets with relevant views: `{len(datasets)}`",
        "",
        "# Datasets",
        "",
    ]
    for dataset in datasets:
        count = sum(1 for view in views if view["dataset"] == dataset)
        body.append(f"- [`{dataset}`](/downstream_views/scale-lean/{safe_slug(dataset)}/) - {count} relevant views")
    body.extend(["", "# Citations", "", f"[1] [BigQuery project resource]({bq_resource(project)})"])
    write_doc(
        bundle / "projects" / f"{safe_slug(project)}.md",
        {
            "type": "BigQuery Downstream Project",
            "title": project,
            "description": f"Downstream BigQuery project with {len(views)} UltraCart-relevant views discovered from live metadata.",
            "resource": bq_resource(project),
            "tags": ["scale-lean", "bigquery", "downstream-views", "ultracart", "okf"],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/augment_okf_scalelean_views.py",
            "source_project": project,
            "relationship_to_bundle": "downstream_consumer",
        },
        "\n".join(body),
    )


def write_view_doc(bundle: Path, view: dict[str, Any], generated_at: str, source_project: str | None) -> None:
    project = view["project"]
    dataset = view["dataset"]
    view_name = view["view"]
    fields = view["fields"]
    refs = view["refs"]
    sensitivity, sensitive_fields = sensitivity_for_fields(fields)
    ultracart_refs = [ref for ref in refs if ref["project"].startswith("ultracart-dw")]
    source_links = [
        (ref, link_for_source_ref(bundle, source_project, ref["project"], ref["dataset"], ref["table"]))
        for ref in refs
    ]
    linked_ultracart = [item for item in source_links if item[1]]

    body = [
        f"`{project}.{dataset}.{view_name}` is a downstream BigQuery view discovered from live `scale-lean` metadata.",
        "",
        "It is included because its view definition or name references UltraCart-style objects. The OKF bundle records schema and dependency relationships only; full SQL text is intentionally omitted.",
        "",
        "# Role In The OKF Bundle",
        "",
        "This concept enriches the upstream UltraCart catalog by showing downstream consumption, staging, canonical, audit, or reporting surfaces in `scale-lean`.",
        "",
        "# BigQuery Metadata",
        "",
        f"- Resource: `{bq_resource(project, dataset, view_name)}`",
        f"- Field count: `{field_count(fields)}`",
        f"- Sensitivity: `{sensitivity}`",
        f"- Uses standard SQL: `{view.get('uses_standard_sql')}`",
        f"- Parsed BigQuery references: `{len(refs)}`",
        f"- Parsed UltraCart project references: `{len(ultracart_refs)}`",
        f"- Linked upstream OKF UltraCart concepts: `{len(linked_ultracart)}`",
        "",
        "# Schema",
        "",
        schema_markdown(fields),
        "",
        "# Parsed Dependencies",
        "",
    ]
    if not refs:
        body.append("_No fully qualified backtick BigQuery table references were parsed from the live view definition._")
    else:
        body.append("| Reference | OKF link |")
        body.append("|---|---|")
        for ref, link in source_links:
            label = f"{ref['project']}.{ref['dataset']}.{ref['table']}"
            okf_link = f"[source concept]({link})" if link else "not in current upstream bundle"
            body.append(f"| `{md_escape(label)}` | {okf_link} |")
    body.extend(["", "# Sensitivity Notes", ""])
    if sensitive_fields:
        shown = ", ".join(f"`{field}`" for field in sensitive_fields[:30])
        more = f" and {len(sensitive_fields) - 30} more" if len(sensitive_fields) > 30 else ""
        body.append(f"Sensitive-looking field names were detected in metadata: {shown}{more}. Treat this concept as metadata-only.")
    else:
        body.append("No sensitive-looking field names were detected by the generator's conservative name scan.")
    body.extend(
        [
            "",
            "# Common Query Patterns",
            "",
            "Metadata-only inspection:",
            "",
            "```sql",
            "SELECT column_name, data_type",
            f"FROM `{project}.{dataset}.INFORMATION_SCHEMA.COLUMNS`",
            f"WHERE table_name = '{view_name}'",
            "ORDER BY ordinal_position;",
            "```",
            "",
            "# Citations",
            "",
            f"[1] [BigQuery view resource]({bq_resource(project, dataset, view_name)})",
        ]
    )
    write_doc(
        bundle / "downstream_views" / "scale-lean" / safe_slug(dataset) / f"{safe_slug(view_name)}.md",
        {
            "type": "BigQuery Downstream View",
            "title": f"{dataset}.{view_name}",
            "description": f"Scale Lean downstream view with {field_count(fields)} fields and {len(refs)} parsed dependencies.",
            "resource": bq_resource(project, dataset, view_name),
            "tags": ["scale-lean", "bigquery", "downstream-view", "ultracart", dataset, view_name, sensitivity],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/augment_okf_scalelean_views.py",
            "source_project": project,
            "source_dataset": dataset,
            "source_table": view_name,
            "source_object_type": "VIEW",
            "relationship_to_bundle": "downstream_consumer",
            "sensitivity": sensitivity,
            "field_count": field_count(fields),
            "parsed_dependency_count": len(refs),
            "linked_upstream_concept_count": len(linked_ultracart),
        },
        "\n".join(body),
    )


def write_indexes(bundle: Path, generated_at: str, views: list[dict[str, Any]], inaccessible: dict[str, str]) -> None:
    root = bundle / "downstream_views" / "scale-lean"
    datasets = sorted({view["dataset"] for view in views})
    lines = [
        "# scale-lean Downstream Views",
        "",
        "This directory contains OKF concepts for live `scale-lean` BigQuery views that reference UltraCart-style sources. View SQL is parsed for dependencies but not stored.",
        "",
        f"- Generated at: `{generated_at}`",
        f"- Relevant views: `{len(views)}`",
        f"- Datasets with relevant views: `{len(datasets)}`",
        "",
        "## Datasets",
        "",
    ]
    for dataset in datasets:
        count = sum(1 for view in views if view["dataset"] == dataset)
        lines.append(f"- [`{dataset}`]({safe_slug(dataset)}/) - {count} views")
    if inaccessible:
        lines.extend(["", "## Inaccessible Or Failed Datasets", ""])
        for dataset in sorted(inaccessible):
            lines.append(f"- `{dataset}`")
    write_plain(root / "index.md", "\n".join(lines))

    for dataset in datasets:
        ds_views = sorted([view for view in views if view["dataset"] == dataset], key=lambda item: item["view"].lower())
        ds_lines = [f"# {dataset} Downstream Views", ""]
        for view in ds_views:
            ds_lines.append(f"- [{view['view']}]({safe_slug(view['view'])}.md) - {field_count(view['fields'])} fields")
        write_plain(root / safe_slug(dataset) / "index.md", "\n".join(ds_lines))

    ref_lines = [
        "This concept summarizes the live `scale-lean` downstream-view augmentation.",
        "",
        "# Summary",
        "",
        f"- Relevant views discovered: `{len(views)}`",
        f"- Datasets with relevant views: `{len(datasets)}`",
        f"- Datasets skipped or failed: `{len(inaccessible)}`",
        "",
        "# Dataset Counts",
        "",
        "| Dataset | Relevant views |",
        "|---|---:|",
    ]
    for dataset in datasets:
        ref_lines.append(f"| [`{dataset}`](/downstream_views/scale-lean/{safe_slug(dataset)}/) | {sum(1 for view in views if view['dataset'] == dataset)} |")
    if inaccessible:
        ref_lines.extend(["", "# Inaccessible Or Failed Datasets", ""])
        for dataset, error in sorted(inaccessible.items()):
            ref_lines.append(f"- `{dataset}` - metadata query failed; see sanitized metadata report.")
    ref_lines.extend(["", "# Citations", "", "[1] [BigQuery project resource](https://bigquery.googleapis.com/v2/projects/scale-lean)"])
    write_doc(
        bundle / "references" / "scale_lean_downstream_views.md",
        {
            "type": "Downstream View Relationship Map",
            "title": "scale-lean Downstream Views",
            "description": f"Live scale-lean BigQuery views that reference UltraCart-style sources and enrich the upstream OKF bundle.",
            "resource": bq_resource("scale-lean"),
            "tags": ["scale-lean", "downstream-views", "relationships", "ultracart", "okf"],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/augment_okf_scalelean_views.py",
            "source_project": "scale-lean",
            "relationship_to_bundle": "downstream_consumer",
        },
        "\n".join(ref_lines),
    )


def update_root_indexes(bundle: Path) -> None:
    root_index = bundle / "index.md"
    text = root_index.read_text(encoding="utf-8")
    line = "* [scale-lean downstream views](downstream_views/scale-lean/) - Live downstream BigQuery views that reference UltraCart-style sources."
    if line not in text:
        text = text.rstrip() + "\n" + line + "\n"
        root_index.write_text(text, encoding="utf-8")

    projects_index = bundle / "projects" / "index.md"
    text = projects_index.read_text(encoding="utf-8")
    line = "* [scale-lean](scale-lean.md) - Downstream project containing UltraCart-consuming views."
    if line not in text:
        projects_index.write_text(text.rstrip() + "\n" + line + "\n", encoding="utf-8")

    refs_index = bundle / "references" / "index.md"
    text = refs_index.read_text(encoding="utf-8")
    line = "* [scale-lean Downstream Views](scale_lean_downstream_views.md) - Live downstream views and parsed upstream relationships."
    if line not in text:
        refs_index.write_text(text.rstrip() + "\n" + line + "\n", encoding="utf-8")


def write_source_metadata(bundle: Path, generated_at: str, views: list[dict[str, Any]], inaccessible: dict[str, str]) -> None:
    serializable = {
        "generated_at": generated_at,
        "source_project": "scale-lean",
        "relevant_view_count": len(views),
        "dataset_count": len({view["dataset"] for view in views}),
        "views": [
            {
                "dataset": view["dataset"],
                "view": view["view"],
                "field_count": field_count(view["fields"]),
                "parsed_refs": view["refs"],
            }
            for view in sorted(views, key=lambda item: (item["dataset"], item["view"]))
        ],
        "inaccessible_or_failed_datasets": inaccessible,
        "policy": {
            "view_definition_stored": False,
            "row_sampling": False,
            "raw_values": False,
        },
    }
    path = bundle / "_source_metadata" / "scale_lean_downstream_views.json"
    path.write_text(json.dumps(serializable, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Augment an OKF bundle with scale-lean downstream views.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--project", default="scale-lean")
    parser.add_argument("--billing-project", help="Billing project for metadata queries. Defaults to --project.")
    parser.add_argument("--dataset", action="append", help="Optional dataset allowlist; may be repeated.")
    args = parser.parse_args()

    generated_at = dt.datetime.now(UTC).isoformat(timespec="seconds")
    billing_project = args.billing_project or args.project
    source_project = bundle_source_project(args.bundle)
    datasets = sorted(args.dataset or discover_datasets(args.project))
    all_views: list[dict[str, Any]] = []
    inaccessible: dict[str, str] = {}
    for dataset in datasets:
        views, error = discover_views(args.project, dataset, billing_project)
        if error:
            inaccessible[dataset] = error.splitlines()[-1][:300]
            continue
        all_views.extend(views)

    # Rebuild augmentation output only.
    downstream_root = args.bundle / "downstream_views" / "scale-lean"
    if downstream_root.exists():
        for child in sorted(downstream_root.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()

    write_project_doc(args.bundle, args.project, generated_at, all_views)
    for view in all_views:
        write_view_doc(args.bundle, view, generated_at, source_project)
    write_indexes(args.bundle, generated_at, all_views, inaccessible)
    update_root_indexes(args.bundle)
    write_source_metadata(args.bundle, generated_at, all_views, inaccessible)

    viewer_script = Path(__file__).resolve().parent / "build_okf_viewer.py"
    subprocess.run([str(viewer_script), str(args.bundle)], check=True)
    print(
        f"Augmented {args.bundle} with {len(all_views)} scale-lean downstream views "
        f"across {len({view['dataset'] for view in all_views})} datasets."
    )
    if inaccessible:
        print(f"Skipped or failed datasets: {len(inaccessible)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
