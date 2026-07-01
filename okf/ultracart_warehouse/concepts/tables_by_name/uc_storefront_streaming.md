---
type: "UltraCart Table Definition"
title: "uc_storefront_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_storefront.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_storefront_streaming](/tables/ultracart_dw_streaming/uc_storefront_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
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
