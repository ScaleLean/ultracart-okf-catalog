---
type: "BigQuery View"
title: "ultracart_dw_high.uc_affiliate_ledgers"
description: "Affiliate commission and transaction ledger with order linkage."
resource: "urn:ultracart:bigquery:object:ultracart_dw_high.uc_affiliate_ledgers"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_high"
  - "uc_affiliate_ledgers"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_high.uc_affiliate_ledgers

Affiliate commission and transaction ledger with order linkage.

## Definition

- Dataset: [ultracart_dw_high](/datasets/ultracart_dw_high.md)
- Object name: `uc_affiliate_ledgers`
- Object type: `VIEW`
- Table family: [affiliate_commissions](/references/table_families.md#affiliate-commissions)
- Grain: One affiliate ledger row per affiliate_ledger_oid.
- Canonical definition: [uc_affiliate_ledgers](/concepts/tables_by_name/uc_affiliate_ledgers.md)

## Schema Coverage

- Field paths: 60
- Array fields: 0
- Struct fields: 3

## Field Paths

| Field path | Data type |
|---|---|
| `affiliate_click_oid` | `INTEGER` |
| `affiliate_ledger_oid` | `INTEGER` |
| `affiliate_link_oid` | `INTEGER` |
| `affiliate_oid` | `INTEGER` |
| `assigned_by_user` | `STRING` |
| `click` | `STRUCT` |
| `click.affiliate_click_oid` | `INTEGER` |
| `click.affiliate_link_oid` | `INTEGER` |
| `click.affiliate_oid` | `INTEGER` |
| `click.click_dts` | `DATETIME` |
| `click.ip_address` | `STRING` |
| `click.landing_page` | `STRING` |
| `click.landing_page_query_string` | `STRING` |
| `click.link` | `STRUCT` |
| `click.link.affiliate_link_oid` | `INTEGER` |
| `click.link.affiliate_managed_link_oid` | `INTEGER` |
| `click.link.affiliate_oid` | `INTEGER` |
| `click.link.affiliate_program_item_oid` | `INTEGER` |
| `click.link.code` | `STRING` |
| `click.link.creative_oid` | `INTEGER` |
| `click.link.custom_html` | `STRING` |
| `click.link.custom_html_approval_status` | `STRING` |
| `click.link.custom_landing_url` | `STRING` |
| `click.link.deleted` | `BOOLEAN` |
| `click.link.invisible_link_approval_status` | `STRING` |
| `click.link.invisible_link_url_prefix` | `STRING` |
| `click.link.name` | `STRING` |
| `click.link.type` | `STRING` |
| `click.referrer` | `STRING` |
| `click.referrer_query_string` | `STRING` |
| `click.screen_recording_uuid` | `STRING` |
| `click.sub_id` | `STRING` |
| `click.ucacid` | `STRING` |
| `item_id` | `STRING` |
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
| `order_id` | `STRING` |
| `original_transaction_dts` | `DATETIME` |
| `partition_date` | `DATE` |
| `sub_id` | `STRING` |
| `tier_number` | `INTEGER` |
| `transaction_amount` | `NUMERIC` |
| `transaction_amount_paid` | `NUMERIC` |
| `transaction_dts` | `DATETIME` |
| `transaction_memo` | `STRING` |
| `transaction_percentage` | `NUMERIC` |
| `transaction_state` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_high.uc_affiliate_ledgers`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
