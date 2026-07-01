---
type: "BigQuery Table"
title: "ultracart_dw_ml.customer_comms_trends_365_90"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:object:ultracart_dw_ml.customer_comms_trends_365_90"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_ml"
  - "customer_comms_trends_365_90"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_ml.customer_comms_trends_365_90

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Definition

- Dataset: [ultracart_dw_ml](/datasets/ultracart_dw_ml.md)
- Object name: `customer_comms_trends_365_90`
- Object type: `BASE TABLE`
- Table family: [ml](/references/table_families.md#ml)
- Grain: Derived customer-modeling or machine-learning feature grain; inspect fields before joining.
- Canonical definition: [customer_comms_trends_365_90](/concepts/tables_by_name/customer_comms_trends_365_90.md)

## Schema Coverage

- Field paths: 17
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `email_hash` | `STRING` |
| `segment_end_binned_click` | `FLOAT` |
| `segment_end_binned_open` | `FLOAT` |
| `segment_end_full_click` | `FLOAT` |
| `segment_end_full_open` | `FLOAT` |
| `slope_binned_click` | `FLOAT` |
| `slope_binned_open` | `FLOAT` |
| `slope_full_click` | `FLOAT` |
| `slope_full_open` | `FLOAT` |
| `sum_squares_regression_binned_click` | `FLOAT` |
| `sum_squares_regression_binned_open` | `FLOAT` |
| `sum_squares_regression_full_click` | `FLOAT` |
| `sum_squares_regression_full_open` | `FLOAT` |
| `y_intercept_binned_click` | `FLOAT` |
| `y_intercept_binned_open` | `FLOAT` |
| `y_intercept_full_click` | `FLOAT` |
| `y_intercept_full_open` | `FLOAT` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_ml.customer_comms_trends_365_90`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
