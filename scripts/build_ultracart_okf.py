#!/usr/bin/env python3
"""Build an OKF bundle from live UltraCart BigQuery metadata.

This generator intentionally uses metadata commands only:

- bq ls
- BigQuery INFORMATION_SCHEMA metadata views

It does not query table rows, sample data, or include full view SQL in the
generated bundle.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
UTC = dt.timezone.utc
SENSITIVE_FIELD_RE = re.compile(
    r"(email|address|phone|payment|card|cvv|token|password|secret|ip_address|"
    r"customer|billing|shipping|conversation|transcript|media|payload)",
    re.I,
)
RAW_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def load_config(path: Path) -> dict[str, Any]:
    """Small YAML subset parser for this project's config file."""
    data: dict[str, Any] = {}
    current: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                data[key] = parse_scalar(value)
                current = None
            else:
                data[key] = []
                current = key
            continue
        if current is None:
            continue
        if line.startswith("- "):
            if not isinstance(data.get(current), list):
                data[current] = []
            data[current].append(parse_scalar(line[2:]))
            continue
        if ":" in line:
            if not isinstance(data.get(current), dict):
                data[current] = {}
            key, value = line.split(":", 1)
            data[current][key.strip()] = parse_scalar(value)
    return data


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
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"BigQuery command did not return JSON: {' '.join(cmd)}\n{text[:500]}"
        ) from exc


def run_bq_metadata_query(sql: str, billing_project: str | None, fallback_project: str) -> list[dict[str, Any]]:
    result = run_bq_json(
        [
            "query",
            "--nouse_legacy_sql",
            "--max_rows=1000000",
            "--project_id",
            billing_project or fallback_project,
            sql,
        ]
    )
    return result or []


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
    text = "" if value is None else str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
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


def flatten_schema(fields: list[dict[str, Any]], prefix: str = "") -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for field in fields:
        name = field.get("name", "")
        path = f"{prefix}.{name}" if prefix else name
        rows.append(
            {
                "field_path": path,
                "type": field.get("type", ""),
                "mode": field.get("mode", ""),
                "description": field.get("description", ""),
            }
        )
        children = field.get("fields") or []
        if children:
            rows.extend(flatten_schema(children, path))
    return rows


def field_count(fields: list[dict[str, Any]]) -> int:
    return len(flatten_schema(fields))


def sensitivity_for_fields(fields: list[dict[str, Any]]) -> tuple[str, list[str]]:
    flattened = flatten_schema(fields)
    hits = sorted(
        {
            row["field_path"]
            for row in flattened
            if SENSITIVE_FIELD_RE.search(row["field_path"])
        }
    )
    if hits:
        return "restricted_metadata_only", hits
    return "standard_metadata", []


def sanitize_table_metadata(meta: dict[str, Any]) -> dict[str, Any]:
    keep_keys = {
        "kind",
        "id",
        "selfLink",
        "tableReference",
        "type",
        "creationTime",
        "lastModifiedTime",
        "description",
        "friendlyName",
        "labels",
        "schema",
        "numBytes",
        "numLongTermBytes",
        "numRows",
        "timePartitioning",
        "rangePartitioning",
        "clustering",
        "materializedView",
        "location",
        "expirationTime",
    }
    sanitized = {key: meta[key] for key in keep_keys if key in meta}
    if "view" in meta:
        view = dict(meta.get("view") or {})
        view.pop("query", None)
        sanitized["view"] = view
        sanitized["view_sql_omitted"] = True
    return sanitized


def sanitize_dataset_metadata(meta: dict[str, Any]) -> dict[str, Any]:
    keep_keys = {
        "kind",
        "id",
        "selfLink",
        "datasetReference",
        "location",
        "creationTime",
        "lastModifiedTime",
        "description",
        "friendlyName",
        "labels",
        "defaultTableExpirationMs",
        "defaultPartitionExpirationMs",
    }
    return {key: redact_raw_emails(meta[key]) for key in keep_keys if key in meta}


