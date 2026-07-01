---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_affiliate_payment_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_affiliate_payment_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_affiliate_payment_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_affiliate_payment_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_affiliate_payment_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_affiliate_payment.
- Canonical definition: [uc_affiliate_payment_streaming](/concepts/tables_by_name/uc_affiliate_payment_streaming.md)

## Schema Coverage

- Field paths: 34
- Array fields: 1
- Struct fields: 2

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_affiliate_payment_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
