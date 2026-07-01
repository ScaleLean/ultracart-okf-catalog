---
type: "UltraCart Table Definition"
title: "model_registry"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:table-definition:model_registry"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "model_registry"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# model_registry

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Grain

Derived customer-modeling or machine-learning feature grain; inspect fields before joining.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_ml` | `BASE TABLE` | [ultracart_dw_ml.model_registry](/tables/ultracart_dw_ml/model_registry.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
