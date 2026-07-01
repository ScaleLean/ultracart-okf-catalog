---
type: "BigQuery View"
title: "ultracart_dw.uc_affiliate_clicks"
description: "Affiliate click and source data."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_affiliate_clicks"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_affiliate_clicks"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_affiliate_clicks

Affiliate click and source data.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_affiliate_clicks`
- Object type: `VIEW`
- Table family: [affiliate_commissions](/references/table_families.md#affiliate-commissions)
- Grain: One current affiliate click row per affiliate_click_oid.
- Canonical definition: [uc_affiliate_clicks](/concepts/tables_by_name/uc_affiliate_clicks.md)

## Schema Coverage

- Field paths: 28
- Array fields: 0
- Struct fields: 1

## Field Paths

| Field path | Data type |
|---|---|
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
FROM `{{ source_project }}.ultracart_dw.uc_affiliate_clicks`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