def redact_raw_emails(value: Any) -> Any:
    if isinstance(value, str):
        return RAW_EMAIL_RE.sub("[redacted-email]", value)
    if isinstance(value, list):
        return [redact_raw_emails(item) for item in value]
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            if key == "access":
                continue
            redacted[key] = redact_raw_emails(item)
        return redacted
    return value


def normalize_table_type(value: str | None) -> str:
    raw = (value or "TABLE").upper().replace(" ", "_")
    if raw in {"BASE_TABLE", "TABLE"}:
        return "TABLE"
    if raw in {"MATERIALIZED_VIEW", "MATERIALIZED_VIEW_REPLICA"}:
        return "MATERIALIZED_VIEW"
    if raw in {"EXTERNAL", "EXTERNAL_TABLE"}:
        return "EXTERNAL"
    if raw == "VIEW":
        return "VIEW"
    return raw


def fields_from_column_field_paths(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    fields: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        field_path = row.get("field_path") or row.get("column_name") or ""
        if not field_path or field_path in seen:
            continue
        seen.add(field_path)
        fields.append(
            {
                "name": field_path,
                "type": row.get("data_type") or "",
                "mode": "NULLABLE" if row.get("is_nullable") == "YES" else "",
                "description": row.get("description") or "",
            }
        )
    return fields


def discover_metadata(project: str, billing_project: str | None, allowlist: list[str]) -> dict[str, Any]:
    datasets_raw = run_bq_json(["ls", "--max_results=10000", "--project_id", project])
    datasets: list[dict[str, Any]] = []
    allow = {item for item in allowlist if item}
    for ds in datasets_raw or []:
        dataset_id = ds["datasetReference"]["datasetId"]
        if allow and dataset_id not in allow:
            continue
        ds_ref = f"{project}:{dataset_id}"
        ds_show = sanitize_dataset_metadata(
            run_bq_json(["show", "--project_id", billing_project or project, ds_ref])
        )
        tables_meta = run_bq_metadata_query(
            f"""
            SELECT
              table_name,
              table_type,
              creation_time,
              base_table_catalog,
              base_table_schema,
              base_table_name,
              default_collation_name,
              snapshot_time_ms,
              upsert_stream_apply_watermark,
              replica_source_catalog,
              replica_source_schema,
              replica_source_name,
              replication_status,
              replication_error
            FROM `{project}.{dataset_id}.INFORMATION_SCHEMA.TABLES`
            ORDER BY table_name
            """,
            billing_project,
            project,
        )
        try:
            field_rows = run_bq_metadata_query(
                f"""
                SELECT
                  table_name,
                  field_path,
                  data_type,
                  description,
                  collation_name,
                  rounding_mode
                FROM `{project}.{dataset_id}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS`
                ORDER BY table_name, field_path
                """,
                billing_project,
                project,
            )
        except RuntimeError:
            field_rows = run_bq_metadata_query(
                f"""
                SELECT
                  table_name,
                  column_name AS field_path,
                  data_type,
                  is_nullable,
                  '' AS description
                FROM `{project}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
                ORDER BY table_name, ordinal_position
                """,
                billing_project,
                project,
            )
        try:
            storage_rows = run_bq_metadata_query(
                f"""
                SELECT
                  table_name,
                  total_rows,
                  total_logical_bytes,
                  active_logical_bytes,
                  long_term_logical_bytes,
                  current_physical_bytes,
                  total_physical_bytes
                FROM `{project}.{dataset_id}.INFORMATION_SCHEMA.TABLE_STORAGE`
                ORDER BY table_name
                """,
                billing_project,
                project,
            )
        except RuntimeError:
            storage_rows = []

        field_rows_by_table: dict[str, list[dict[str, Any]]] = {}
        for row in field_rows:
            field_rows_by_table.setdefault(row["table_name"], []).append(row)
        storage_by_table = {row["table_name"]: row for row in storage_rows}

        tables: list[dict[str, Any]] = []
        for table_row in tables_meta:
            table_id = table_row["table_name"]
            normalized_type = normalize_table_type(table_row.get("table_type"))
            storage = storage_by_table.get(table_id, {})
            fields = fields_from_column_field_paths(field_rows_by_table.get(table_id, []))
            info_row = {
                key: value
                for key, value in table_row.items()
                if value not in (None, "")
            }
            metadata: dict[str, Any] = {
                "kind": "bigquery#table",
                "id": f"{project}:{dataset_id}.{table_id}",
                "tableReference": {
                    "projectId": project,
                    "datasetId": dataset_id,
                    "tableId": table_id,
                },
                "type": normalized_type,
                "creationTime": table_row.get("creation_time"),
                "schema": {"fields": fields},
                "information_schema": info_row,
            }
            if storage:
                metadata["numRows"] = storage.get("total_rows")
                metadata["numBytes"] = storage.get("total_logical_bytes")
                metadata["storage"] = {
                    key: value
                    for key, value in storage.items()
                    if key != "table_name" and value not in (None, "")
                }
            if normalized_type == "VIEW":
                metadata["view_sql_omitted"] = True
            tables.append(
                {
                    "table_id": table_id,
                    "list_metadata": {
                        "type": normalized_type,
                        "raw_table_type": table_row.get("table_type"),
                        "tableReference": {
                            "projectId": project,
                            "datasetId": dataset_id,
                            "tableId": table_id,
                        },
                    },
                    "metadata": metadata,
                }
            )
        datasets.append(
            {
                "dataset_id": dataset_id,
                "list_metadata": ds,
                "metadata": ds_show,
                "tables": sorted(tables, key=lambda item: item["table_id"].lower()),
            }
        )
    return {
        "project": project,
        "billing_project": billing_project,
        "datasets": sorted(datasets, key=lambda item: item["dataset_id"].lower()),
    }


def table_type(table: dict[str, Any]) -> str:
    return (
        table.get("list_metadata", {}).get("type")
        or table.get("metadata", {}).get("type")
        or "TABLE"
    )


def timestamp_from_ms(value: str | int | None) -> str:
    if value in (None, ""):
        return "unknown"
    try:
        millis = int(value)
    except (TypeError, ValueError):
        return str(value)
    return dt.datetime.fromtimestamp(millis / 1000, tz=UTC).isoformat(timespec="seconds")


def infer_dataset_role(dataset_id: str) -> str:
    lower = dataset_id.lower()
    if lower.endswith("_streaming"):
        return "Raw-ish streaming/current-state source layer used to feed views; metadata only here."
    if lower.endswith("_medium"):
        return "Medium-access UltraCart current-state view layer."
    if lower.endswith("_high"):
        return "Higher-access UltraCart current-state view layer; treat as sensitive by default."
    if lower.endswith("_low"):
        return "Lower-access UltraCart current-state view layer."
    if lower == "ultracart_dw":
        return "Standard UltraCart current-state view layer."
    if lower.endswith("_dashboard"):
        return "UltraCart dashboard rollup layer."
    if lower.endswith("_import"):
        return "Imported/helper object layer."
    if lower.endswith("_ml"):
        return "Derived model and feature layer."
    if lower.endswith("_work"):
        return "Workbench/reporting layer; use as reference, not canonical source."
    return "BigQuery dataset discovered from live project metadata."


def infer_table_role(dataset_id: str, table_id: str, obj_type: str) -> str:
    name = table_id.lower()
    if "order" in name and "auto" not in name:
        return "Order-related object inferred from table name and schema metadata."
    if "auto_order" in name:
        return "Subscription or auto-order lifecycle object inferred from table name and schema metadata."
    if "item" in name or "sku" in name:
        return "Item/product/catalog object inferred from table name and schema metadata."
    if "screen_record" in name or "session" in name or "traffic" in name:
        return "Session, screen-recording, or storefront behavior object inferred from table name and schema metadata."
    if "affiliate" in name:
        return "Affiliate, commission, click, or payment object inferred from table name and schema metadata."
    if "storefront" in name:
        return "Storefront configuration, page, experiment, or customer-email object inferred from table name and schema metadata."
    if "conversation" in name or "ticket" in name or "pbx" in name:
        return "Support/conversation object inferred from table name and schema metadata; treat as sensitive."
    if obj_type == "VIEW":
        return "BigQuery view discovered from live metadata."
    if obj_type == "MATERIALIZED_VIEW":
        return "BigQuery materialized view discovered from live metadata."
    if dataset_id.endswith("_streaming"):
        return "Physical streaming table discovered from live metadata."
    return "BigQuery table discovered from live metadata."


def schema_markdown(fields: list[dict[str, Any]]) -> str:
    rows = flatten_schema(fields)
    if not rows:
        return "_No schema fields were returned by live BigQuery metadata._"
    out = ["| Field path | Type | Mode | Description |", "|---|---|---|---|"]
    for row in rows:
        out.append(
            "| `{}` | {} | {} | {} |".format(
                md_escape(row["field_path"]),
                md_escape(row["type"]),
                md_escape(row["mode"]),
                md_escape(row["description"]),
            )
        )
    return "\n".join(out)


def table_link(dataset_id: str, table_id: str) -> str:
    return f"/tables/{safe_slug(dataset_id)}/{safe_slug(table_id)}.md"


def dataset_link(dataset_id: str) -> str:
    return f"/datasets/{safe_slug(dataset_id)}.md"


def group_tables_by_name(metadata: dict[str, Any]) -> dict[str, list[tuple[str, str]]]:
    by_name: dict[str, list[tuple[str, str]]] = {}
    for ds in metadata["datasets"]:
        dataset_id = ds["dataset_id"]
        for table in ds["tables"]:
            by_name.setdefault(table["table_id"], []).append((dataset_id, table["table_id"]))
    return by_name


def write_project_doc(bundle: Path, metadata: dict[str, Any], generated_at: str, tags: list[str]) -> None:
    project = metadata["project"]
    dataset_count = len(metadata["datasets"])
    table_count = sum(len(ds["tables"]) for ds in metadata["datasets"])
    body = [
        f"`{project}` is the live BigQuery project used as the source for this OKF bundle.",
        "",
        "This concept was generated from BigQuery project/dataset/table metadata only. No table rows were queried or sampled.",
        "",
        "# Discovered Datasets",
        "",
        "| Dataset | Tables/views | Role |",
        "|---|---:|---|",
    ]
    for ds in metadata["datasets"]:
        body.append(
            f"| [{ds['dataset_id']}]({dataset_link(ds['dataset_id'])}) | "
            f"{len(ds['tables'])} | {md_escape(infer_dataset_role(ds['dataset_id']))} |"
        )
    body.extend(
        [
            "",
            "# Source Metadata",
            "",
            f"- Dataset count: `{dataset_count}`",
            f"- Table/view/materialized-view count: `{table_count}`",
            f"- Generated at: `{generated_at}`",
            "",
            "# Citations",
            "",
            f"[1] [BigQuery project resource]({bq_resource(project)})",
        ]
    )
    write_doc(
        bundle / "projects" / f"{safe_slug(project)}.md",
        {
            "type": "BigQuery Project",
            "title": project,
            "description": f"Live BigQuery project containing {dataset_count} datasets and {table_count} discovered objects.",
            "resource": bq_resource(project),
            "tags": tags + ["bigquery-project"],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/build_ultracart_okf.py",
            "source_project": project,
        },
        "\n".join(body),
    )


def write_dataset_doc(bundle: Path, project: str, ds: dict[str, Any], generated_at: str, tags: list[str]) -> None:
    dataset_id = ds["dataset_id"]
    meta = ds["metadata"]
    role = infer_dataset_role(dataset_id)
    created = timestamp_from_ms(meta.get("creationTime"))
    modified = timestamp_from_ms(meta.get("lastModifiedTime"))
    body = [
        f"`{project}.{dataset_id}` is a BigQuery dataset discovered from live metadata.",
        "",
        role,
        "",
        "# Dataset Metadata",
        "",
        f"- Project: [`{project}`](/projects/{safe_slug(project)}.md)",
        f"- Location: `{meta.get('location') or ds.get('list_metadata', {}).get('location') or 'unknown'}`",
        f"- Created: `{created}`",
        f"- Last modified: `{modified}`",
        f"- Discovered objects: `{len(ds['tables'])}`",
        "",
        "# Objects",
        "",
        "| Object | Type | Field count | Sensitivity |",
        "|---|---|---:|---|",
    ]
    for table in ds["tables"]:
        fields = table.get("metadata", {}).get("schema", {}).get("fields", []) or []
        sensitivity, _ = sensitivity_for_fields(fields)
        body.append(
            f"| [{table['table_id']}]({table_link(dataset_id, table['table_id'])}) | "
            f"{md_escape(table_type(table))} | {field_count(fields)} | {sensitivity} |"
        )
    body.extend(
        [
            "",
            "# Common Query Patterns",
            "",
            "```sql",
            f"SELECT table_name, table_type",
            f"FROM `{project}.{dataset_id}.INFORMATION_SCHEMA.TABLES`",
            "ORDER BY table_name;",
            "```",
            "",
            "# Citations",
            "",
            f"[1] [BigQuery dataset resource]({bq_resource(project, dataset_id)})",
        ]
    )
    write_doc(
        bundle / "datasets" / f"{safe_slug(dataset_id)}.md",
        {
            "type": "BigQuery Dataset",
            "title": f"{dataset_id}",
            "description": f"Live BigQuery dataset with {len(ds['tables'])} discovered objects.",
            "resource": bq_resource(project, dataset_id),
            "tags": tags + ["bigquery-dataset", dataset_id],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/build_ultracart_okf.py",
            "source_project": project,
            "source_dataset": dataset_id,
            "source_role": role,
        },
        "\n".join(body),
    )


def write_table_doc(
    bundle: Path,
    project: str,
    dataset_id: str,
    table: dict[str, Any],
    generated_at: str,
    tags: list[str],
    by_name: dict[str, list[tuple[str, str]]],
) -> None:
    table_id = table["table_id"]
    meta = table["metadata"]
    fields = meta.get("schema", {}).get("fields", []) or []
    obj_type = table_type(table)
    sensitivity, sensitive_fields = sensitivity_for_fields(fields)
    role = infer_table_role(dataset_id, table_id, obj_type)
    created = timestamp_from_ms(meta.get("creationTime"))
    modified = timestamp_from_ms(meta.get("lastModifiedTime"))
    row_count = meta.get("numRows", "not reported for this object type")
    bytes_count = meta.get("numBytes", "not reported")
    siblings = [
        (ds, tbl)
        for ds, tbl in by_name.get(table_id, [])
        if not (ds == dataset_id and tbl == table_id)
    ]

    body = [
        f"`{project}.{dataset_id}.{table_id}` is a `{obj_type}` discovered from live BigQuery metadata.",
        "",
        role,
        "",
        "# Grain And Role",
        "",
        "The exact analytical grain should be confirmed from the schema and downstream usage before building reporting logic. This OKF concept records source metadata and safe usage guidance; it does not assert row-level business semantics beyond what can be inferred from live metadata.",
        "",
        "# BigQuery Metadata",
        "",
        f"- Dataset: [`{dataset_id}`]({dataset_link(dataset_id)})",
        f"- Object type: `{obj_type}`",
        f"- Created: `{created}`",
        f"- Last modified: `{modified}`",
        f"- Reported rows: `{row_count}`",
        f"- Reported bytes: `{bytes_count}`",
        f"- Field count: `{field_count(fields)}`",
        f"- Sensitivity: `{sensitivity}`",
    ]
    if meta.get("timePartitioning"):
        body.append(f"- Time partitioning: `{json.dumps(meta['timePartitioning'], sort_keys=True)}`")
    if meta.get("rangePartitioning"):
        body.append(f"- Range partitioning: `{json.dumps(meta['rangePartitioning'], sort_keys=True)}`")
    if meta.get("clustering"):
        body.append(f"- Clustering: `{json.dumps(meta['clustering'], sort_keys=True)}`")
    if meta.get("view_sql_omitted"):
        body.append("- View SQL: omitted by generator policy; this bundle stores metadata, not full SQL definitions.")
    body.extend(["", "# Schema", "", schema_markdown(fields), ""])

    body.extend(["# Sensitivity Notes", ""])
    if sensitive_fields:
        shown = ", ".join(f"`{field}`" for field in sensitive_fields[:40])
        more = f" and {len(sensitive_fields) - 40} more" if len(sensitive_fields) > 40 else ""
        body.append(
            "Sensitive-looking field names were detected in metadata: "
            f"{shown}{more}. Treat this concept as metadata-only; do not sample rows casually."
        )
    else:
        body.append("No sensitive-looking field names were detected by the generator's conservative name scan.")
    body.append("")

    if siblings:
        body.extend(["# Related Objects", ""])
        body.append("Objects with the same table id in other live datasets:")
        body.append("")
        for ds, tbl in siblings:
            body.append(f"- [`{ds}.{tbl}`]({table_link(ds, tbl)})")
        body.append("")

    body.extend(
        [
            "# Common Query Patterns",
            "",
            "Metadata-only schema inspection:",
            "",
            "```sql",
            "SELECT column_name, data_type, is_nullable",
            f"FROM `{project}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`",
            f"WHERE table_name = '{table_id}'",
            "ORDER BY ordinal_position;",
            "```",
            "",
            "Aggregate-only row count check, if a cost review approves querying this object:",
            "",
            "```sql",
            f"SELECT COUNT(*) AS row_count",
            f"FROM `{project}.{dataset_id}.{table_id}`;",
            "```",
            "",
            "# Citations",
            "",
            f"[1] [BigQuery table resource]({bq_resource(project, dataset_id, table_id)})",
        ]
    )
    write_doc(
        bundle / "tables" / safe_slug(dataset_id) / f"{safe_slug(table_id)}.md",
        {
            "type": f"BigQuery {obj_type.title().replace('_', ' ')}",
            "title": f"{dataset_id}.{table_id}",
            "description": f"Live BigQuery {obj_type.lower()} with {field_count(fields)} schema fields in {dataset_id}.",
            "resource": bq_resource(project, dataset_id, table_id),
            "tags": tags + ["bigquery-table", dataset_id, table_id, sensitivity],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/build_ultracart_okf.py",
            "source_project": project,
            "source_dataset": dataset_id,
            "source_table": table_id,
            "source_object_type": obj_type,
            "sensitivity": sensitivity,
            "field_count": field_count(fields),
        },
        "\n".join(body),
    )


def write_indexes(bundle: Path, metadata: dict[str, Any], generated_at: str) -> None:
    project = metadata["project"]
    table_count = sum(len(ds["tables"]) for ds in metadata["datasets"])
    root = [
        "---",
        'okf_version: "0.1"',
        "---",
        "",
        f"# {project} OKF Bundle",
        "",
        "Generated from live BigQuery metadata. Concept docs are Markdown files with YAML frontmatter.",
        "",
        "# Entry Points",
        "",
        f"* [Project](/projects/{safe_slug(project)}.md) - Live BigQuery project overview.",
        "* [Datasets](datasets/) - One concept per discovered BigQuery dataset.",
        "* [Tables](tables/) - One concept per discovered BigQuery object, grouped by dataset.",
        "* [References](references/) - Generator policy, sensitivity rules, and run metadata.",
        "",
        "# Summary",
        "",
        f"* Datasets: {len(metadata['datasets'])}",
        f"* Tables/views/materialized views: {table_count}",
        f"* Generated at: {generated_at}",
    ]
    write_plain(bundle / "index.md", "\n".join(root))

    write_plain(
        bundle / "projects" / "index.md",
        "# BigQuery Projects\n\n"
        f"* [{project}]({safe_slug(project)}.md) - Source project for this OKF bundle.",
    )

    datasets = ["# Datasets", ""]
    for ds in metadata["datasets"]:
        datasets.append(
            f"* [{ds['dataset_id']}]({safe_slug(ds['dataset_id'])}.md) - "
            f"{len(ds['tables'])} discovered objects."
        )
    write_plain(bundle / "datasets" / "index.md", "\n".join(datasets))

    tables_root = ["# Tables", ""]
    for ds in metadata["datasets"]:
        dataset_id = ds["dataset_id"]
        tables_root.append(
            f"* [{dataset_id}]({safe_slug(dataset_id)}/) - {len(ds['tables'])} discovered objects."
        )
        table_index = [f"# {dataset_id} Tables", ""]
        for table in ds["tables"]:
            fields = table.get("metadata", {}).get("schema", {}).get("fields", []) or []
            table_index.append(
                f"* [{table['table_id']}]({safe_slug(table['table_id'])}.md) - "
                f"{table_type(table)} with {field_count(fields)} schema fields."
            )
        write_plain(bundle / "tables" / safe_slug(dataset_id) / "index.md", "\n".join(table_index))
    write_plain(bundle / "tables" / "index.md", "\n".join(tables_root))

    refs = [
        "# References",
        "",
        "* [Generator Policy](generator_policy.md) - How this bundle was generated safely from BigQuery metadata.",
        "* [Inferred Table Families](inferred_table_families.md) - Table-name families found across live datasets.",
        "* [Generation Run](generation_run.md) - Counts and command context for the latest generation.",
    ]
    write_plain(bundle / "references" / "index.md", "\n".join(refs))

    log = [
        "# Bundle Update Log",
        "",
        f"## {generated_at[:10]}",
        f"* **Creation**: Generated the OKF bundle from live BigQuery metadata for `{project}`.",
    ]
    write_plain(bundle / "log.md", "\n".join(log))


def write_references(bundle: Path, metadata: dict[str, Any], generated_at: str, tags: list[str]) -> None:
    project = metadata["project"]
    table_count = sum(len(ds["tables"]) for ds in metadata["datasets"])
    write_doc(
        bundle / "references" / "generator_policy.md",
        {
            "type": "Generator Policy",
            "title": "Live BigQuery Metadata Generator Policy",
            "description": "Safety and source policy for generating this OKF bundle from BigQuery metadata only.",
            "resource": bq_resource(project),
            "tags": tags + ["generator-policy", "safety"],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/build_ultracart_okf.py",
        },
        "\n".join(
            [
                "This bundle is generated from live BigQuery metadata using `bq ls` and `bq show`.",
                "",
                "# Allowed Inputs",
                "",
                "- Dataset listings.",
                "- Table/view/materialized-view listings.",
                "- Dataset metadata.",
                "- Table metadata and schema fields.",
                "",
                "# Explicit Exclusions",
                "",
                "- No all-column row queries.",
                "- No row samples.",
                "- No raw customer records.",
                "- No raw email, address, phone, payment, conversation, or session payload values.",
                "- No full view SQL in the OKF bundle.",
                "",
                "# Citations",
                "",
                f"[1] [BigQuery project resource]({bq_resource(project)})",
            ]
        ),
    )

    by_name = group_tables_by_name(metadata)
    families = {name: refs for name, refs in by_name.items() if len(refs) > 1}
    lines = [
        "This concept lists table ids that appear in more than one live dataset in the source project.",
        "",
        "# Families",
        "",
    ]
    if not families:
        lines.append("_No repeated table ids were discovered across datasets._")
    else:
        for table_id in sorted(families):
            lines.append(f"## `{table_id}`")
            lines.append("")
            for dataset_id, sibling_table in sorted(families[table_id]):
                lines.append(f"- [`{dataset_id}.{sibling_table}`]({table_link(dataset_id, sibling_table)})")
            lines.append("")
    lines.extend(["# Citations", "", f"[1] [BigQuery project resource]({bq_resource(project)})"])
    write_doc(
        bundle / "references" / "inferred_table_families.md",
        {
            "type": "Inferred Relationship Map",
            "title": "Inferred Table Families",
            "description": "Table ids that repeat across live BigQuery datasets in the source project.",
            "resource": bq_resource(project),
            "tags": tags + ["table-families", "inferred"],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/build_ultracart_okf.py",
        },
        "\n".join(lines),
    )

    run_lines = [
        "This concept records the latest OKF generation run.",
        "",
        "# Counts",
        "",
        f"- Source project: `{project}`",
        f"- Billing project used by `bq`: `{metadata.get('billing_project') or project}`",
        f"- Dataset count: `{len(metadata['datasets'])}`",
        f"- Table/view/materialized-view count: `{table_count}`",
        f"- Generated at: `{generated_at}`",
        "",
        "# Dataset Counts",
        "",
        "| Dataset | Objects |",
        "|---|---:|",
    ]
    for ds in metadata["datasets"]:
        run_lines.append(f"| [`{ds['dataset_id']}`]({dataset_link(ds['dataset_id'])}) | {len(ds['tables'])} |")
    run_lines.extend(["", "# Citations", "", f"[1] [BigQuery project resource]({bq_resource(project)})"])
    write_doc(
        bundle / "references" / "generation_run.md",
        {
            "type": "Generation Run",
            "title": "Latest Generation Run",
            "description": f"Live BigQuery metadata generation run with {len(metadata['datasets'])} datasets and {table_count} objects.",
            "resource": bq_resource(project),
            "tags": tags + ["generation-run"],
            "timestamp": generated_at,
            "okf_version": "0.1",
            "generated_by": "scripts/build_ultracart_okf.py",
        },
        "\n".join(run_lines),
    )


def write_source_metadata(bundle: Path, metadata: dict[str, Any], generated_at: str) -> None:
    meta_dir = bundle / "_source_metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "generated_at": generated_at,
        "source_project": metadata["project"],
        "billing_project": metadata.get("billing_project"),
        "dataset_count": len(metadata["datasets"]),
        "object_count": sum(len(ds["tables"]) for ds in metadata["datasets"]),
        "datasets": [
            {
                "dataset_id": ds["dataset_id"],
                "object_count": len(ds["tables"]),
                "objects": [
                    {
                        "table_id": table["table_id"],
                        "type": table_type(table),
                        "field_count": field_count(
                            table.get("metadata", {}).get("schema", {}).get("fields", []) or []
                        ),
                    }
                    for table in ds["tables"]
                ],
            }
            for ds in metadata["datasets"]
        ],
    }
    (meta_dir / "source_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    # Store sanitized metadata for traceability. Full view SQL is omitted.
    (meta_dir / "sanitized_bq_metadata.json").write_text(
        json.dumps(redact_raw_emails(metadata), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def build_bundle(config: dict[str, Any], out: Path) -> dict[str, Any]:
    project = str(config.get("source_project") or "").strip()
    if not project or project.startswith("YOUR_"):
        raise ValueError("config must set source_project to an authorized UltraCart BigQuery project")
    billing_project = str(config.get("billing_project") or "") or None
    if billing_project and billing_project.startswith("YOUR_"):
        billing_project = None
    allowlist = config.get("dataset_allowlist") or []
    if not isinstance(allowlist, list):
        allowlist = []
    tags = config.get("tags") or ["ultracart", "bigquery", "okf"]
    if not isinstance(tags, list):
        tags = ["ultracart", "bigquery", "okf"]
    generated_at = dt.datetime.now(UTC).isoformat(timespec="seconds")

    metadata = discover_metadata(project, billing_project, allowlist)
    metadata["billing_project"] = billing_project

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    by_name = group_tables_by_name(metadata)
    write_indexes(out, metadata, generated_at)
    write_project_doc(out, metadata, generated_at, tags)
    for ds in metadata["datasets"]:
        write_dataset_doc(out, project, ds, generated_at, tags)
        for table in ds["tables"]:
            write_table_doc(out, project, ds["dataset_id"], table, generated_at, tags, by_name)
    write_references(out, metadata, generated_at, tags)
    write_source_metadata(out, metadata, generated_at)
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description="Build UltraCart OKF from live BigQuery metadata.")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--no-viewer", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    metadata = build_bundle(config, args.out)

    if not args.no_viewer:
        viewer_script = ROOT / "scripts" / "build_okf_viewer.py"
        subprocess.run([sys.executable, str(viewer_script), str(args.out)], check=True)

    table_count = sum(len(ds["tables"]) for ds in metadata["datasets"])
    print(
        f"Generated OKF bundle at {args.out} from live BigQuery metadata: "
        f"{len(metadata['datasets'])} datasets, {table_count} objects."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
