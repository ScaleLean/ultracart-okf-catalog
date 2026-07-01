---
type: "UltraCart Table Definition"
title: "uc_affiliate_postback_log_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_postback_log_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_postback_log_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_postback_log_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_affiliate_postback_log.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_affiliate_postback_log_streaming](/tables/ultracart_dw_streaming/uc_affiliate_postback_log_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `affiliate_oid` | `INTEGER` |
| `affiliate_postback_log_uuid` | `STRING` |
| `commission` | `NUMERIC` |
| `config_url` | `STRING` |
| `landing_page_query_string` | `STRING` |
| `ledger_oids` | `ARRAY<STRUCT>` |
| `ledger_oids.value` | `INTEGER` |
| `merchant_id` | `STRING` |
| `order_id` | `STRING` |
| `partition_date` | `DATE` |
| `postback_dts` | `DATETIME` |
| `response` | `STRING` |
| `status_code` | `INTEGER` |
| `sub_id` | `STRING` |
| `url` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
