---
type: "UltraCart Table Definition"
title: "dataset_registry"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:table-definition:dataset_registry"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "dataset_registry"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# dataset_registry

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Grain

Derived customer-modeling or machine-learning feature grain; inspect fields before joining.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_ml` | `BASE TABLE` | [ultracart_dw_ml.dataset_registry](/tables/ultracart_dw_ml/dataset_registry.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
