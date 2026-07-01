---
type: "UltraCart Table Definition"
title: "uc_affiliate_click_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_click_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_click_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_click_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_affiliate_click.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_affiliate_click_streaming](/tables/ultracart_dw_streaming/uc_affiliate_click_streaming.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
