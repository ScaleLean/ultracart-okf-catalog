---
type: "BigQuery View"
title: "ultracart_dw_low.uc_storefront_customer_lists"
description: "Storefront list membership data."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_storefront_customer_lists"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_storefront_customer_lists"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_storefront_customer_lists

Storefront list membership data.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_storefront_customer_lists`
- Object type: `VIEW`
- Table family: [customers_support](/references/table_families.md#customers-support)
- Grain: One storefront list membership row.
- Canonical definition: [uc_storefront_customer_lists](/concepts/tables_by_name/uc_storefront_customer_lists.md)

## Schema Coverage

- Field paths: 7
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `add_dts` | `DATETIME` |
| `email_hash` | `STRING` |
| `esp_customer_uuid` | `STRING` |
| `list_name` | `STRING` |
| `list_uuid` | `STRING` |
| `merchant_id` | `STRING` |
| `partition_oid` | `INTEGER` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_low.uc_storefront_customer_lists`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
