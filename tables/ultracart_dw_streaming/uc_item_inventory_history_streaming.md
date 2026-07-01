---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_item_inventory_history_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_item_inventory_history_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_item_inventory_history_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_item_inventory_history_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_item_inventory_history_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_item_inventory_history.
- Canonical definition: [uc_item_inventory_history_streaming](/concepts/tables_by_name/uc_item_inventory_history_streaming.md)

## Schema Coverage

- Field paths: 15
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `adjustment` | `NUMERIC` |
| `after_inventory_level` | `NUMERIC` |
| `before_inventory_level` | `NUMERIC` |
| `distribution_center_code` | `STRING` |
| `distribution_center_oid` | `INTEGER` |
| `history_dts` | `DATETIME` |
| `item_inventory_history_oid` | `INTEGER` |
| `merchant_id` | `STRING` |
| `merchant_item_id` | `STRING` |
| `merchant_item_oid` | `INTEGER` |
| `order_id` | `STRING` |
| `partition_oid` | `INTEGER` |
| `reason` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_item_inventory_history_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
