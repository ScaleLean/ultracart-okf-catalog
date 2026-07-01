---
type: "UltraCart Table Definition"
title: "uc_affiliate_postback_logs"
description: "Affiliate postback event log."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_postback_logs"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_postback_logs"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_postback_logs

Affiliate postback event log.

## Grain

Affiliate postback log events.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_affiliate_postback_logs](/tables/ultracart_dw/uc_affiliate_postback_logs.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_affiliate_postback_logs](/tables/ultracart_dw_low/uc_affiliate_postback_logs.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_affiliate_postback_logs](/tables/ultracart_dw_medium/uc_affiliate_postback_logs.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_affiliate_postback_logs](/tables/ultracart_dw_high/uc_affiliate_postback_logs.md) |

## Field Paths

| Field path | Data type |
|---|---|
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
