---
type: "UltraCart Table Definition"
title: "uc_storefront_customer_sessions"
description: "Storefront customer session membership data."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_customer_sessions"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_customer_sessions"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_customer_sessions

Storefront customer session membership data.

## Grain

One storefront customer-session row.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_customer_sessions](/tables/ultracart_dw/uc_storefront_customer_sessions.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_customer_sessions](/tables/ultracart_dw_low/uc_storefront_customer_sessions.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_customer_sessions](/tables/ultracart_dw_medium/uc_storefront_customer_sessions.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_customer_sessions](/tables/ultracart_dw_high/uc_storefront_customer_sessions.md) |

## Field Paths

| Field path | Data type |
|---|---|
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
| `email` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
