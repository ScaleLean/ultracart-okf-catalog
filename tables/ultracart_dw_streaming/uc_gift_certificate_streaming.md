---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_gift_certificate_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_gift_certificate_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_gift_certificate_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_gift_certificate_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_gift_certificate_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_gift_certificate.
- Canonical definition: [uc_gift_certificate_streaming](/concepts/tables_by_name/uc_gift_certificate_streaming.md)

## Schema Coverage

- Field paths: 24
- Array fields: 1
- Struct fields: 1

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `activated` | `BOOLEAN` |
| `code` | `STRING` |
| `customer_profile_oid` | `INTEGER` |
| `deleted` | `BOOLEAN` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `expiration_dts` | `DATETIME` |
| `gift_certificate_oid` | `INTEGER` |
| `internal` | `BOOLEAN` |
| `ledger_entries` | `ARRAY<STRUCT>` |
| `ledger_entries.amount` | `NUMERIC` |
| `ledger_entries.description` | `STRING` |
| `ledger_entries.entry_dts` | `DATETIME` |
| `ledger_entries.gift_certificate_ledger_oid` | `INTEGER` |
| `ledger_entries.gift_certificate_oid` | `INTEGER` |
| `ledger_entries.reference_order_id` | `STRING` |
| `merchant_id` | `STRING` |
| `merchant_note` | `STRING` |
| `original_balance` | `NUMERIC` |
| `partition_oid` | `INTEGER` |
| `reference_order_id` | `STRING` |
| `remaining_balance` | `NUMERIC` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_gift_certificate_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
