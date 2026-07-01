---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_storefront_customer_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_storefront_customer_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_storefront_customer_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_storefront_customer_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_storefront_customer_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_storefront_customer.
- Canonical definition: [uc_storefront_customer_streaming](/concepts/tables_by_name/uc_storefront_customer_streaming.md)

## Schema Coverage

- Field paths: 50
- Array fields: 5
- Struct fields: 5

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `consecutive_emails_unclicked` | `INTEGER` |
| `consecutive_emails_unopened` | `INTEGER` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `emails` | `ARRAY<STRUCT>` |
| `emails.campaign_name` | `STRING` |
| `emails.clicked` | `BOOLEAN` |
| `emails.clicked_dts` | `DATETIME` |
| `emails.commseq_uuid` | `STRING` |
| `emails.converted` | `BOOLEAN` |
| `emails.email_uuid` | `STRING` |
| `emails.flow_name` | `STRING` |
| `emails.opened` | `BOOLEAN` |
| `emails.opened_dts` | `DATETIME` |
| `emails.order_id` | `STRING` |
| `emails.sent_dts` | `DATETIME` |
| `emails.spam_complaint` | `BOOLEAN` |
| `emails.spam_complaint_dts` | `DATETIME` |
| `emails.subject` | `STRING` |
| `emails.transport` | `STRING` |
| `esp_customer_uuid` | `STRING` |
| `global_unsubscribed` | `BOOLEAN` |
| `lists` | `ARRAY<STRUCT>` |
| `lists.add_dts` | `DATETIME` |
| `lists.list_name` | `STRING` |
| `lists.list_uuid` | `STRING` |
| `merchant_id` | `STRING` |
| `partition_oid` | `INTEGER` |
| `segments` | `ARRAY<STRUCT>` |
| `segments.add_dts` | `DATETIME` |
| `segments.segment_name` | `STRING` |
| `segments.segment_uuid` | `STRING` |
| `sessions` | `ARRAY<STRUCT>` |
| `sessions.end_dts` | `DATETIME` |
| `sessions.order_id` | `STRING` |
| `sessions.page_views` | `ARRAY<STRUCT>` |
| `sessions.page_views.bounce` | `BOOLEAN` |
| `sessions.page_views.start_dts` | `DATETIME` |
| `sessions.page_views.time_on_page_second` | `NUMERIC` |
| `sessions.page_views.url` | `STRING` |
| `sessions.screen_recording_uuid` | `STRING` |
| `sessions.start_dts` | `DATETIME` |
| `sessions.utm_campaign` | `STRING` |
| `sessions.utm_content` | `STRING` |
| `sessions.utm_id` | `STRING` |
| `sessions.utm_medium` | `STRING` |
| `sessions.utm_source` | `STRING` |
| `sessions.utm_term` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_storefront_customer_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
