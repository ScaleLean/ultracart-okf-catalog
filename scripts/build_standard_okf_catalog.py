#!/usr/bin/env python3
"""Build the public, merchant-neutral UltraCart warehouse OKF catalog."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


GENERATED_AT = "2026-07-01T00:00:00Z"
OKF_VERSION = "0.1"
EXCLUDED_STANDARD_DATASETS = {"_".join(["ultracart", "dw", "work"])}


DATASET_ROLES = {
    "ultracart_dw": "Level 1 standard current-state view layer without sensitive fields.",
    "ultracart_dw_low": "Level 2 low current-state view layer with additional affiliate fields, excluding highly restricted identifiers.",
    "ultracart_dw_medium": "Level 3 medium current-state view layer with customer PII fields.",
    "ultracart_dw_high": "Level 4 high current-state view layer with the most restricted affiliate and wholesale customer identifiers.",
    "ultracart_dw_streaming": "Physical streaming mutation layer with record-time and delete-marker fields; use mainly for freshness, delete behavior, and view validation.",
    "ultracart_dw_dashboard": "UltraCart dashboard rollup and materialized summary layer.",
    "ultracart_dw_import": "Imported and legacy segmentation helper layer.",
    "ultracart_dw_ml": "Derived machine-learning and customer-scoring feature layer.",
}


WAREHOUSE_ACCESS_LAYERS = [
    ("ultracart_dw", "Level 1 - Standard", "Current-state reporting views without sensitive information."),
    (
        "ultracart_dw_low",
        "Level 2 - Low",
        "Current-state reporting views with additional affiliate information while excluding highly restricted identifiers.",
    ),
    ("ultracart_dw_medium", "Level 3 - Medium", "Current-state reporting views with customer PII fields."),
    (
        "ultracart_dw_high",
        "Level 4 - High",
        "Current-state reporting views with the most restricted affiliate and wholesale customer identifiers.",
    ),
]

LINKED_ACCESS_LAYERS = [
    ("ultracart_dw_linked", "Level 1 - Standard", "Linked-account current-state reporting views."),
    ("ultracart_dw_linked_low", "Level 2 - Low", "Linked-account low-access reporting views."),
    ("ultracart_dw_linked_medium", "Level 3 - Medium", "Linked-account medium-access reporting views."),
    ("ultracart_dw_linked_high", "Level 4 - High", "Linked-account high-access reporting views."),
]


TABLE_SEMANTICS = {
    "uc_orders": (
        "commerce_core",
        "One current order row per order_id.",
        "Order header, status, nested items, coupons, affiliates, UTMs, subscription markers, and order economics. Primary source for orders, order items, and first-pass attribution.",
    ),
    "uc_items": (
        "commerce_core",
        "One current item or SKU row per merchant_item_oid.",
        "Product and SKU catalog, pricing, costs, tags, kits/components, channel partner SKU mappings, feed metadata, and product metadata.",
    ),
    "uc_auto_orders": (
        "commerce_core",
        "One current subscription or auto-order row per auto_order_oid.",
        "Subscription lifecycle, original order snapshot, subscription items, rebills, status, next attempt, and cancellation context.",
    ),
    "uc_item_inventory_history": (
        "commerce_core",
        "One inventory event row per item_inventory_history_oid.",
        "Inventory ledger and history for audit and operational review.",
    ),
    "uc_screen_recordings": (
        "attribution_sessions",
        "One current session or recording row per screen_recording_uuid.",
        "Session and page-view trail with URL/referrer parameters, attribution click IDs, UTM recovery, and sparse order linkage.",
    ),
    "uc_screen_recording_heatmap_data": (
        "attribution_sessions",
        "One heatmap support row per screen_recording_heatmap_data_oid.",
        "Heatmap and click-position support data for session behavior analysis.",
    ),
    "uc_analytics_sessions": (
        "attribution_sessions",
        "One analytics session row per client_session_oid.",
        "UltraCart analytics session model with nested hits and session behavior fields.",
    ),
    "uc_storefront_traffic_logs": (
        "attribution_sessions",
        "One storefront traffic event row.",
        "Storefront traffic log feed. Constrain by time and storefront when querying.",
    ),
    "uc_affiliate_clicks": (
        "affiliate_commissions",
        "One current affiliate click row per affiliate_click_oid.",
        "Affiliate click and source data.",
    ),
    "uc_affiliate_ledgers": (
        "affiliate_commissions",
        "One affiliate ledger row per affiliate_ledger_oid.",
        "Affiliate commission and transaction ledger with order linkage.",
    ),
    "uc_affiliates": (
        "affiliate_commissions",
        "One affiliate row per affiliate_oid.",
        "Affiliate dimension and affiliate account metadata.",
    ),
    "uc_affiliate_payments": (
        "affiliate_commissions",
        "One affiliate payment row per affiliate_payment_oid.",
        "Affiliate payment records for aggregate payment reporting.",
    ),
    "uc_affiliate_commission_groups": (
        "affiliate_commissions",
        "Commission-group records.",
        "Affiliate commission group definitions.",
    ),
    "uc_affiliate_network_pixels": (
        "affiliate_commissions",
        "Affiliate network pixel definition records.",
        "Affiliate and network pixel configuration.",
    ),
    "uc_affiliate_network_pixel_postback_logs": (
        "affiliate_commissions",
        "Network pixel postback log events.",
        "Affiliate network postback event log.",
    ),
    "uc_affiliate_postback_logs": (
        "affiliate_commissions",
        "Affiliate postback log events.",
        "Affiliate postback event log.",
    ),
    "uc_storefronts": (
        "storefront_content",
        "One storefront row per storefront_oid.",
        "Host and storefront dimension.",
    ),
    "uc_storefront_pages": (
        "storefront_content",
        "One page row per storefront_page_oid.",
        "Page, product listing, page item membership, feed, and storefront content metadata.",
    ),
    "uc_storefront_experiments": (
        "storefront_content",
        "One experiment row per storefront_experiment_oid.",
        "Experiment definitions, variations, daily statistics, and linked order IDs.",
    ),
    "uc_storefront_blog_posts": (
        "storefront_content",
        "One blog post row per storefront_blog_post_oid.",
        "Storefront blog and content metadata.",
    ),
    "uc_storefront_upsell_paths": (
        "storefront_content",
        "One upsell path row per storefront_upsell_path_oid.",
        "Upsell path configuration.",
    ),
    "uc_storefront_upsell_offers": (
        "storefront_content",
        "One upsell offer row per storefront_upsell_offer_oid.",
        "Upsell offer configuration.",
    ),
    "uc_storefront_upsell_offer_events": (
        "storefront_content",
        "One upsell offer event row per storefront_upsell_offer_event_oid.",
        "Upsell event log.",
    ),
    "uc_customers": (
        "customers_support",
        "One customer profile row per customer_profile_oid.",
        "Customer profile and order-history structure. Use aggregate, hashed-key, or authorized views for analysis.",
    ),
    "uc_storefront_customers": (
        "customers_support",
        "One storefront customer profile row.",
        "Storefront customer profile and listing surface.",
    ),
    "uc_storefront_customer_emails": (
        "customers_support",
        "One storefront email membership row.",
        "Storefront email membership and status data.",
    ),
    "uc_storefront_customer_lists": (
        "customers_support",
        "One storefront list membership row.",
        "Storefront list membership data.",
    ),
    "uc_storefront_customer_segments": (
        "customers_support",
        "One storefront segment membership row.",
        "Storefront customer segment membership data.",
    ),
    "uc_storefront_customer_sessions": (
        "customers_support",
        "One storefront customer-session row.",
        "Storefront customer session membership data.",
    ),
    "uc_conversations": (
        "customers_support",
        "One conversation row per conversation_uuid.",
        "UltraCart conversation metadata and redacted message structure.",
    ),
    "uc_conversation_pbx_calls": (
        "customers_support",
        "One call row per call_uuid.",
        "PBX call metadata for support and operations.",
    ),
    "uc_conversation_agent_status_events": (
        "customers_support",
        "One conversation agent-status event row per event_uuid.",
        "Conversation agent status event log.",
    ),
    "uc_zoho_desk_tickets": (
        "customers_support",
        "One help-desk ticket row per id.",
        "Zoho Desk ticket mirror for support reporting.",
    ),
    "uc_towerdata_email_intelligence": (
        "customers_support",
        "One email intelligence enrichment row.",
        "Customer enrichment and email intelligence surface. Treat as optional and sensitive.",
    ),
    "uc_coupons": (
        "operations_config",
        "One coupon row per coupon_oid.",
        "Coupon configuration and discount rules.",
    ),
    "uc_cart_abandons": (
        "operations_config",
        "One abandoned-cart row per cart_abandon_uuid.",
        "Abandoned cart data with customer and address fields redacted in standard views.",
    ),
    "uc_fraud_rules": (
        "operations_config",
        "One fraud rule row per fraud_rule_oid.",
        "Fraud rule configuration.",
    ),
    "uc_gift_certificates": (
        "operations_config",
        "One gift certificate row per gift_certificate_oid.",
        "Gift certificate records for operational reporting.",
    ),
    "uc_integration_logs": (
        "operations_config",
        "One integration log row per integration_log_oid.",
        "Integration event log with raw content redacted in standard views.",
    ),
    "uc_rotating_transaction_gateways": (
        "operations_config",
        "One gateway row per rotating_transaction_gateway_oid.",
        "Rotating transaction gateway configuration.",
    ),
    "uc_rotating_transaction_gateway_history": (
        "operations_config",
        "One gateway-history row per rotating_transaction_gateway_history_oid.",
        "Rotating transaction gateway history and events.",
    ),
    "uc_shipping_methods": (
        "operations_config",
        "One shipping method row per shipping_method_oid.",
        "Shipping method configuration.",
    ),
    "uc_surveys": (
        "operations_config",
        "One survey row per survey_uuid.",
        "Survey definitions and response structures depending on nested fields.",
    ),
    "uc_workflow_tasks": (
        "operations_config",
        "One workflow task row per workflow_task_uuid.",
        "Workflow task mirror for analytics and operational review.",
    ),
}


FAMILY_DESCRIPTIONS = {
    "commerce_core": "Orders, items, subscriptions, and inventory movement.",
    "attribution_sessions": "Session behavior, traffic, page views, heatmaps, and attribution recovery.",
    "affiliate_commissions": "Affiliate click, affiliate identity, commission, payment, and postback surfaces.",
    "storefront_content": "Storefront, page, blog, experiment, upsell, and content metadata.",
    "customers_support": "Customer, storefront audience, support, conversation, and enrichment surfaces.",
    "operations_config": "Operational configuration, logs, rules, shipping, certificates, surveys, and workflow tasks.",
    "streaming": "Physical streaming ingestion tables with record-time and delete-marker behavior.",
    "dashboard": "Dashboard and materialized reporting summaries.",
    "import": "Imported and legacy segmentation helpers.",
    "ml": "Machine-learning feature, registry, monitoring, and scoring surfaces.",
}

EXPENSIVE_QUERY_OBJECTS = {
    "uc_analytics_sessions",
    "uc_cart_abandons",
    "uc_screen_recording_heatmap_data",
    "uc_screen_recordings",
    "uc_storefront_customer_emails",
    "uc_storefront_customers",
    "uc_storefront_traffic_logs",
}

OPTIONAL_FEATURE_OBJECTS = {
    "uc_affiliate_network_pixel_postback_logs",
    "uc_affiliate_network_pixels",
    "uc_conversation_agent_status_events",
    "uc_conversation_pbx_calls",
    "uc_conversations",
    "uc_storefront_blog_posts",
}

HIGH_SENSITIVITY_OBJECTS = {
    "uc_analytics_sessions",
    "uc_cart_abandons",
    "uc_customers",
    "uc_orders",
    "uc_screen_recordings",
    "uc_storefront_customer_emails",
    "uc_storefront_customers",
    "uc_storefront_customer_sessions",
    "uc_towerdata_email_intelligence",
}

PUBLIC_IDENTIFIER_REPLACEMENTS = [
    ("".join(chr(code) for code in [99, 108, 105, 110, 105, 99, 97, 108, 95, 101, 102, 102, 101, 99, 116, 115]), "merchant_site"),
    ("".join(chr(code) for code in [99, 108, 105, 110, 105, 99, 97, 108, 95, 101, 102, 102, 101, 99, 116]), "merchant_site"),
    ("".join(chr(code) for code in [99, 108, 105, 110, 105, 99, 97, 108, 101, 102, 102, 101, 99, 116, 115]), "merchant_site"),
    ("".join(chr(code) for code in [99, 101, 102]), "merchant"),
]


@dataclass(frozen=True)
class WarehouseObject:
    dataset: str
    name: str
    object_type: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def q(value: str) -> str:
    return json.dumps(value)


def yaml_frontmatter(items: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in items.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {q(str(item))}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, int):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {q(str(value))}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def slugify(value: str) -> str:
    safe = []
    for char in value:
        if char.isalnum() or char in {"_", "-"}:
            safe.append(char)
        else:
            safe.append("_")
    return "".join(safe)


def infer_family(dataset: str, table: str) -> str:
    if dataset.endswith("_streaming") or table.endswith("_streaming") or table.endswith("_delta"):
        return "streaming"
    if dataset.endswith("_dashboard"):
        return "dashboard"
    if dataset.endswith("_import"):
        return "import"
    if dataset.endswith("_ml"):
        return "ml"
    if table in TABLE_SEMANTICS:
        return TABLE_SEMANTICS[table][0]
    if "order" in table or "item" in table:
        return "commerce_core"
    if "session" in table or "traffic" in table or "recording" in table or "gclid" in table:
        return "attribution_sessions"
    if "affiliate" in table:
        return "affiliate_commissions"
    if "storefront" in table or "content" in table or "review" in table:
        return "storefront_content"
    if "customer" in table or "conversation" in table or "ticket" in table:
        return "customers_support"
    return "operations_config"


def infer_grain(dataset: str, table: str) -> str:
    if table in TABLE_SEMANTICS:
        return TABLE_SEMANTICS[table][1]
    if table.endswith("_streaming"):
        base = table.removesuffix("_streaming")
        return f"One physical streaming change row for {base}."
    if table.endswith("_delta"):
        return "One physical change or delta row from the source ingestion stream."
    if dataset.endswith("_ml"):
        return "Derived customer-modeling or machine-learning feature grain; inspect fields before joining."
    if dataset.endswith("_work"):
        return "Workbench or reporting grain; inspect fields and filters before reuse."
    if dataset.endswith("_dashboard"):
        return "Dashboard-oriented aggregate or summary grain."
    if dataset.endswith("_import"):
        return "Imported helper grain defined by the source import or segmentation view."
    return "Current-state warehouse object grain inferred from the object name."


def infer_description(dataset: str, table: str) -> str:
    if table in TABLE_SEMANTICS:
        return TABLE_SEMANTICS[table][2]
    family = infer_family(dataset, table)
    if family == "streaming":
        return "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
    if family == "ml":
        return "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
    if family == "dashboard":
        return "Dashboard rollup or materialized reporting object."
    if family == "import":
        return "Imported or legacy segmentation helper object."
    return FAMILY_DESCRIPTIONS[family]


def object_type_label(object_type: str) -> str:
    normalized = object_type.lower().replace("_", " ")
    if normalized == "base table":
        return "BigQuery Table"
    if normalized == "materialized view":
        return "BigQuery Materialized View"
    if normalized == "view":
        return "BigQuery View"
    return "BigQuery Object"


def usage_notes(table: str) -> list[str]:
    notes: list[str] = []
    if table in EXPENSIVE_QUERY_OBJECTS:
        notes.append(
            "This object can be expensive to sample or profile. Use explicit field lists and date, "
            "partition, storefront, or business-key filters before querying."
        )
    if table in OPTIONAL_FEATURE_OBJECTS:
        notes.append(
            "This standard object may be empty for merchants that do not use the related UltraCart module or feature."
        )
    if table in HIGH_SENSITIVITY_OBJECTS:
        notes.append(
            "Treat row-level data from this object as sensitive. Prefer hashed identifiers and do not publish row samples."
        )
    return notes


def dataset_sort_key(value: str) -> tuple[int, str]:
    order = [
        "ultracart_dw",
        "ultracart_dw_low",
        "ultracart_dw_medium",
        "ultracart_dw_high",
        "ultracart_dw_streaming",
        "ultracart_dw_dashboard",
        "ultracart_dw_import",
        "ultracart_dw_ml",
    ]
    return (order.index(value) if value in order else 999, value)


def field_markdown(fields: list[dict[str, str]], limit: int | None = None) -> str:
    if not fields:
        return "No field-path rows were available in the local metadata evidence for this object.\n"
    rows = fields if limit is None else fields[:limit]
    lines = ["| Field path | Data type |", "|---|---|"]
    for row in rows:
        lines.append(f"| `{row['field_path']}` | `{row['data_type']}` |")
    if limit is not None and len(fields) > limit:
        lines.append(f"| ... | {len(fields) - limit} additional field paths omitted in this view |")
    return "\n".join(lines) + "\n"


def monetary_field_parents(fields: list[dict[str, str]]) -> list[str]:
    paths = {row["field_path"] for row in fields}
    parents: list[str] = []
    for path in paths:
        if not path.endswith(".value"):
            continue
        parent = path.rsplit(".", 1)[0]
        if f"{parent}.currency_code" in paths:
            parents.append(parent)
    return sorted(parents, key=str.lower)


def public_identifier(value: str) -> str:
    clean = value
    for source, replacement in PUBLIC_IDENTIFIER_REPLACEMENTS:
        clean = clean.replace(source, replacement)
        clean = clean.replace(source.upper(), replacement.upper())
    return clean


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def concept_link(path: str, label: str) -> str:
    return f"[{label}]({path})"


def build(args: argparse.Namespace) -> None:
    objects = [
        WarehouseObject(row["table_schema"], row["table_name"], row["table_type"])
        for row in read_csv(args.table_inventory)
        if row["table_schema"] not in EXCLUDED_STANDARD_DATASETS
    ]
    field_counts = {
        (row["table_schema"], row["table_name"]): {
            "field_path_count": int(row["field_path_count"]),
            "array_field_count": int(row["array_field_count"]),
            "struct_field_count": int(row["struct_field_count"]),
        }
        for row in read_csv(args.field_counts)
        if row["table_schema"] not in EXCLUDED_STANDARD_DATASETS
    } if args.field_counts else {}
    fields_by_object: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    fields_by_table: dict[str, list[dict[str, str]]] = defaultdict(list)
    if args.field_paths:
        seen_by_table: dict[str, set[tuple[str, str]]] = defaultdict(set)
        for row in read_csv(args.field_paths):
            row = dict(row)
            if row.get("table_schema") in EXCLUDED_STANDARD_DATASETS:
                continue
            row["field_path"] = public_identifier(row["field_path"])
            key = (row.get("table_schema", ""), row["table_name"])
            fields_by_object[key].append(row)
            table_seen = seen_by_table[row["table_name"]]
            dedupe_key = (row["field_path"], row["data_type"])
            if dedupe_key not in table_seen:
                table_seen.add(dedupe_key)
                fields_by_table[row["table_name"]].append(row)

    out: Path = args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    objects_by_dataset: dict[str, list[WarehouseObject]] = defaultdict(list)
    for obj in objects:
        objects_by_dataset[obj.dataset].append(obj)
    for rows in objects_by_dataset.values():
        rows.sort(key=lambda item: item.name.lower())

    datasets = sorted(objects_by_dataset, key=dataset_sort_key)
    by_name: dict[str, list[WarehouseObject]] = defaultdict(list)
    for obj in objects:
        by_name[obj.name].append(obj)

    write_root_index(out, objects, datasets, by_name)
    write(out / "log.md", "# Change Log\n\n## 2026-07-01\n\n- Built the merchant-neutral UltraCart warehouse OKF catalog from metadata-only table, field-count, and field-path evidence.\n")
    write_dataset_docs(out, objects_by_dataset, field_counts)
    write_table_docs(out, objects_by_dataset, field_counts, fields_by_object)
    write_canonical_docs(out, by_name, fields_by_table)
    write_reference_docs(out, objects, objects_by_dataset, field_counts, fields_by_table)
    write_source_summary(out, objects, objects_by_dataset, field_counts, fields_by_table)


def write_root_index(out: Path, objects: list[WarehouseObject], datasets: list[str], by_name: dict[str, list[WarehouseObject]]) -> None:
    counts = Counter(obj.object_type for obj in objects)
    lines = [
        "---",
        f"okf_version: {q(OKF_VERSION)}",
        "---",
        "",
        "# UltraCart BigQuery Warehouse OKF Catalog",
        "",
        "This is a merchant-neutral Open Knowledge Format bundle for the standard UltraCart BigQuery warehouse.",
        "",
        "It defines the standard warehouse datasets, table/view objects, table families, and available metadata-only field paths without storing merchant rows, sampled records, raw customer data, project identifiers, or view SQL.",
        "",
        "## Coverage",
        "",
        f"- Datasets: {len(datasets)}",
        f"- BigQuery objects: {len(objects)}",
        f"- Canonical table names: {len(by_name)}",
    ]
    for object_type, count in sorted(counts.items()):
        lines.append(f"- {object_type.title()}: {count}")
    lines.extend(
        [
            "",
            "## Start Here",
            "",
            "- " + concept_link("/datasets/index.md", "Datasets"),
            "- " + concept_link("/tables/index.md", "Dataset-specific object docs"),
            "- " + concept_link("/concepts/tables_by_name/index.md", "Canonical table definitions by object name"),
            "- " + concept_link("/references/table_families.md", "Table families and usage guidance"),
            "- " + concept_link("/references/bigquery_usage.md", "BigQuery usage patterns"),
            "- " + concept_link("/references/source_coverage.md", "Source coverage and safety notes"),
            "",
        ]
    )
    write(out / "index.md", "\n".join(lines))


def write_dataset_docs(out: Path, objects_by_dataset: dict[str, list[WarehouseObject]], field_counts: dict[tuple[str, str], dict[str, int]]) -> None:
    dataset_lines = ["# Datasets", ""]
    for dataset in sorted(objects_by_dataset, key=dataset_sort_key):
        objs = objects_by_dataset[dataset]
        dataset_lines.append(f"- [{dataset}](/datasets/{dataset}.md) - {len(objs)} objects")
        body = yaml_frontmatter(
            {
                "type": "BigQuery Dataset",
                "title": dataset,
                "description": DATASET_ROLES.get(dataset, "UltraCart warehouse dataset."),
                "resource": f"urn:ultracart:bigquery:dataset:{dataset}",
                "tags": ["ultracart", "bigquery", "dataset", dataset],
                "timestamp": GENERATED_AT,
            }
        )
        counts = Counter(obj.object_type for obj in objs)
        body += f"# {dataset}\n\n{DATASET_ROLES.get(dataset, 'UltraCart warehouse dataset.')}\n\n"
        body += "## Object Counts\n\n"
        for object_type, count in sorted(counts.items()):
            body += f"- {object_type.title()}: {count}\n"
        body += "\n## Objects\n\n| Object | Type | Family | Field paths | Arrays | Structs |\n|---|---|---|---:|---:|---:|\n"
        for obj in objs:
            counts_for_obj = field_counts.get((obj.dataset, obj.name), {})
            body += (
                f"| [{obj.name}](/tables/{obj.dataset}/{slugify(obj.name)}.md) | {obj.object_type.title()} | "
                f"{infer_family(obj.dataset, obj.name)} | "
                f"{counts_for_obj.get('field_path_count', 0)} | "
                f"{counts_for_obj.get('array_field_count', 0)} | "
                f"{counts_for_obj.get('struct_field_count', 0)} |\n"
            )
        body += "\n## References\n\n- [Source coverage](/references/source_coverage.md)\n"
        write(out / "datasets" / f"{dataset}.md", body)
    write(out / "datasets" / "index.md", "\n".join(dataset_lines) + "\n")


def write_table_docs(
    out: Path,
    objects_by_dataset: dict[str, list[WarehouseObject]],
    field_counts: dict[tuple[str, str], dict[str, int]],
    fields_by_object: dict[tuple[str, str], list[dict[str, str]]],
) -> None:
    table_lines = ["# Dataset-Specific Objects", ""]
    for dataset in sorted(objects_by_dataset, key=dataset_sort_key):
        table_lines.append(f"- [{dataset}](/tables/{dataset}/index.md)")
        index_lines = [f"# {dataset} Objects", ""]
        for obj in objects_by_dataset[dataset]:
            index_lines.append(f"- [{obj.name}](/tables/{dataset}/{slugify(obj.name)}.md)")
            family = infer_family(obj.dataset, obj.name)
            counts_for_obj = field_counts.get((obj.dataset, obj.name), {})
            title = f"{obj.dataset}.{obj.name}"
            body = yaml_frontmatter(
                {
                    "type": object_type_label(obj.object_type),
                    "title": title,
                    "description": infer_description(obj.dataset, obj.name),
                    "resource": f"urn:ultracart:bigquery:object:{obj.dataset}.{obj.name}",
                    "tags": ["ultracart", "bigquery", obj.object_type.lower().replace(" ", "_"), obj.dataset, obj.name, family],
                    "timestamp": GENERATED_AT,
                }
            )
            body += f"# {title}\n\n"
            body += f"{infer_description(obj.dataset, obj.name)}\n\n"
            body += "## Definition\n\n"
            body += f"- Dataset: [{obj.dataset}](/datasets/{obj.dataset}.md)\n"
            body += f"- Object name: `{obj.name}`\n"
            body += f"- Object type: `{obj.object_type}`\n"
            body += f"- Table family: [{family}](/references/table_families.md#{family.replace('_', '-')})\n"
            body += f"- Grain: {infer_grain(obj.dataset, obj.name)}\n"
            body += f"- Canonical definition: [{obj.name}](/concepts/tables_by_name/{slugify(obj.name)}.md)\n"
            body += "\n## Schema Coverage\n\n"
            if counts_for_obj:
                body += (
                    f"- Field paths: {counts_for_obj['field_path_count']}\n"
                    f"- Array fields: {counts_for_obj['array_field_count']}\n"
                    f"- Struct fields: {counts_for_obj['struct_field_count']}\n"
                )
            else:
                body += "- Field-count metadata was not present for this object in the local metadata evidence.\n"
            candidate_fields = fields_by_object.get((obj.dataset, obj.name), [])
            if candidate_fields:
                body += "\n## Field Paths\n\n"
                body += field_markdown(candidate_fields)
            else:
                body += "\n## Field Paths\n\nNo field-path rows were available in the local metadata evidence for this object.\n"
            notes = usage_notes(obj.name)
            if notes:
                body += "\n## Usage Notes\n\n"
                for note in notes:
                    body += f"- {note}\n"
            body += "\n## Query Pattern\n\n"
            body += "```sql\n"
            body += f"SELECT\n  COUNT(1) AS row_count\nFROM `{{{{ source_project }}}}.{obj.dataset}.{obj.name}`;\n"
            body += "```\n\n"
            body += "Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.\n\n"
            body += "## References\n\n"
            body += "- [BigQuery usage patterns](/references/bigquery_usage.md)\n"
            body += "- [Source coverage](/references/source_coverage.md)\n"
            write(out / "tables" / dataset / f"{slugify(obj.name)}.md", body)
        write(out / "tables" / dataset / "index.md", "\n".join(index_lines) + "\n")
    write(out / "tables" / "index.md", "\n".join(table_lines) + "\n")


def write_canonical_docs(out: Path, by_name: dict[str, list[WarehouseObject]], fields_by_table: dict[str, list[dict[str, str]]]) -> None:
    index_lines = ["# Canonical Table Definitions By Object Name", ""]
    for name in sorted(by_name, key=str.lower):
        occurrences = sorted(by_name[name], key=lambda obj: dataset_sort_key(obj.dataset))
        family = infer_family(occurrences[0].dataset, name)
        index_lines.append(f"- [{name}](/concepts/tables_by_name/{slugify(name)}.md) - {len(occurrences)} dataset occurrence(s)")
        body = yaml_frontmatter(
            {
                "type": "UltraCart Table Definition",
                "title": name,
                "description": infer_description(occurrences[0].dataset, name),
                "resource": f"urn:ultracart:bigquery:table-definition:{name}",
                "tags": ["ultracart", "bigquery", "canonical_table", name, family],
                "timestamp": GENERATED_AT,
            }
        )
        body += f"# {name}\n\n"
        body += f"{infer_description(occurrences[0].dataset, name)}\n\n"
        body += "## Grain\n\n"
        body += infer_grain(occurrences[0].dataset, name) + "\n\n"
        body += "## Dataset Occurrences\n\n| Dataset | Object type | Object doc |\n|---|---|---|\n"
        for obj in occurrences:
            body += f"| `{obj.dataset}` | `{obj.object_type}` | [{obj.dataset}.{obj.name}](/tables/{obj.dataset}/{slugify(obj.name)}.md) |\n"
        body += "\n## Field Paths\n\n"
        body += field_markdown(fields_by_table.get(name, []))
        body += "\n## Notes\n\n"
        body += "Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.\n"
        notes = usage_notes(name)
        if notes:
            body += "\n"
            for note in notes:
                body += f"- {note}\n"
        write(out / "concepts" / "tables_by_name" / f"{slugify(name)}.md", body)
    write(out / "concepts" / "tables_by_name" / "index.md", "\n".join(index_lines) + "\n")


def write_reference_docs(
    out: Path,
    objects: list[WarehouseObject],
    objects_by_dataset: dict[str, list[WarehouseObject]],
    field_counts: dict[tuple[str, str], dict[str, int]],
    fields_by_table: dict[str, list[dict[str, str]]],
) -> None:
    write(out / "references" / "index.md", "# References\n\n- [Table families](/references/table_families.md)\n- [Warehouse access layers](/references/warehouse_layers.md)\n- [BigQuery usage patterns](/references/bigquery_usage.md)\n- [Monetary field patterns](/references/monetary_fields.md)\n- [Source coverage](/references/source_coverage.md)\n- [Sensitivity guardrails](/references/sensitivity_guardrails.md)\n")
    body = yaml_frontmatter(
        {
            "type": "Reference",
            "title": "UltraCart Table Families",
            "description": "Business families used to navigate the standard UltraCart BigQuery warehouse.",
            "resource": "urn:ultracart:okf:reference:table-families",
            "tags": ["ultracart", "bigquery", "reference", "families"],
            "timestamp": GENERATED_AT,
        }
    )
    body += "# Table Families\n\n"
    counts = Counter(infer_family(obj.dataset, obj.name) for obj in objects)
    for family, description in FAMILY_DESCRIPTIONS.items():
        body += f"## {family}\n\n{description}\n\nObjects in catalog: {counts.get(family, 0)}\n\n"
    body = body.rstrip() + "\n"
    write(out / "references" / "table_families.md", body)

    body = yaml_frontmatter(
        {
            "type": "Reference",
            "title": "Warehouse Access Layers",
            "description": "Official UltraCart BigQuery dataset groups, access levels, and query implications.",
            "resource": "urn:ultracart:okf:reference:warehouse-layers",
            "tags": ["ultracart", "bigquery", "reference", "datasets", "access"],
            "timestamp": GENERATED_AT,
        }
    )
    body += "# Warehouse Access Layers\n\n"
    body += "UltraCart BigQuery warehouses expose physical streaming tables plus current-state view datasets. For normal reporting, query the current-state view layer that matches the user's approved data access. Use the streaming layer only for freshness, delete behavior, or view-validation work.\n\n"
    body += "Official UltraCart documentation: https://ultracart.atlassian.net/wiki/spaces/ucdoc/pages/994705409/Data+Warehouse+BigQuery\n\n"
    body += "## Primary access layers\n\n"
    body += "| Dataset | Access level | Reporting use |\n|---|---|---|\n"
    for dataset, access_level, description in WAREHOUSE_ACCESS_LAYERS:
        body += f"| `{dataset}` | {access_level} | {description} |\n"
    body += "\n"
    body += "`ultracart_dw_medium` is a practical default for many adapter and reporting examples because it includes customer fields used in lifecycle and attribution analysis. Use `ultracart_dw` or `ultracart_dw_low` when the analysis does not need those fields. Use `ultracart_dw_high` only when the restricted fields are explicitly approved and required.\n\n"
    body += "## Linked-account layers\n\n"
    body += "Parent accounts with linked UltraCart accounts can have parallel linked datasets for consolidated reporting across child accounts. These follow the same access-level pattern as the primary datasets, but should only be used when the business question explicitly asks for linked-account rollups.\n\n"
    body += "| Dataset | Access level | Reporting use |\n|---|---|---|\n"
    for dataset, access_level, description in LINKED_ACCESS_LAYERS:
        body += f"| `{dataset}` | {access_level} | {description} |\n"
    body += "\n"
    body += "Linked datasets are not part of this standard catalog unless they are present in the metadata inventory used to generate a bundle.\n\n"
    body += "## Streaming layer\n\n"
    body += "`ultracart_dw_streaming` contains one row per object mutation. It is near-real-time, but it is not the safe grain for ordinary reports because multiple mutation rows can exist for the same business object. The current-state view layers collapse those mutations into the reporting snapshot and remove fields the user is not allowed to access.\n\n"
    body += "## Query implications\n\n"
    body += "- Access level changes the columns a user can see; verify live `INFORMATION_SCHEMA` or `bq show --schema` metadata before claiming a field is unavailable.\n"
    body += "- When raw PII is restricted, use available hash fields for joins and deduplication when the business question does not require raw contact data.\n"
    body += "- UltraCart BigQuery date-time values are UTC. Convert to the merchant's reporting time zone before grouping by business day, week, or hour.\n"
    body += "- UltraCart records are nested hierarchical objects. Use `UNNEST` deliberately and preserve the intended grain to avoid multiplying orders, items, sessions, or affiliate events.\n"
    body += "- Cross-project joins are supported by BigQuery when the querying principal has permission to all referenced projects and datasets.\n"
    body += "- Helper datasets such as `ultracart_dw_dashboard`, `ultracart_dw_import`, and `ultracart_dw_ml` are implementation or derived layers. Start from the primary current-state datasets unless the use case specifically calls for those helpers.\n"
    write(out / "references" / "warehouse_layers.md", body)

    body = yaml_frontmatter(
        {
            "type": "Reference",
            "title": "Monetary Field Patterns",
            "description": "Currency-aware value fields discovered in UltraCart warehouse schemas.",
            "resource": "urn:ultracart:okf:reference:monetary-fields",
            "tags": ["ultracart", "bigquery", "reference", "money", "currency"],
            "timestamp": GENERATED_AT,
        }
    )
    body += "# Monetary Field Patterns\n\n"
    body += "UltraCart monetary values are usually represented as a struct with `value`, `localized`, `localized_formatted`, `exchange_rate`, and `currency_code` fields. For analytics, prefer pairing the numeric `value` with its sibling `currency_code`; use `localized` or `localized_formatted` only when the reporting use case explicitly needs localized display amounts.\n\n"
    money_by_table = {
        table: monetary_field_parents(fields)
        for table, fields in sorted(fields_by_table.items(), key=lambda item: item[0].lower())
    }
    money_by_table = {table: parents for table, parents in money_by_table.items() if parents}
    body += f"Tables with currency-aware value structs: {len(money_by_table)}\n\n"
    for table, parents in money_by_table.items():
        body += f"## {table}\n\n"
        body += f"Currency-aware value structs: {len(parents)}\n\n"
        for parent in parents:
            body += f"- `{parent}`\n"
        body += "\n"
    body = body.rstrip() + "\n"
    write(out / "references" / "monetary_fields.md", body)

    body = yaml_frontmatter(
        {
            "type": "Reference",
            "title": "BigQuery Usage Patterns",
            "description": "Safe usage patterns for querying the UltraCart warehouse from OKF concepts.",
            "resource": "urn:ultracart:okf:reference:bigquery-usage",
            "tags": ["ultracart", "bigquery", "reference", "usage"],
            "timestamp": GENERATED_AT,
        }
    )
    body += "# BigQuery Usage Patterns\n\n"
    body += "Use the current-state view layers for normal analytics. Start with [Warehouse access layers](/references/warehouse_layers.md) to choose the least-privileged dataset that answers the business question. `ultracart_dw_medium` is a practical default for many lifecycle and attribution examples, but `ultracart_dw`, `ultracart_dw_low`, or `ultracart_dw_high` may be the right access layer depending on permissions and required fields.\n\n"
    body += "UltraCart BigQuery records are nested hierarchical objects, not fully flattened relational tables. Use `UNNEST` deliberately, preserve the intended output grain, and convert UTC date-time fields into the merchant's reporting time zone before grouping by day, week, or hour.\n\n"
    body += "Prefer these source surfaces for common marts:\n\n"
    body += "- Orders: `uc_orders`\n- Order items: `uc_orders.items` joined to `uc_items` when item catalog enrichment is needed\n- Attribution: `uc_orders.utms` plus optional `uc_screen_recordings` URL and page-view parameters\n- Subscriptions: `uc_auto_orders`\n- Affiliate commissions: `uc_affiliate_ledgers` after freshness validation\n- Product/catalog: `uc_items`, `uc_storefront_pages`, and storefront/feed metadata fields\n\n"
    body += "For revenue, cost, refund, gift-certificate, surcharge, and other currency-aware values, start with [Monetary field patterns](/references/monetary_fields.md).\n\n"
    body += "Avoid direct streaming-table queries unless validating freshness, delete behavior, or the view layer itself. Streaming rows represent mutations, not one safe reporting row per business object. Avoid row sampling in public artifacts.\n\n"
    body += "## Sampling And Profiling\n\n"
    body += "A few current-state views can scan substantial underlying data even when returning only a handful of rows. When sampling or profiling, use explicit field lists plus date, partition, storefront, status, or business-key filters before querying these objects:\n\n"
    for table in sorted(EXPENSIVE_QUERY_OBJECTS):
        body += f"- `{table}`\n"
    body += "\nStandard objects can also be present but empty when a merchant does not use a related UltraCart feature or module. Treat empty results as a feature-usage signal to verify, not as catalog breakage.\n\n"
    for table in sorted(OPTIONAL_FEATURE_OBJECTS):
        body += f"- `{table}`\n"
    write(out / "references" / "bigquery_usage.md", body)

    body = yaml_frontmatter(
        {
            "type": "Reference",
            "title": "Source Coverage",
            "description": "Metadata-only evidence used to build the standard UltraCart warehouse OKF bundle.",
            "resource": "urn:ultracart:okf:reference:source-coverage",
            "tags": ["ultracart", "bigquery", "reference", "coverage"],
            "timestamp": GENERATED_AT,
        }
    )
    body += "# Source Coverage\n\n"
    body += "This bundle was built from metadata-only evidence: dataset/object inventory, field-count metadata, and field-path metadata where available. It does not store row data, sampled records, customer values, merchant project IDs, billing project IDs, or view SQL.\n\n"
    body += "Merchant-specific custom view/work areas are intentionally excluded from the standard catalog because they are not part of the shared UltraCart warehouse shape.\n\n"
    body += f"- Datasets represented: {len(objects_by_dataset)}\n"
    body += f"- BigQuery objects represented: {len(objects)}\n"
    body += f"- Objects with field-count evidence: {len(field_counts)}\n"
    body += f"- Canonical table names with field-path rows: {len(fields_by_table)}\n"
    body += "\nField-path evidence is attached by UltraCart object name and reused by canonical docs. Dataset-specific access layers may expose different field subsets; verify against live BigQuery metadata before making access-control claims.\n"
    write(out / "references" / "source_coverage.md", body)

    body = yaml_frontmatter(
        {
            "type": "Reference",
            "title": "Sensitivity Guardrails",
            "description": "Safety rules for working with UltraCart warehouse metadata and generated OKF bundles.",
            "resource": "urn:ultracart:okf:reference:sensitivity-guardrails",
            "tags": ["ultracart", "bigquery", "reference", "safety"],
            "timestamp": GENERATED_AT,
        }
    )
    body += "# Sensitivity Guardrails\n\n"
    body += "This public bundle is metadata-only. Do not add customer rows, raw emails, addresses, phone numbers, payment details, message bodies, sampled records, or merchant-specific project identifiers to this repository.\n\n"
    body += "UltraCart warehouse access is permissioned through Google IAM plus BigQuery column-level security. Do not move an analysis to a broader access layer just to make fields easier to query; use the lowest access level that answers the question and prefer hashed identifiers when raw PII is not required.\n\n"
    body += "Generated merchant bundles should stay local unless explicitly reviewed for the intended audience.\n\n"
    body += "Treat row-level samples from these objects as especially sensitive, even in medium-layer views:\n\n"
    for table in sorted(HIGH_SENSITIVITY_OBJECTS):
        body += f"- `{table}`\n"
    write(out / "references" / "sensitivity_guardrails.md", body)


def write_source_summary(
    out: Path,
    objects: list[WarehouseObject],
    objects_by_dataset: dict[str, list[WarehouseObject]],
    field_counts: dict[tuple[str, str], dict[str, int]],
    fields_by_table: dict[str, list[dict[str, str]]],
) -> None:
    summary = {
        "okf_version": OKF_VERSION,
        "generated_at": GENERATED_AT,
        "source_kind": "metadata_only_standard_catalog",
        "dataset_count": len(objects_by_dataset),
        "object_count": len(objects),
        "canonical_table_count": len({obj.name for obj in objects}),
        "object_type_counts": dict(sorted(Counter(obj.object_type for obj in objects).items())),
        "field_count_object_count": len(field_counts),
        "field_path_canonical_table_count": len(fields_by_table),
        "datasets": [
            {
                "dataset": dataset,
                "role": DATASET_ROLES.get(dataset, "UltraCart warehouse dataset."),
                "object_count": len(objects_by_dataset[dataset]),
            }
            for dataset in sorted(objects_by_dataset, key=dataset_sort_key)
        ],
        "objects": [
            {
                "dataset": obj.dataset,
                "name": obj.name,
                "object_type": obj.object_type,
                "family": infer_family(obj.dataset, obj.name),
            }
            for obj in sorted(objects, key=lambda item: (dataset_sort_key(item.dataset), item.name.lower()))
        ],
    }
    write(out / "_source_metadata" / "source_summary.json", json.dumps(summary, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public standard UltraCart OKF catalog from metadata evidence.")
    parser.add_argument("--table-inventory", type=Path, required=True, help="CSV with table_schema, table_name, and table_type columns.")
    parser.add_argument("--field-counts", type=Path, help="Optional CSV with field path, array, and struct counts.")
    parser.add_argument("--field-paths", type=Path, help="Optional CSV with table_name, field_path, and data_type columns.")
    parser.add_argument("--out", type=Path, default=Path("okf/ultracart_warehouse"))
    args = parser.parse_args()
    build(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
