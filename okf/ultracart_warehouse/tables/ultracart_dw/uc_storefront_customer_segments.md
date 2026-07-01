---
type: "BigQuery View"
title: "ultracart_dw.uc_storefront_customer_segments"
description: "Storefront customer segment membership data."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_storefront_customer_segments"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_storefront_customer_segments"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_storefront_customer_segments

Storefront customer segment membership data.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_storefront_customer_segments`
- Object type: `VIEW`
- Table family: [customers_support](/references/table_families.md#customers-support)
- Grain: One storefront segment membership row.
- Canonical definition: [uc_storefront_customer_segments](/concepts/tables_by_name/uc_storefront_customer_segments.md)

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
| `merchant_id` | `STRING` |
| `partition_oid` | `INTEGER` |
| `segment_name` | `STRING` |
| `segment_uuid` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw.uc_storefront_customer_segments`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
