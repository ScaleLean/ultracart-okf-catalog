---
type: "UltraCart Table Definition"
title: "uc_storefront_customer_segments"
description: "Storefront customer segment membership data."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_customer_segments"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_customer_segments"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_customer_segments

Storefront customer segment membership data.

## Grain

One storefront segment membership row.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_customer_segments](/tables/ultracart_dw/uc_storefront_customer_segments.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_customer_segments](/tables/ultracart_dw_low/uc_storefront_customer_segments.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_customer_segments](/tables/ultracart_dw_medium/uc_storefront_customer_segments.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_customer_segments](/tables/ultracart_dw_high/uc_storefront_customer_segments.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `add_dts` | `DATETIME` |
| `email_hash` | `STRING` |
| `esp_customer_uuid` | `STRING` |
| `merchant_id` | `STRING` |
| `partition_oid` | `INTEGER` |
| `segment_name` | `STRING` |
| `segment_uuid` | `STRING` |
| `email` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
