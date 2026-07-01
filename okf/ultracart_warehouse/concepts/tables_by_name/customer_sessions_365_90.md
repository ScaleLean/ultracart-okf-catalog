---
type: "UltraCart Table Definition"
title: "customer_sessions_365_90"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:table-definition:customer_sessions_365_90"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "customer_sessions_365_90"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# customer_sessions_365_90

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Grain

Derived customer-modeling or machine-learning feature grain; inspect fields before joining.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_ml` | `BASE TABLE` | [ultracart_dw_ml.customer_sessions_365_90](/tables/ultracart_dw_ml/customer_sessions_365_90.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
