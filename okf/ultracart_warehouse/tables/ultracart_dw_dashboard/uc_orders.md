---
type: "BigQuery Table"
title: "ultracart_dw_dashboard.uc_orders"
description: "Order header, status, nested items, coupons, affiliates, UTMs, subscription markers, and order economics. Primary source for orders, order items, and first-pass attribution."
resource: "urn:ultracart:bigquery:object:ultracart_dw_dashboard.uc_orders"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_dashboard"
  - "uc_orders"
  - "dashboard"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_dashboard.uc_orders

Order header, status, nested items, coupons, affiliates, UTMs, subscription markers, and order economics. Primary source for orders, order items, and first-pass attribution.

## Definition

- Dataset: [ultracart_dw_dashboard](/datasets/ultracart_dw_dashboard.md)
- Object name: `uc_orders`
- Object type: `BASE TABLE`
- Table family: [dashboard](/references/table_families.md#dashboard)
- Grain: One current order row per order_id.
- Canonical definition: [uc_orders](/concepts/tables_by_name/uc_orders.md)

## Schema Coverage

- Field paths: 7
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `channel_partner_code` | `STRING` |
| `creation_dts` | `DATETIME` |
| `order_id` | `STRING` |
| `partition_date` | `DATE` |
| `payment_dts` | `DATETIME` |
| `storefront_host_name` | `STRING` |
| `total_value` | `NUMERIC` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_dashboard.uc_orders`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
