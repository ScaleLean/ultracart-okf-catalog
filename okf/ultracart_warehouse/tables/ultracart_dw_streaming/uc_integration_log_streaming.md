---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_integration_log_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_integration_log_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_integration_log_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_integration_log_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_integration_log_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_integration_log.
- Canonical definition: [uc_integration_log_streaming](/concepts/tables_by_name/uc_integration_log_streaming.md)

## Schema Coverage

- Field paths: 37
- Array fields: 5
- Struct fields: 5

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_integration_log_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
