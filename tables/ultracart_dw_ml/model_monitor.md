---
type: "BigQuery Table"
title: "ultracart_dw_ml.model_monitor"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:object:ultracart_dw_ml.model_monitor"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_ml"
  - "model_monitor"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_ml.model_monitor

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Definition

- Dataset: [ultracart_dw_ml](/datasets/ultracart_dw_ml.md)
- Object name: `model_monitor`
- Object type: `BASE TABLE`
- Table family: [ml](/references/table_families.md#ml)
- Grain: Derived customer-modeling or machine-learning feature grain; inspect fields before joining.
- Canonical definition: [model_monitor](/concepts/tables_by_name/model_monitor.md)

## Schema Coverage

- Field paths: 11
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `creation_dts` | `DATETIME` |
| `dataset_name` | `STRING` |
| `dataset_version` | `INTEGER` |
| `model_drift` | `FLOAT` |
| `model_name` | `STRING` |
| `model_version` | `INTEGER` |
| `mse` | `FLOAT` |
| `observation_window` | `INTEGER` |
| `prediction_period` | `INTEGER` |
| `rmse` | `FLOAT` |
| `storefront_oid` | `INTEGER` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_ml.model_monitor`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
