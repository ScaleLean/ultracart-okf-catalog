---
type: "UltraCart Table Definition"
title: "uc_storefronts"
description: "Host and storefront dimension."
resource: "urn:ultracart:bigquery:table-definition:uc_storefronts"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefronts"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefronts

Host and storefront dimension.

## Grain

One storefront row per storefront_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefronts](/tables/ultracart_dw/uc_storefronts.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefronts](/tables/ultracart_dw_low/uc_storefronts.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefronts](/tables/ultracart_dw_medium/uc_storefronts.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefronts](/tables/ultracart_dw_high/uc_storefronts.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `host_alias1` | `STRING` |
| `host_alias2` | `STRING` |
| `host_alias3` | `STRING` |
| `host_alias4` | `STRING` |
| `host_alias5` | `STRING` |
| `host_name` | `STRING` |
| `locked` | `BOOLEAN` |
| `merchant_id` | `STRING` |
| `partition_oid` | `INTEGER` |
| `redirect_aliases` | `BOOLEAN` |
| `storefront_oid` | `INTEGER` |
| `unlock_password` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
