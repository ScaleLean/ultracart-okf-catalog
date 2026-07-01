---
type: "UltraCart Table Definition"
title: "customer_auto_orders_365_90"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:table-definition:customer_auto_orders_365_90"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "customer_auto_orders_365_90"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# customer_auto_orders_365_90

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Grain

Derived customer-modeling or machine-learning feature grain; inspect fields before joining.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_ml` | `BASE TABLE` | [ultracart_dw_ml.customer_auto_orders_365_90](/tables/ultracart_dw_ml/customer_auto_orders_365_90.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `active_count` | `INTEGER` |
| `email_hash` | `STRING` |
| `rebill_count` | `INTEGER` |
| `rebill_total_revenue` | `FLOAT` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
