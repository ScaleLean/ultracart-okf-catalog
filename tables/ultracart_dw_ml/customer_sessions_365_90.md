---
type: "BigQuery Table"
title: "ultracart_dw_ml.customer_sessions_365_90"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:object:ultracart_dw_ml.customer_sessions_365_90"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_ml"
  - "customer_sessions_365_90"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_ml.customer_sessions_365_90

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Definition

- Dataset: [ultracart_dw_ml](/datasets/ultracart_dw_ml.md)
- Object name: `customer_sessions_365_90`
- Object type: `BASE TABLE`
- Table family: [ml](/references/table_families.md#ml)
- Grain: Derived customer-modeling or machine-learning feature grain; inspect fields before joining.
- Canonical definition: [customer_sessions_365_90](/concepts/tables_by_name/customer_sessions_365_90.md)

## Schema Coverage

- Field paths: 26
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `days_since_last_visit` | `INTEGER` |
| `email_hash` | `STRING` |
| `page_views_per_visit` | `FLOAT` |
| `session_order_count` | `INTEGER` |
| `time_on_site_per_visit` | `FLOAT` |
| `total_page_views` | `INTEGER` |
| `total_time_on_site` | `INTEGER` |
| `utm_campaign` | `STRING` |
| `utm_source` | `STRING` |
| `visit_T` | `INTEGER` |
| `visit_frequency` | `INTEGER` |
| `visit_recency` | `INTEGER` |
| `visits_count` | `INTEGER` |
| `visits_per_day_0` | `INTEGER` |
| `visits_per_day_1` | `INTEGER` |
| `visits_per_day_2` | `INTEGER` |
| `visits_per_day_3` | `INTEGER` |
| `visits_per_day_4` | `INTEGER` |
| `visits_per_day_5` | `INTEGER` |
| `visits_per_day_6` | `INTEGER` |
| `visits_per_daypart_0` | `INTEGER` |
| `visits_per_daypart_1` | `INTEGER` |
| `visits_per_daypart_2` | `INTEGER` |
| `visits_per_daypart_3` | `INTEGER` |
| `visits_per_daypart_4` | `INTEGER` |
| `visits_per_daypart_5` | `INTEGER` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_ml.customer_sessions_365_90`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
