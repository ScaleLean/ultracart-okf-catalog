---
type: "BigQuery View"
title: "ultracart_dw_low.uc_affiliate_payments"
description: "Affiliate payment records for aggregate payment reporting."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_affiliate_payments"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_affiliate_payments"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_affiliate_payments

Affiliate payment records for aggregate payment reporting.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_affiliate_payments`
- Object type: `VIEW`
- Table family: [affiliate_commissions](/references/table_families.md#affiliate-commissions)
- Grain: One affiliate payment row per affiliate_payment_oid.
- Canonical definition: [uc_affiliate_payments](/concepts/tables_by_name/uc_affiliate_payments.md)

## Schema Coverage

- Field paths: 29
- Array fields: 1
- Struct fields: 2

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_low.uc_affiliate_payments`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
