---
type: "UltraCart Table Definition"
title: "uc_gift_certificates"
description: "Gift certificate records for operational reporting."
resource: "urn:ultracart:bigquery:table-definition:uc_gift_certificates"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_gift_certificates"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_gift_certificates

Gift certificate records for operational reporting.

## Grain

One gift certificate row per gift_certificate_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_gift_certificates](/tables/ultracart_dw/uc_gift_certificates.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_gift_certificates](/tables/ultracart_dw_low/uc_gift_certificates.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_gift_certificates](/tables/ultracart_dw_medium/uc_gift_certificates.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_gift_certificates](/tables/ultracart_dw_high/uc_gift_certificates.md) |

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
| `email` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
