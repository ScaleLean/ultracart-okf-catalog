---
type: "UltraCart Table Definition"
title: "uc_affiliate_payment_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_payment_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_payment_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_payment_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_affiliate_payment.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_affiliate_payment_streaming](/tables/ultracart_dw_streaming/uc_affiliate_payment_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `affiliate_oid` | `INTEGER` |
| `affiliate_payment_oid` | `INTEGER` |
| `check_number` | `STRING` |
| `comment` | `STRING` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `first_name` | `STRING` |
| `first_name_hash` | `STRING` |
| `last_name` | `STRING` |
| `last_name_hash` | `STRING` |
| `partition_date` | `DATE` |
| `payment_amount` | `NUMERIC` |
| `payment_dts` | `DATETIME` |
| `payment_ledgers` | `ARRAY<STRUCT>` |
| `payment_ledgers.amount` | `NUMERIC` |
| `payment_ledgers.ledger` | `STRUCT` |
| `payment_ledgers.ledger.affiliate_click_oid` | `INTEGER` |
| `payment_ledgers.ledger.affiliate_ledger_oid` | `INTEGER` |
| `payment_ledgers.ledger.affiliate_link_oid` | `INTEGER` |
| `payment_ledgers.ledger.affiliate_oid` | `INTEGER` |
| `payment_ledgers.ledger.assigned_by_user` | `STRING` |
| `payment_ledgers.ledger.item_id` | `STRING` |
| `payment_ledgers.ledger.order_id` | `STRING` |
| `payment_ledgers.ledger.original_transaction_dts` | `DATETIME` |
| `payment_ledgers.ledger.sub_id` | `STRING` |
| `payment_ledgers.ledger.tier_number` | `INTEGER` |
| `payment_ledgers.ledger.transaction_amount` | `NUMERIC` |
| `payment_ledgers.ledger.transaction_amount_paid` | `NUMERIC` |
| `payment_ledgers.ledger.transaction_dts` | `DATETIME` |
| `payment_ledgers.ledger.transaction_memo` | `STRING` |
| `payment_ledgers.ledger.transaction_percentage` | `NUMERIC` |
| `payment_ledgers.ledger.transaction_state` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
