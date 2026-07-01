---
type: "UltraCart Table Definition"
title: "segment_customers_autoOrders"
description: "Imported or legacy segmentation helper object."
resource: "urn:ultracart:bigquery:table-definition:segment_customers_autoOrders"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "segment_customers_autoOrders"
  - "import"
timestamp: "2026-07-01T00:00:00Z"
---

# segment_customers_autoOrders

Imported or legacy segmentation helper object.

## Grain

Imported helper grain defined by the source import or segmentation view.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_import` | `VIEW` | [ultracart_dw_import.segment_customers_autoOrders](/tables/ultracart_dw_import/segment_customers_autoOrders.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `completed_orders_count` | `INTEGER` |
| `creation_dts` | `DATETIME` |
| `email` | `STRING` |
| `enabled` | `BOOLEAN` |
| `last_canceled_dts` | `DATETIME` |
| `product_category` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
