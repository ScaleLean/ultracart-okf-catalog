---
type: "UltraCart Table Definition"
title: "uc_integration_logs"
description: "Integration event log with raw content redacted in standard views."
resource: "urn:ultracart:bigquery:table-definition:uc_integration_logs"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_integration_logs"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_integration_logs

Integration event log with raw content redacted in standard views.

## Grain

One integration log row per integration_log_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_integration_logs](/tables/ultracart_dw/uc_integration_logs.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_integration_logs](/tables/ultracart_dw_low/uc_integration_logs.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_integration_logs](/tables/ultracart_dw_medium/uc_integration_logs.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_integration_logs](/tables/ultracart_dw_high/uc_integration_logs.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `action` | `STRING` |
| `attributes` | `ARRAY<STRUCT>` |
| `attributes.name` | `STRING` |
| `auto_order_oids` | `ARRAY<STRUCT>` |
| `auto_order_oids.value` | `INTEGER` |
| `direction` | `STRING` |
| `files` | `ARRAY<STRUCT>` |
| `files.mime_type` | `STRING` |
| `files.name` | `STRING` |
| `files.size` | `INTEGER` |
| `files.uuid` | `STRING` |
| `integration_log_oid` | `INTEGER` |
| `item_id` | `STRING` |
| `item_ipn_oid` | `INTEGER` |
| `log_dts` | `DATETIME` |
| `log_map_entries` | `ARRAY<STRUCT>` |
| `log_map_entries.key` | `STRING` |
| `log_type` | `STRING` |
| `logger_id` | `STRING` |
| `logger_name` | `STRING` |
| `merchant_id` | `STRING` |
| `order_ids` | `ARRAY<STRUCT>` |
| `order_ids.value` | `STRING` |
| `partition_date` | `DATE` |
| `pk` | `STRING` |
| `sk` | `STRING` |
| `status` | `STRING` |
| `status_code` | `INTEGER` |
| `attributes.value` | `STRING` |
| `email` | `STRING` |
| `files.content` | `BYTES` |
| `files.content_json` | `JSON` |
| `files.content_text` | `STRING` |
| `log` | `STRING` |
| `log_map_entries.value` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
