---
type: "UltraCart Table Definition"
title: "uc_storefront_upsell_offer_events"
description: "Upsell event log."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_upsell_offer_events"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_upsell_offer_events"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_upsell_offer_events

Upsell event log.

## Grain

One upsell offer event row per storefront_upsell_offer_event_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_upsell_offer_events](/tables/ultracart_dw/uc_storefront_upsell_offer_events.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_upsell_offer_events](/tables/ultracart_dw_low/uc_storefront_upsell_offer_events.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_upsell_offer_events](/tables/ultracart_dw_medium/uc_storefront_upsell_offer_events.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_upsell_offer_events](/tables/ultracart_dw_high/uc_storefront_upsell_offer_events.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `currency_code` | `STRING` |
| `decline_count` | `INTEGER` |
| `event_dts` | `DATETIME` |
| `exchange_rate` | `NUMERIC` |
| `item_id` | `STRING` |
| `order_id` | `STRING` |
| `partition_date` | `DATE` |
| `profit` | `NUMERIC` |
| `profit_localized` | `NUMERIC` |
| `profit_localized_formatted` | `STRING` |
| `quantity` | `INTEGER` |
| `refund_quantity` | `INTEGER` |
| `refunded_profit` | `NUMERIC` |
| `refunded_profit_localized` | `NUMERIC` |
| `refunded_profit_localized_formatted` | `STRING` |
| `refunded_revenue` | `NUMERIC` |
| `refunded_revenue_localized` | `NUMERIC` |
| `refunded_revenue_localized_formatted` | `STRING` |
| `revenue` | `NUMERIC` |
| `revenue_localized` | `NUMERIC` |
| `revenue_localized_formatted` | `STRING` |
| `screen_size` | `STRING` |
| `session_id` | `STRING` |
| `storefront_upsell_offer_event_oid` | `INTEGER` |
| `storefront_upsell_offer_oid` | `INTEGER` |
| `successful_charge` | `INTEGER` |
| `utms` | `ARRAY<STRUCT>` |
| `utms.attribution_first_click_profit` | `NUMERIC` |
| `utms.attribution_first_click_refunded_profit` | `NUMERIC` |
| `utms.attribution_first_click_refunded_revenue` | `NUMERIC` |
| `utms.attribution_first_click_revenue` | `NUMERIC` |
| `utms.attribution_first_click_subtotal` | `NUMERIC` |
| `utms.attribution_first_click_total` | `NUMERIC` |
| `utms.attribution_last_click_profit` | `NUMERIC` |
| `utms.attribution_last_click_refunded_profit` | `NUMERIC` |
| `utms.attribution_last_click_refunded_revenue` | `NUMERIC` |
| `utms.attribution_last_click_revenue` | `NUMERIC` |
| `utms.attribution_last_click_subtotal` | `NUMERIC` |
| `utms.attribution_last_click_total` | `NUMERIC` |
| `utms.attribution_linear_profit` | `NUMERIC` |
| `utms.attribution_linear_refunded_profit` | `NUMERIC` |
| `utms.attribution_linear_refunded_revenue` | `NUMERIC` |
| `utms.attribution_linear_revenue` | `NUMERIC` |
| `utms.attribution_linear_subtotal` | `NUMERIC` |
| `utms.attribution_linear_total` | `NUMERIC` |
| `utms.attribution_position_based_profit` | `NUMERIC` |
| `utms.attribution_position_based_refunded_profit` | `NUMERIC` |
| `utms.attribution_position_based_refunded_revenue` | `NUMERIC` |
| `utms.attribution_position_based_revenue` | `NUMERIC` |
| `utms.attribution_position_based_subtotal` | `NUMERIC` |
| `utms.attribution_position_based_total` | `NUMERIC` |
| `utms.click_dts` | `DATETIME` |
| `utms.facebook_ad_id` | `STRING` |
| `utms.fbclid` | `STRING` |
| `utms.gbraid` | `STRING` |
| `utms.glcid` | `STRING` |
| `utms.itm_campaign` | `STRING` |
| `utms.itm_content` | `STRING` |
| `utms.itm_id` | `STRING` |
| `utms.itm_medium` | `STRING` |
| `utms.itm_source` | `STRING` |
| `utms.itm_term` | `STRING` |
| `utms.msclkid` | `STRING` |
| `utms.short_code` | `STRING` |
| `utms.short_code_backup` | `BOOLEAN` |
| `utms.ttclid` | `STRING` |
| `utms.uc_message_id` | `STRING` |
| `utms.utm_campaign` | `STRING` |
| `utms.utm_content` | `STRING` |
| `utms.utm_id` | `STRING` |
| `utms.utm_medium` | `STRING` |
| `utms.utm_source` | `STRING` |
| `utms.utm_term` | `STRING` |
| `utms.vmcid` | `STRING` |
| `utms.wbraid` | `STRING` |
| `view_count` | `INTEGER` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
