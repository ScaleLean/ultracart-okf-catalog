---
type: "UltraCart Table Definition"
title: "uc_affiliate_network_pixel_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_network_pixel_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_network_pixel_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_network_pixel_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_affiliate_network_pixel.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_affiliate_network_pixel_streaming](/tables/ultracart_dw_streaming/uc_affiliate_network_pixel_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `affiliate_network_pixel_oid` | `INTEGER` |
| `assign_to_internal_affiliate_oid` | `INTEGER` |
| `commission_fixed` | `NUMERIC` |
| `conversion_pixel` | `STRING` |
| `conversion_type` | `STRING` |
| `cookie_lifetime_days` | `INTEGER` |
| `fire_percentage` | `NUMERIC` |
| `merchant_id` | `STRING` |
| `network_name` | `STRING` |
| `no_fire_assign_to_internal_affiliate_oid` | `INTEGER` |
| `no_fire_skip_internal_affiliate_system` | `BOOLEAN` |
| `parameter_name` | `STRING` |
| `parameter_value` | `STRING` |
| `partition_oid` | `INTEGER` |
| `record_fire_in_custom_field` | `INTEGER` |
| `record_name_in_custom_field` | `INTEGER` |
| `remove_empty_pixel_parameters` | `BOOLEAN` |
| `stomp_other_cookies` | `BOOLEAN` |
| `storefront_oid` | `INTEGER` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
