---
type: "UltraCart Table Definition"
title: "uc_affiliate_network_pixels"
description: "Affiliate and network pixel configuration."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_network_pixels"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_network_pixels"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_network_pixels

Affiliate and network pixel configuration.

## Grain

Affiliate network pixel definition records.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_affiliate_network_pixels](/tables/ultracart_dw/uc_affiliate_network_pixels.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_affiliate_network_pixels](/tables/ultracart_dw_low/uc_affiliate_network_pixels.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_affiliate_network_pixels](/tables/ultracart_dw_medium/uc_affiliate_network_pixels.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_affiliate_network_pixels](/tables/ultracart_dw_high/uc_affiliate_network_pixels.md) |

## Field Paths

| Field path | Data type |
|---|---|
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
