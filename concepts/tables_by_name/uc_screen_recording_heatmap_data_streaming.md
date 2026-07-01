---
type: "UltraCart Table Definition"
title: "uc_screen_recording_heatmap_data_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_screen_recording_heatmap_data_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_screen_recording_heatmap_data_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_screen_recording_heatmap_data_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_screen_recording_heatmap_data.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_screen_recording_heatmap_data_streaming](/tables/ultracart_dw_streaming/uc_screen_recording_heatmap_data_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `heatmap_date` | `DATETIME` |
| `merchant_id` | `STRING` |
| `partition_date` | `DATE` |
| `screen_recording_heatmap_data_oid` | `INTEGER` |
| `screen_size` | `STRING` |
| `scroll_percentage` | `INTEGER` |
| `selectors` | `ARRAY<STRUCT>` |
| `selectors.clicks` | `ARRAY<STRUCT>` |
| `selectors.clicks.xp` | `INTEGER` |
| `selectors.clicks.yp` | `INTEGER` |
| `selectors.movements` | `ARRAY<STRUCT>` |
| `selectors.movements.xp` | `INTEGER` |
| `selectors.movements.yp` | `INTEGER` |
| `selectors.selector` | `STRING` |
| `storefront_oid` | `INTEGER` |
| `url` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
