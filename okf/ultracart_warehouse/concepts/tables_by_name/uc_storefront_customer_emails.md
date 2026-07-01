---
type: "UltraCart Table Definition"
title: "uc_storefront_customer_emails"
description: "Storefront email membership and status data."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_customer_emails"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_customer_emails"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_customer_emails

Storefront email membership and status data.

## Grain

One storefront email membership row.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_customer_emails](/tables/ultracart_dw/uc_storefront_customer_emails.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_customer_emails](/tables/ultracart_dw_low/uc_storefront_customer_emails.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_customer_emails](/tables/ultracart_dw_medium/uc_storefront_customer_emails.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_customer_emails](/tables/ultracart_dw_high/uc_storefront_customer_emails.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `campaign_name` | `STRING` |
| `clicked` | `BOOLEAN` |
| `clicked_dts` | `DATETIME` |
| `commseq_uuid` | `STRING` |
| `converted` | `BOOLEAN` |
| `email_hash` | `STRING` |
| `email_uuid` | `STRING` |
| `esp_customer_uuid` | `STRING` |
| `flow_name` | `STRING` |
| `merchant_id` | `STRING` |
| `opened` | `BOOLEAN` |
| `opened_dts` | `DATETIME` |
| `order_id` | `STRING` |
| `partition_date` | `DATE` |
| `sent_dts` | `DATETIME` |
| `spam_complaint` | `BOOLEAN` |
| `spam_complaint_dts` | `DATETIME` |
| `subject` | `STRING` |
| `transport` | `STRING` |
| `email` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
