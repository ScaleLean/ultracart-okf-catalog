---
type: "UltraCart Table Definition"
title: "uc_storefront_customer_email_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_customer_email_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_customer_email_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_customer_email_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_storefront_customer_email.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_storefront_customer_email_streaming](/tables/ultracart_dw_streaming/uc_storefront_customer_email_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `campaign_name` | `STRING` |
| `clicked` | `BOOLEAN` |
| `clicked_dts` | `DATETIME` |
| `commseq_uuid` | `STRING` |
| `converted` | `BOOLEAN` |
| `email` | `STRING` |
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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
