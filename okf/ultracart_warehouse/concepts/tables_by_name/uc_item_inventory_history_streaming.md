---
type: "UltraCart Table Definition"
title: "uc_item_inventory_history_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_item_inventory_history_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_item_inventory_history_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_item_inventory_history_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_item_inventory_history.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_item_inventory_history_streaming](/tables/ultracart_dw_streaming/uc_item_inventory_history_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
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
