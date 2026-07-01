---
type: "BigQuery View"
title: "ultracart_dw_low.uc_integration_logs"
description: "Integration event log with raw content redacted in standard views."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_integration_logs"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_integration_logs"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_integration_logs

Integration event log with raw content redacted in standard views.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_integration_logs`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One integration log row per integration_log_oid.
- Canonical definition: [uc_integration_logs](/concepts/tables_by_name/uc_integration_logs.md)

## Schema Coverage

- Field paths: 28
- Array fields: 5
- Struct fields: 5

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_low.uc_integration_logs`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
