---
type: "UltraCart Table Definition"
title: "uc_item_inventory_history"
description: "Inventory ledger and history for audit and operational review."
resource: "urn:ultracart:bigquery:table-definition:uc_item_inventory_history"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_item_inventory_history"
  - "commerce_core"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_item_inventory_history

Inventory ledger and history for audit and operational review.

## Grain

One inventory event row per item_inventory_history_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_item_inventory_history](/tables/ultracart_dw/uc_item_inventory_history.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_item_inventory_history](/tables/ultracart_dw_low/uc_item_inventory_history.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_item_inventory_history](/tables/ultracart_dw_medium/uc_item_inventory_history.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_item_inventory_history](/tables/ultracart_dw_high/uc_item_inventory_history.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `adjustment` | `NUMERIC` |
| `after_inventory_level` | `NUMERIC` |
| `before_inventory_level` | `NUMERIC` |
| `distribution_center_code` | `STRING` |
| `distribution_center_oid` | `INTEGER` |
| `history_dts` | `DATETIME` |
| `item_inventory_history_oid` | `INTEGER` |
| `merchant_id` | `STRING` |
| `merchant_item_id` | `STRING` |
| `merchant_item_oid` | `INTEGER` |
| `order_id` | `STRING` |
| `partition_oid` | `INTEGER` |
| `reason` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
