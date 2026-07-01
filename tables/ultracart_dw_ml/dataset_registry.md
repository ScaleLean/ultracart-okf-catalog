---
type: "BigQuery Table"
title: "ultracart_dw_ml.dataset_registry"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:object:ultracart_dw_ml.dataset_registry"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_ml"
  - "dataset_registry"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_ml.dataset_registry

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Definition

- Dataset: [ultracart_dw_ml](/datasets/ultracart_dw_ml.md)
- Object name: `dataset_registry`
- Object type: `BASE TABLE`
- Table family: [ml](/references/table_families.md#ml)
- Grain: Derived customer-modeling or machine-learning feature grain; inspect fields before joining.
- Canonical definition: [dataset_registry](/concepts/tables_by_name/dataset_registry.md)

## Schema Coverage

- Field paths: 9
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `compression_method` | `STRING` |
| `creation_dts` | `DATETIME` |
| `gcs_path` | `STRING` |
| `name` | `STRING` |
| `num_rows` | `INTEGER` |
| `observation_window` | `INTEGER` |
| `prediction_period` | `INTEGER` |
| `storefront_oid` | `INTEGER` |
| `version` | `INTEGER` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_ml.dataset_registry`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
