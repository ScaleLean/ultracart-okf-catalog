---
type: "UltraCart Table Definition"
title: "customer_tower_data"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:table-definition:customer_tower_data"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "customer_tower_data"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# customer_tower_data

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Grain

Derived customer-modeling or machine-learning feature grain; inspect fields before joining.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_ml` | `BASE TABLE` | [ultracart_dw_ml.customer_tower_data](/tables/ultracart_dw_ml/customer_tower_data.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `age` | `STRING` |
| `big_spender` | `STRING` |
| `deal_seeker` | `STRING` |
| `email_hash` | `STRING` |
| `financial_group` | `STRING` |
| `financial_segment` | `STRING` |
| `gender` | `STRING` |
| `household_income` | `STRING` |
| `length_of_residence` | `STRING` |
| `life_stage_group` | `STRING` |
| `life_stage_segment` | `STRING` |
| `net_worth` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
