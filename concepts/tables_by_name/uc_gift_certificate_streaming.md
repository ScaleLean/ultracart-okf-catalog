---
type: "UltraCart Table Definition"
title: "uc_gift_certificate_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_gift_certificate_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_gift_certificate_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_gift_certificate_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_gift_certificate.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_gift_certificate_streaming](/tables/ultracart_dw_streaming/uc_gift_certificate_streaming.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
