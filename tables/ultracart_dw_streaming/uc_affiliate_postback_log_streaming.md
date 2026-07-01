---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_affiliate_postback_log_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_affiliate_postback_log_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_affiliate_postback_log_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_affiliate_postback_log_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_affiliate_postback_log_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_affiliate_postback_log.
- Canonical definition: [uc_affiliate_postback_log_streaming](/concepts/tables_by_name/uc_affiliate_postback_log_streaming.md)

## Schema Coverage

- Field paths: 17
- Array fields: 1
- Struct fields: 1

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_affiliate_postback_log_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
