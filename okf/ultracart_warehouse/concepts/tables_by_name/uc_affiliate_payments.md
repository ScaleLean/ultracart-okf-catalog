---
type: "UltraCart Table Definition"
title: "uc_affiliate_payments"
description: "Affiliate payment records for aggregate payment reporting."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_payments"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_payments"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_payments

Affiliate payment records for aggregate payment reporting.

## Grain

One affiliate payment row per affiliate_payment_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_affiliate_payments](/tables/ultracart_dw/uc_affiliate_payments.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_affiliate_payments](/tables/ultracart_dw_low/uc_affiliate_payments.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_affiliate_payments](/tables/ultracart_dw_medium/uc_affiliate_payments.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_affiliate_payments](/tables/ultracart_dw_high/uc_affiliate_payments.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `affiliate_oid` | `INTEGER` |
| `affiliate_payment_oid` | `INTEGER` |
| `check_number` | `STRING` |
| `comment` | `STRING` |
| `email_hash` | `STRING` |
| `first_name_hash` | `STRING` |
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
| `email` | `STRING` |
| `first_name` | `STRING` |
| `last_name` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
