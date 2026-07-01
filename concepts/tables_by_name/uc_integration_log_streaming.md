---
type: "UltraCart Table Definition"
title: "uc_integration_log_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_integration_log_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_integration_log_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_integration_log_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_integration_log.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_integration_log_streaming](/tables/ultracart_dw_streaming/uc_integration_log_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `action` | `STRING` |
| `attributes` | `ARRAY<STRUCT>` |
| `attributes.name` | `STRING` |
| `attributes.value` | `STRING` |
| `auto_order_oids` | `ARRAY<STRUCT>` |
| `auto_order_oids.value` | `INTEGER` |
| `direction` | `STRING` |
| `email` | `STRING` |
| `files` | `ARRAY<STRUCT>` |
| `files.content` | `BYTES` |
| `files.content_json` | `JSON` |
| `files.content_text` | `STRING` |
| `files.mime_type` | `STRING` |
| `files.name` | `STRING` |
| `files.size` | `INTEGER` |
| `files.uuid` | `STRING` |
| `integration_log_oid` | `INTEGER` |
| `item_id` | `STRING` |
| `item_ipn_oid` | `INTEGER` |
| `log` | `STRING` |
| `log_dts` | `DATETIME` |
| `log_map_entries` | `ARRAY<STRUCT>` |
| `log_map_entries.key` | `STRING` |
| `log_map_entries.value` | `STRING` |
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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
