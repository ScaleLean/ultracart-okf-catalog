---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_affiliate_click_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_affiliate_click_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_affiliate_click_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_affiliate_click_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_affiliate_click_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_affiliate_click.
- Canonical definition: [uc_affiliate_click_streaming](/concepts/tables_by_name/uc_affiliate_click_streaming.md)

## Schema Coverage

- Field paths: 30
- Array fields: 0
- Struct fields: 1

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `affiliate_click_oid` | `INTEGER` |
| `affiliate_link_oid` | `INTEGER` |
| `affiliate_oid` | `INTEGER` |
| `click_dts` | `DATETIME` |
| `ip_address` | `STRING` |
| `landing_page` | `STRING` |
| `landing_page_query_string` | `STRING` |
| `link` | `STRUCT` |
| `link.affiliate_link_oid` | `INTEGER` |
| `link.affiliate_managed_link_oid` | `INTEGER` |
| `link.affiliate_oid` | `INTEGER` |
| `link.affiliate_program_item_oid` | `INTEGER` |
| `link.code` | `STRING` |
| `link.creative_oid` | `INTEGER` |
| `link.custom_html` | `STRING` |
| `link.custom_html_approval_status` | `STRING` |
| `link.custom_landing_url` | `STRING` |
| `link.deleted` | `BOOLEAN` |
| `link.invisible_link_approval_status` | `STRING` |
| `link.invisible_link_url_prefix` | `STRING` |
| `link.name` | `STRING` |
| `link.type` | `STRING` |
| `partition_date` | `DATE` |
| `referrer` | `STRING` |
| `referrer_query_string` | `STRING` |
| `screen_recording_uuid` | `STRING` |
| `sub_id` | `STRING` |
| `ucacid` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_affiliate_click_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
