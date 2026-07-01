---
type: "UltraCart Table Definition"
title: "uc_order_summary_mv"
description: "Dashboard rollup or materialized reporting object."
resource: "urn:ultracart:bigquery:table-definition:uc_order_summary_mv"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_order_summary_mv"
  - "dashboard"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_order_summary_mv

Dashboard rollup or materialized reporting object.

## Grain

Dashboard-oriented aggregate or summary grain.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_dashboard` | `MATERIALIZED VIEW` | [ultracart_dw_dashboard.uc_order_summary_mv](/tables/ultracart_dw_dashboard/uc_order_summary_mv.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `channel` | `STRING` |
| `partition_date` | `DATE` |
| `period` | `DATETIME` |
| `total` | `NUMERIC` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
