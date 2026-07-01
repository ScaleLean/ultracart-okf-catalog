---
type: "UltraCart Table Definition"
title: "uc_affiliate_ledgers"
description: "Affiliate commission and transaction ledger with order linkage."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_ledgers"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_ledgers"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_ledgers

Affiliate commission and transaction ledger with order linkage.

## Grain

One affiliate ledger row per affiliate_ledger_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_affiliate_ledgers](/tables/ultracart_dw/uc_affiliate_ledgers.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_affiliate_ledgers](/tables/ultracart_dw_low/uc_affiliate_ledgers.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_affiliate_ledgers](/tables/ultracart_dw_medium/uc_affiliate_ledgers.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_affiliate_ledgers](/tables/ultracart_dw_high/uc_affiliate_ledgers.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
