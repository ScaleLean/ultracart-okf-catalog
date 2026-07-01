---
type: "BigQuery View"
title: "ultracart_dw.uc_affiliate_postback_logs"
description: "Affiliate postback event log."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_affiliate_postback_logs"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_affiliate_postback_logs"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_affiliate_postback_logs

Affiliate postback event log.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_affiliate_postback_logs`
- Object type: `VIEW`
- Table family: [affiliate_commissions](/references/table_families.md#affiliate-commissions)
- Grain: Affiliate postback log events.
- Canonical definition: [uc_affiliate_postback_logs](/concepts/tables_by_name/uc_affiliate_postback_logs.md)

## Schema Coverage

- Field paths: 15
- Array fields: 1
- Struct fields: 1

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw.uc_affiliate_postback_logs`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
