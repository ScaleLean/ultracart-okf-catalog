---
type: "BigQuery Table"
title: "ultracart_dw_ml.model_registry"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:object:ultracart_dw_ml.model_registry"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_ml"
  - "model_registry"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_ml.model_registry

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Definition

- Dataset: [ultracart_dw_ml](/datasets/ultracart_dw_ml.md)
- Object name: `model_registry`
- Object type: `BASE TABLE`
- Table family: [ml](/references/table_families.md#ml)
- Grain: Derived customer-modeling or machine-learning feature grain; inspect fields before joining.
- Canonical definition: [model_registry](/concepts/tables_by_name/model_registry.md)

## Schema Coverage

- Field paths: 12
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `creation_dts` | `DATETIME` |
| `dataset_gcs_path` | `STRING` |
| `dataset_name` | `STRING` |
| `dataset_version` | `INTEGER` |
| `gcs_path` | `STRING` |
| `mse` | `FLOAT` |
| `name` | `STRING` |
| `observation_window` | `INTEGER` |
| `prediction_period` | `INTEGER` |
| `rmse` | `FLOAT` |
| `storefront_oid` | `INTEGER` |
| `version` | `INTEGER` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_ml.model_registry`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
