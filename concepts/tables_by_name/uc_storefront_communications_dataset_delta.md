---
type: "UltraCart Table Definition"
title: "uc_storefront_communications_dataset_delta"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_communications_dataset_delta"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_communications_dataset_delta"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_communications_dataset_delta

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical change or delta row from the source ingestion stream.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_storefront_communications_dataset_delta](/tables/ultracart_dw_streaming/uc_storefront_communications_dataset_delta.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `dataset_id` | `STRING` |
| `email` | `STRING` |
| `record_json` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
