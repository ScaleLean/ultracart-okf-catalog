---
type: "BigQuery Table"
title: "ultracart_dw_ml.customer_tower_data"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:object:ultracart_dw_ml.customer_tower_data"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_ml"
  - "customer_tower_data"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_ml.customer_tower_data

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Definition

- Dataset: [ultracart_dw_ml](/datasets/ultracart_dw_ml.md)
- Object name: `customer_tower_data`
- Object type: `BASE TABLE`
- Table family: [ml](/references/table_families.md#ml)
- Grain: Derived customer-modeling or machine-learning feature grain; inspect fields before joining.
- Canonical definition: [customer_tower_data](/concepts/tables_by_name/customer_tower_data.md)

## Schema Coverage

- Field paths: 12
- Array fields: 0
- Struct fields: 0

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_ml.customer_tower_data`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
