---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_storefront_customer_session_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_storefront_customer_session_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_storefront_customer_session_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_storefront_customer_session_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_storefront_customer_session_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_storefront_customer_session.
- Canonical definition: [uc_storefront_customer_session_streaming](/concepts/tables_by_name/uc_storefront_customer_session_streaming.md)

## Schema Coverage

- Field paths: 22
- Array fields: 1
- Struct fields: 1

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `end_dts` | `DATETIME` |
| `esp_customer_uuid` | `STRING` |
| `merchant_id` | `STRING` |
| `order_id` | `STRING` |
| `page_views` | `ARRAY<STRUCT>` |
| `page_views.bounce` | `BOOLEAN` |
| `page_views.start_dts` | `DATETIME` |
| `page_views.time_on_page_second` | `NUMERIC` |
| `page_views.url` | `STRING` |
| `partition_date` | `DATE` |
| `screen_recording_uuid` | `STRING` |
| `start_dts` | `DATETIME` |
| `utm_campaign` | `STRING` |
| `utm_content` | `STRING` |
| `utm_id` | `STRING` |
| `utm_medium` | `STRING` |
| `utm_source` | `STRING` |
| `utm_term` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_storefront_customer_session_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
