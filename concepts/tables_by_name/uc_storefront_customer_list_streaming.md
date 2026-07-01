---
type: "UltraCart Table Definition"
title: "uc_storefront_customer_list_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_customer_list_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_customer_list_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_customer_list_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_storefront_customer_list.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_storefront_customer_list_streaming](/tables/ultracart_dw_streaming/uc_storefront_customer_list_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `add_dts` | `DATETIME` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `esp_customer_uuid` | `STRING` |
| `list_name` | `STRING` |
| `list_uuid` | `STRING` |
| `merchant_id` | `STRING` |
| `partition_oid` | `INTEGER` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
