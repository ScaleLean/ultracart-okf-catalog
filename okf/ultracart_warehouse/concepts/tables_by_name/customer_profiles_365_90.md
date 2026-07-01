---
type: "UltraCart Table Definition"
title: "customer_profiles_365_90"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:table-definition:customer_profiles_365_90"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "customer_profiles_365_90"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# customer_profiles_365_90

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Grain

Derived customer-modeling or machine-learning feature grain; inspect fields before joining.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_ml` | `BASE TABLE` | [ultracart_dw_ml.customer_profiles_365_90](/tables/ultracart_dw_ml/customer_profiles_365_90.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `current_loyalty_points` | `INTEGER` |
| `email_hash` | `STRING` |
| `loyalty_ledger_entries_count` | `INTEGER` |
| `loyalty_redemptions_count` | `INTEGER` |
| `review_count` | `INTEGER` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
