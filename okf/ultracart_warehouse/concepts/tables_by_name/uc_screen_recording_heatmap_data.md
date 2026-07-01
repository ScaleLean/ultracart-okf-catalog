---
type: "UltraCart Table Definition"
title: "uc_screen_recording_heatmap_data"
description: "Heatmap and click-position support data for session behavior analysis."
resource: "urn:ultracart:bigquery:table-definition:uc_screen_recording_heatmap_data"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_screen_recording_heatmap_data"
  - "attribution_sessions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_screen_recording_heatmap_data

Heatmap and click-position support data for session behavior analysis.

## Grain

One heatmap support row per screen_recording_heatmap_data_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_screen_recording_heatmap_data](/tables/ultracart_dw/uc_screen_recording_heatmap_data.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_screen_recording_heatmap_data](/tables/ultracart_dw_low/uc_screen_recording_heatmap_data.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_screen_recording_heatmap_data](/tables/ultracart_dw_medium/uc_screen_recording_heatmap_data.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_screen_recording_heatmap_data](/tables/ultracart_dw_high/uc_screen_recording_heatmap_data.md) |

## Field Paths

| Field path | Data type |
|---|---|
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
