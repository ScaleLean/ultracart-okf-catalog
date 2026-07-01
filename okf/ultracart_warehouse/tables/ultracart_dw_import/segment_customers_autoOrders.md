---
type: "BigQuery View"
title: "ultracart_dw_import.segment_customers_autoOrders"
description: "Imported or legacy segmentation helper object."
resource: "urn:ultracart:bigquery:object:ultracart_dw_import.segment_customers_autoOrders"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_import"
  - "segment_customers_autoOrders"
  - "import"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_import.segment_customers_autoOrders

Imported or legacy segmentation helper object.

## Definition

- Dataset: [ultracart_dw_import](/datasets/ultracart_dw_import.md)
- Object name: `segment_customers_autoOrders`
- Object type: `VIEW`
- Table family: [import](/references/table_families.md#import)
- Grain: Imported helper grain defined by the source import or segmentation view.
- Canonical definition: [segment_customers_autoOrders](/concepts/tables_by_name/segment_customers_autoOrders.md)

## Schema Coverage

- Field paths: 6
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `completed_orders_count` | `INTEGER` |
| `creation_dts` | `DATETIME` |
| `email` | `STRING` |
| `enabled` | `BOOLEAN` |
| `last_canceled_dts` | `DATETIME` |
| `product_category` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_import.segment_customers_autoOrders`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
