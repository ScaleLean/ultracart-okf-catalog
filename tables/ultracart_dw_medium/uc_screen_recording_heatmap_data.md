---
type: "BigQuery View"
title: "ultracart_dw_medium.uc_screen_recording_heatmap_data"
description: "Heatmap and click-position support data for session behavior analysis."
resource: "urn:ultracart:bigquery:object:ultracart_dw_medium.uc_screen_recording_heatmap_data"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_medium"
  - "uc_screen_recording_heatmap_data"
  - "attribution_sessions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_medium.uc_screen_recording_heatmap_data

Heatmap and click-position support data for session behavior analysis.

## Definition

- Dataset: [ultracart_dw_medium](/datasets/ultracart_dw_medium.md)
- Object name: `uc_screen_recording_heatmap_data`
- Object type: `VIEW`
- Table family: [attribution_sessions](/references/table_families.md#attribution-sessions)
- Grain: One heatmap support row per screen_recording_heatmap_data_oid.
- Canonical definition: [uc_screen_recording_heatmap_data](/concepts/tables_by_name/uc_screen_recording_heatmap_data.md)

## Schema Coverage

- Field paths: 16
- Array fields: 3
- Struct fields: 3

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_medium.uc_screen_recording_heatmap_data`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
