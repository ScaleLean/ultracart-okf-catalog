---
type: "BigQuery View"
title: "ultracart_dw.uc_item_inventory_history"
description: "Inventory ledger and history for audit and operational review."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_item_inventory_history"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_item_inventory_history"
  - "commerce_core"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_item_inventory_history

Inventory ledger and history for audit and operational review.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_item_inventory_history`
- Object type: `VIEW`
- Table family: [commerce_core](/references/table_families.md#commerce-core)
- Grain: One inventory event row per item_inventory_history_oid.
- Canonical definition: [uc_item_inventory_history](/concepts/tables_by_name/uc_item_inventory_history.md)

## Schema Coverage

- Field paths: 13
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
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
FROM `{{ source_project }}.ultracart_dw.uc_item_inventory_history`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
