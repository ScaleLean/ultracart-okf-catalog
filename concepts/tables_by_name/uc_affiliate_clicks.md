---
type: "UltraCart Table Definition"
title: "uc_affiliate_clicks"
description: "Affiliate click and source data."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_clicks"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_clicks"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_clicks

Affiliate click and source data.

## Grain

One current affiliate click row per affiliate_click_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_affiliate_clicks](/tables/ultracart_dw/uc_affiliate_clicks.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_affiliate_clicks](/tables/ultracart_dw_low/uc_affiliate_clicks.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_affiliate_clicks](/tables/ultracart_dw_medium/uc_affiliate_clicks.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_affiliate_clicks](/tables/ultracart_dw_high/uc_affiliate_clicks.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
