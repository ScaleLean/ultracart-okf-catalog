---
type: "BigQuery Materialized View"
title: "ultracart_dw_dashboard.uc_order_summary_mv"
description: "Dashboard rollup or materialized reporting object."
resource: "urn:ultracart:bigquery:object:ultracart_dw_dashboard.uc_order_summary_mv"
tags:
  - "ultracart"
  - "bigquery"
  - "materialized_view"
  - "ultracart_dw_dashboard"
  - "uc_order_summary_mv"
  - "dashboard"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_dashboard.uc_order_summary_mv

Dashboard rollup or materialized reporting object.

## Definition

- Dataset: [ultracart_dw_dashboard](/datasets/ultracart_dw_dashboard.md)
- Object name: `uc_order_summary_mv`
- Object type: `MATERIALIZED VIEW`
- Table family: [dashboard](/references/table_families.md#dashboard)
- Grain: Dashboard-oriented aggregate or summary grain.
- Canonical definition: [uc_order_summary_mv](/concepts/tables_by_name/uc_order_summary_mv.md)

## Schema Coverage

- Field paths: 4
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `channel` | `STRING` |
| `partition_date` | `DATE` |
| `period` | `DATETIME` |
| `total` | `NUMERIC` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_dashboard.uc_order_summary_mv`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
