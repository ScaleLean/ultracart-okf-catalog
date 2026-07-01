---
type: "UltraCart Table Definition"
title: "uc_storefront_customers"
description: "Storefront customer profile and listing surface."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_customers"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_customers"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_customers

Storefront customer profile and listing surface.

## Grain

One storefront customer profile row.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_customers](/tables/ultracart_dw/uc_storefront_customers.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_customers](/tables/ultracart_dw_low/uc_storefront_customers.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_customers](/tables/ultracart_dw_medium/uc_storefront_customers.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_customers](/tables/ultracart_dw_high/uc_storefront_customers.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `consecutive_emails_unclicked` | `INTEGER` |
| `consecutive_emails_unopened` | `INTEGER` |
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
| `email` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
