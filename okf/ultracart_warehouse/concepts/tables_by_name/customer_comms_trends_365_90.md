---
type: "UltraCart Table Definition"
title: "customer_comms_trends_365_90"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:table-definition:customer_comms_trends_365_90"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "customer_comms_trends_365_90"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# customer_comms_trends_365_90

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Grain

Derived customer-modeling or machine-learning feature grain; inspect fields before joining.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_ml` | `BASE TABLE` | [ultracart_dw_ml.customer_comms_trends_365_90](/tables/ultracart_dw_ml/customer_comms_trends_365_90.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
