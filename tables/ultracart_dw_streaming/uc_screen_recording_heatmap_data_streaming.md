---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_screen_recording_heatmap_data_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_screen_recording_heatmap_data_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_screen_recording_heatmap_data_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_screen_recording_heatmap_data_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_screen_recording_heatmap_data_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_screen_recording_heatmap_data.
- Canonical definition: [uc_screen_recording_heatmap_data_streaming](/concepts/tables_by_name/uc_screen_recording_heatmap_data_streaming.md)

## Schema Coverage

- Field paths: 18
- Array fields: 3
- Struct fields: 3

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_screen_recording_heatmap_data_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
