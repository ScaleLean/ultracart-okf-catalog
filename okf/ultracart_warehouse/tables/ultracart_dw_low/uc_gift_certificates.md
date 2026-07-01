---
type: "BigQuery View"
title: "ultracart_dw_low.uc_gift_certificates"
description: "Gift certificate records for operational reporting."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_gift_certificates"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_gift_certificates"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_gift_certificates

Gift certificate records for operational reporting.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_gift_certificates`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One gift certificate row per gift_certificate_oid.
- Canonical definition: [uc_gift_certificates](/concepts/tables_by_name/uc_gift_certificates.md)

## Schema Coverage

- Field paths: 21
- Array fields: 1
- Struct fields: 1

## Field Paths

| Field path | Data type |
|---|---|
| `activated` | `BOOLEAN` |
| `code` | `STRING` |
| `customer_profile_oid` | `INTEGER` |
| `deleted` | `BOOLEAN` |
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
FROM `{{ source_project }}.ultracart_dw_low.uc_gift_certificates`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
