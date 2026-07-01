---
type: "UltraCart Table Definition"
title: "uc_affiliate_commission_groups"
description: "Affiliate commission group definitions."
resource: "urn:ultracart:bigquery:table-definition:uc_affiliate_commission_groups"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_affiliate_commission_groups"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_affiliate_commission_groups

Affiliate commission group definitions.

## Grain

Commission-group records.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_affiliate_commission_groups](/tables/ultracart_dw/uc_affiliate_commission_groups.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_affiliate_commission_groups](/tables/ultracart_dw_low/uc_affiliate_commission_groups.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_affiliate_commission_groups](/tables/ultracart_dw_medium/uc_affiliate_commission_groups.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_affiliate_commission_groups](/tables/ultracart_dw_high/uc_affiliate_commission_groups.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `affiliate_commission_group_oid` | `INTEGER` |
| `default_commission_group` | `BOOLEAN` |
| `exclude_items` | `ARRAY<STRUCT>` |
| `exclude_items.merchant_item_id` | `STRING` |
| `exclude_items.merchant_item_oid` | `INTEGER` |
| `global_commissions` | `ARRAY<STRUCT>` |
| `global_commissions.commission_percentage` | `NUMERIC` |
| `global_commissions.commission_percentage_repeat_customer` | `NUMERIC` |
| `global_commissions.description` | `STRING` |
| `global_commissions.fixed_commission` | `NUMERIC` |
| `global_commissions.fixed_commission_repeat_customer` | `NUMERIC` |
| `global_commissions.maximum_commission` | `NUMERIC` |
| `global_commissions.maximum_commission_repeat_customer` | `NUMERIC` |
| `global_commissions.minimum_commission` | `NUMERIC` |
| `global_commissions.minimum_commission_repeat_customer` | `NUMERIC` |
| `global_commissions.tier_number` | `INTEGER` |
| `hide_recruiting_link` | `BOOLEAN` |
| `items` | `ARRAY<STRUCT>` |
| `items.affiliate_commission_group_oid` | `INTEGER` |
| `items.affiliate_program_item_oid` | `INTEGER` |
| `items.alternate_description` | `STRING` |
| `items.hide_from_affiliate_console` | `BOOLEAN` |
| `items.merchant_item_id` | `STRING` |
| `items.merchant_item_oid` | `INTEGER` |
| `items.payment_schedule` | `ARRAY<STRUCT>` |
| `items.payment_schedule.days` | `INTEGER` |
| `items.payment_schedule.percentage` | `NUMERIC` |
| `items.status` | `STRING` |
| `items.tier_commissions` | `ARRAY<STRUCT>` |
| `items.tier_commissions.commission_amount` | `NUMERIC` |
| `items.tier_commissions.commission_amount_repeat_customer` | `NUMERIC` |
| `items.tier_commissions.commission_ranges` | `ARRAY<STRUCT>` |
| `items.tier_commissions.commission_ranges.commission_amount` | `NUMERIC` |
| `items.tier_commissions.commission_ranges.unit_cost` | `NUMERIC` |
| `items.tier_commissions.commission_ranges.unit_cost_high` | `NUMERIC` |
| `items.tier_commissions.commission_ranges.unit_cost_low` | `NUMERIC` |
| `items.tier_commissions.commission_ranges_repeat_customer` | `ARRAY<STRUCT>` |
| `items.tier_commissions.commission_ranges_repeat_customer.commission_amount` | `NUMERIC` |
| `items.tier_commissions.commission_ranges_repeat_customer.unit_cost` | `NUMERIC` |
| `items.tier_commissions.commission_ranges_repeat_customer.unit_cost_high` | `NUMERIC` |
| `items.tier_commissions.commission_ranges_repeat_customer.unit_cost_low` | `NUMERIC` |
| `items.tier_commissions.commission_type` | `STRING` |
| `items.tier_commissions.description` | `STRING` |
| `items.tier_commissions.tier_number` | `INTEGER` |
| `keep_commission_on_refunded_order` | `BOOLEAN` |
| `name` | `STRING` |
| `partition_oid` | `INTEGER` |
| `prevent_sending_all_emails` | `BOOLEAN` |
| `remove_cookie_after_purchase` | `BOOLEAN` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
