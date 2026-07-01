---
type: "UltraCart Table Definition"
title: "uc_storefront_customer_session_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_customer_session_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_customer_session_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_customer_session_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_storefront_customer_session.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_storefront_customer_session_streaming](/tables/ultracart_dw_streaming/uc_storefront_customer_session_streaming.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
