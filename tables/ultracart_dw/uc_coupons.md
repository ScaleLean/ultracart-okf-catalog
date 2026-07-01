---
type: "BigQuery View"
title: "ultracart_dw.uc_coupons"
description: "Coupon configuration and discount rules."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_coupons"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_coupons"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_coupons

Coupon configuration and discount rules.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_coupons`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One coupon row per coupon_oid.
- Canonical definition: [uc_coupons](/concepts/tables_by_name/uc_coupons.md)

## Schema Coverage

- Field paths: 341
- Array fields: 79
- Struct fields: 129

## Field Paths

| Field path | Data type |
|---|---|
| `affiliate_oid` | `INTEGER` |
| `allow_multiple_one_time_codes` | `BOOLEAN` |
| `amount_off_items` | `STRUCT` |
| `amount_off_items.currency_code` | `STRING` |
| `amount_off_items.discount_amount` | `NUMERIC` |
| `amount_off_items.item_tags` | `ARRAY<STRUCT>` |
| `amount_off_items.item_tags.value` | `STRING` |
| `amount_off_items.items` | `ARRAY<STRUCT>` |
| `amount_off_items.items.value` | `STRING` |
| `amount_off_items.limit` | `INTEGER` |
| `amount_off_items_and_free_shipping` | `STRUCT` |
| `amount_off_items_and_free_shipping.currency_code` | `STRING` |
| `amount_off_items_and_free_shipping.discount_amount` | `NUMERIC` |
| `amount_off_items_and_free_shipping.item_tags` | `ARRAY<STRUCT>` |
| `amount_off_items_and_free_shipping.item_tags.value` | `STRING` |
| `amount_off_items_and_free_shipping.items` | `ARRAY<STRUCT>` |
| `amount_off_items_and_free_shipping.items.value` | `STRING` |
| `amount_off_items_and_free_shipping.limit` | `INTEGER` |
| `amount_off_items_and_free_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `amount_off_items_and_free_shipping.shipping_methods.value` | `STRING` |
| `amount_off_shipping` | `STRUCT` |
| `amount_off_shipping.currency_code` | `STRING` |
| `amount_off_shipping.discount_amount` | `NUMERIC` |
| `amount_off_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `amount_off_shipping.shipping_methods.value` | `STRING` |
| `amount_off_shipping_with_items_purchase` | `STRUCT` |
| `amount_off_shipping_with_items_purchase.currency_code` | `STRING` |
| `amount_off_shipping_with_items_purchase.discount_amount` | `NUMERIC` |
| `amount_off_shipping_with_items_purchase.items` | `ARRAY<STRUCT>` |
| `amount_off_shipping_with_items_purchase.items.value` | `STRING` |
| `amount_off_shipping_with_items_purchase.shipping_methods` | `ARRAY<STRUCT>` |
| `amount_off_shipping_with_items_purchase.shipping_methods.value` | `STRING` |
| `amount_off_subtotal` | `STRUCT` |
| `amount_off_subtotal.currency_code` | `STRING` |
| `amount_off_subtotal.discount_amount` | `NUMERIC` |
| `amount_off_subtotal_and_free_shipping` | `STRUCT` |
| `amount_off_subtotal_and_free_shipping.currency_code` | `STRING` |
| `amount_off_subtotal_and_free_shipping.discount_amount` | `NUMERIC` |
| `amount_off_subtotal_and_free_shipping.purchase_amount` | `NUMERIC` |
| `amount_off_subtotal_and_free_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `amount_off_subtotal_and_free_shipping.shipping_methods.value` | `STRING` |
| `amount_off_subtotal_and_shipping` | `STRUCT` |
| `amount_off_subtotal_and_shipping.currency_code` | `STRING` |
| `amount_off_subtotal_and_shipping.discount_amount` | `NUMERIC` |
| `amount_off_subtotal_with_block_purchase` | `STRUCT` |
| `amount_off_subtotal_with_block_purchase.currency_code` | `STRING` |
| `amount_off_subtotal_with_block_purchase.discount_amount` | `NUMERIC` |
| `amount_off_subtotal_with_block_purchase.required_purchase_item` | `STRING` |
| `amount_off_subtotal_with_block_purchase.required_purchase_quantity` | `INTEGER` |
| `amount_off_subtotal_with_items_purchase` | `STRUCT` |
| `amount_off_subtotal_with_items_purchase.currency_code` | `STRING` |
| `amount_off_subtotal_with_items_purchase.discount_amount` | `NUMERIC` |
| `amount_off_subtotal_with_items_purchase.items` | `ARRAY<STRUCT>` |
| `amount_off_subtotal_with_items_purchase.items.value` | `STRING` |
| `amount_off_subtotal_with_items_purchase.required_purchase_quantity` | `INTEGER` |
| `amount_off_subtotal_with_purchase` | `STRUCT` |
| `amount_off_subtotal_with_purchase.currency_code` | `STRING` |
| `amount_off_subtotal_with_purchase.discount_amount` | `NUMERIC` |
| `amount_off_subtotal_with_purchase.purchase_amount` | `NUMERIC` |
| `amount_shipping_with_subtotal` | `STRUCT` |
| `amount_shipping_with_subtotal.currency_code` | `STRING` |
| `amount_shipping_with_subtotal.purchase_amount` | `NUMERIC` |
| `amount_shipping_with_subtotal.shipping_amount` | `NUMERIC` |
| `amount_shipping_with_subtotal.shipping_methods` | `ARRAY<STRUCT>` |
| `amount_shipping_with_subtotal.shipping_methods.value` | `STRING` |
| `automatically_apply_coupon_codes` | `STRUCT` |
| `automatically_apply_coupon_codes.coupon_codes` | `ARRAY<STRUCT>` |
| `automatically_apply_coupon_codes.coupon_codes.value` | `STRING` |
| `buy_one_get_one` | `STRUCT` |
| `buy_one_get_one.item_tags` | `ARRAY<STRUCT>` |
| `buy_one_get_one.item_tags.value` | `STRING` |
| `buy_one_get_one.items` | `ARRAY<STRUCT>` |
| `buy_one_get_one.items.value` | `STRING` |
| `buy_one_get_one.limit` | `INTEGER` |
| `calculated_description` | `STRING` |
| `can_be_used_with_other_coupons` | `BOOLEAN` |
| `coupon_oid` | `INTEGER` |
| `coupon_type` | `STRING` |
| `description` | `STRING` |
| `discount_item_with_item_purchase` | `STRUCT` |
| `discount_item_with_item_purchase.currency_code` | `STRING` |
| `discount_item_with_item_purchase.discount_item` | `STRING` |
| `discount_item_with_item_purchase.discount_item_tags` | `ARRAY<STRUCT>` |
| `discount_item_with_item_purchase.discount_item_tags.value` | `STRING` |
| `discount_item_with_item_purchase.discount_price` | `NUMERIC` |
| `discount_item_with_item_purchase.limit` | `INTEGER` |
| `discount_item_with_item_purchase.required_purchase_item` | `STRING` |
| `discount_item_with_item_purchase.required_purchase_items_tags` | `ARRAY<STRUCT>` |
| `discount_item_with_item_purchase.required_purchase_items_tags.value` | `STRING` |
| `discount_items` | `STRUCT` |
| `discount_items.currency_code` | `STRING` |
| `discount_items.discount_price` | `NUMERIC` |
| `discount_items.items` | `ARRAY<STRUCT>` |
| `discount_items.items.value` | `STRING` |
| `discount_items.limit` | `INTEGER` |
| `expiration_dts` | `DATETIME` |
| `free_item_and_shipping_with_subtotal` | `STRUCT` |
| `free_item_and_shipping_with_subtotal.currency_code` | `STRING` |
| `free_item_and_shipping_with_subtotal.items` | `ARRAY<STRUCT>` |
| `free_item_and_shipping_with_subtotal.items.value` | `STRING` |
| `free_item_and_shipping_with_subtotal.limit` | `INTEGER` |
| `free_item_and_shipping_with_subtotal.shipping_methods` | `ARRAY<STRUCT>` |
| `free_item_and_shipping_with_subtotal.shipping_methods.value` | `STRING` |
| `free_item_and_shipping_with_subtotal.subtotal_amount` | `NUMERIC` |
| `free_item_with_item_purchase` | `STRUCT` |
| `free_item_with_item_purchase.item_tags` | `ARRAY<STRUCT>` |
| `free_item_with_item_purchase.item_tags.value` | `STRING` |
| `free_item_with_item_purchase.items` | `ARRAY<STRUCT>` |
| `free_item_with_item_purchase.items.value` | `STRING` |
| `free_item_with_item_purchase.limit` | `INTEGER` |
| `free_item_with_item_purchase.match_required_purchase_item_to_free_item` | `BOOLEAN` |
| `free_item_with_item_purchase.required_purchase_items` | `ARRAY<STRUCT>` |
| `free_item_with_item_purchase.required_purchase_items.value` | `STRING` |
| `free_item_with_item_purchase.required_purchase_items_tags` | `ARRAY<STRUCT>` |
| `free_item_with_item_purchase.required_purchase_items_tags.value` | `STRING` |
| `free_item_with_item_purchase_and_free_shipping` | `STRUCT` |
| `free_item_with_item_purchase_and_free_shipping.items` | `ARRAY<STRUCT>` |
| `free_item_with_item_purchase_and_free_shipping.items.value` | `STRING` |
| `free_item_with_item_purchase_and_free_shipping.limit` | `INTEGER` |
| `free_item_with_item_purchase_and_free_shipping.match_required_purchase_item_to_free_item` | `BOOLEAN` |
| `free_item_with_item_purchase_and_free_shipping.required_purchase_items` | `ARRAY<STRUCT>` |
| `free_item_with_item_purchase_and_free_shipping.required_purchase_items.value` | `STRING` |
| `free_item_with_item_purchase_and_free_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `free_item_with_item_purchase_and_free_shipping.shipping_methods.value` | `STRING` |
| `free_item_with_subtotal` | `STRUCT` |
| `free_item_with_subtotal.currency_code` | `STRING` |
| `free_item_with_subtotal.items` | `ARRAY<STRUCT>` |
| `free_item_with_subtotal.items.value` | `STRING` |
| `free_item_with_subtotal.limit` | `INTEGER` |
| `free_item_with_subtotal.subtotal_amount` | `NUMERIC` |
| `free_items_with_item_purchase` | `STRUCT` |
| `free_items_with_item_purchase.free_item` | `STRING` |
| `free_items_with_item_purchase.free_quantity` | `INTEGER` |
| `free_items_with_item_purchase.limit` | `INTEGER` |
| `free_items_with_item_purchase.required_purchase_item` | `STRING` |
| `free_items_with_item_purchase.required_purchase_quantity` | `INTEGER` |
| `free_items_with_mixmatch_purchase` | `STRUCT` |
| `free_items_with_mixmatch_purchase.free_item` | `STRING` |
| `free_items_with_mixmatch_purchase.free_quantity` | `INTEGER` |
| `free_items_with_mixmatch_purchase.limit` | `INTEGER` |
| `free_items_with_mixmatch_purchase.required_purchase_mix_and_match_group` | `STRING` |
| `free_items_with_mixmatch_purchase.required_purchase_quantity` | `INTEGER` |
| `free_shipping` | `STRUCT` |
| `free_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `free_shipping.shipping_methods.value` | `STRING` |
| `free_shipping_specific_items` | `STRUCT` |
| `free_shipping_specific_items.items` | `ARRAY<STRUCT>` |
| `free_shipping_specific_items.items.value` | `STRING` |
| `free_shipping_with_items_purchase` | `STRUCT` |
| `free_shipping_with_items_purchase.items` | `ARRAY<STRUCT>` |
| `free_shipping_with_items_purchase.items.value` | `STRING` |
| `free_shipping_with_items_purchase.shipping_methods` | `ARRAY<STRUCT>` |
| `free_shipping_with_items_purchase.shipping_methods.value` | `STRING` |
| `free_shipping_with_subtotal` | `STRUCT` |
| `free_shipping_with_subtotal.currency_code` | `STRING` |
| `free_shipping_with_subtotal.purchase_amount` | `NUMERIC` |
| `free_shipping_with_subtotal.shipping_methods` | `ARRAY<STRUCT>` |
| `free_shipping_with_subtotal.shipping_methods.value` | `STRING` |
| `hide_from_customer` | `BOOLEAN` |
| `merchant_code` | `STRING` |
| `merchant_notes` | `STRING` |
| `more_loyalty_cashback` | `STRUCT` |
| `more_loyalty_cashback.loyalty_cashback` | `NUMERIC` |
| `more_loyalty_points` | `STRUCT` |
| `more_loyalty_points.loyalty_points` | `NUMERIC` |
| `multiple_amounts_off_items` | `STRUCT` |
| `multiple_amounts_off_items.discounts` | `ARRAY<STRUCT>` |
| `multiple_amounts_off_items.discounts.discount_amount` | `NUMERIC` |
| `multiple_amounts_off_items.discounts.items` | `ARRAY<STRUCT>` |
| `multiple_amounts_off_items.discounts.items.value` | `STRING` |
| `multiple_amounts_off_items.limit` | `INTEGER` |
| `no_discount` | `STRUCT` |
| `no_discount.ignore_this_property` | `BOOLEAN` |
| `partition_oid` | `INTEGER` |
| `percent_more_loyalty_cashback` | `STRUCT` |
| `percent_more_loyalty_cashback.percent_more_loyalty_cashback` | `NUMERIC` |
| `percent_more_loyalty_points` | `STRUCT` |
| `percent_more_loyalty_points.percent_more_loyalty_points` | `NUMERIC` |
| `percent_off_item_with_items_quantity_purchase` | `STRUCT` |
| `percent_off_item_with_items_quantity_purchase.discount_percent` | `NUMERIC` |
| `percent_off_item_with_items_quantity_purchase.item_tags` | `ARRAY<STRUCT>` |
| `percent_off_item_with_items_quantity_purchase.item_tags.value` | `STRING` |
| `percent_off_item_with_items_quantity_purchase.items` | `ARRAY<STRUCT>` |
| `percent_off_item_with_items_quantity_purchase.items.value` | `STRING` |
| `percent_off_item_with_items_quantity_purchase.limit` | `INTEGER` |
| `percent_off_item_with_items_quantity_purchase.required_purchase_items` | `ARRAY<STRUCT>` |
| `percent_off_item_with_items_quantity_purchase.required_purchase_items.value` | `STRING` |
| `percent_off_item_with_items_quantity_purchase.required_purchase_items_tags` | `ARRAY<STRUCT>` |
| `percent_off_item_with_items_quantity_purchase.required_purchase_items_tags.value` | `STRING` |
| `percent_off_item_with_items_quantity_purchase.required_purchase_quantity` | `INTEGER` |
| `percent_off_items` | `STRUCT` |
| `percent_off_items.discount_percent` | `NUMERIC` |
| `percent_off_items.excluded_item_tags` | `ARRAY<STRUCT>` |
| `percent_off_items.excluded_item_tags.value` | `STRING` |
| `percent_off_items.excluded_items` | `ARRAY<STRUCT>` |
| `percent_off_items.excluded_items.value` | `STRING` |
| `percent_off_items.item_tags` | `ARRAY<STRUCT>` |
| `percent_off_items.item_tags.value` | `STRING` |
| `percent_off_items.items` | `ARRAY<STRUCT>` |
| `percent_off_items.items.value` | `STRING` |
| `percent_off_items.limit` | `INTEGER` |
| `percent_off_items_and_free_shipping` | `STRUCT` |
| `percent_off_items_and_free_shipping.discount_percent` | `NUMERIC` |
| `percent_off_items_and_free_shipping.excluded_item_tags` | `ARRAY<STRUCT>` |
| `percent_off_items_and_free_shipping.excluded_item_tags.value` | `STRING` |
| `percent_off_items_and_free_shipping.excluded_items` | `ARRAY<STRUCT>` |
| `percent_off_items_and_free_shipping.excluded_items.value` | `STRING` |
| `percent_off_items_and_free_shipping.item_tags` | `ARRAY<STRUCT>` |
| `percent_off_items_and_free_shipping.item_tags.value` | `STRING` |
| `percent_off_items_and_free_shipping.items` | `ARRAY<STRUCT>` |
| `percent_off_items_and_free_shipping.items.value` | `STRING` |
| `percent_off_items_and_free_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `percent_off_items_and_free_shipping.shipping_methods.value` | `STRING` |
| `percent_off_items_with_items_purchase` | `STRUCT` |
| `percent_off_items_with_items_purchase.discount_percent` | `NUMERIC` |
| `percent_off_items_with_items_purchase.item_tags` | `ARRAY<STRUCT>` |
| `percent_off_items_with_items_purchase.item_tags.value` | `STRING` |
| `percent_off_items_with_items_purchase.items` | `ARRAY<STRUCT>` |
| `percent_off_items_with_items_purchase.items.value` | `STRING` |
| `percent_off_items_with_items_purchase.limit` | `INTEGER` |
| `percent_off_items_with_items_purchase.required_purchase_items` | `ARRAY<STRUCT>` |
| `percent_off_items_with_items_purchase.required_purchase_items.value` | `STRING` |
| `percent_off_items_with_items_purchase.required_purchase_items_tags` | `ARRAY<STRUCT>` |
| `percent_off_items_with_items_purchase.required_purchase_items_tags.value` | `STRING` |
| `percent_off_items_with_minimum_item_amount` | `STRUCT` |
| `percent_off_items_with_minimum_item_amount.currency_code` | `STRING` |
| `percent_off_items_with_minimum_item_amount.discount_percent` | `NUMERIC` |
| `percent_off_items_with_minimum_item_amount.excluded_item_tags` | `ARRAY<STRUCT>` |
| `percent_off_items_with_minimum_item_amount.excluded_item_tags.value` | `STRING` |
| `percent_off_items_with_minimum_item_amount.excluded_items` | `ARRAY<STRUCT>` |
| `percent_off_items_with_minimum_item_amount.excluded_items.value` | `STRING` |
| `percent_off_items_with_minimum_item_amount.item_tags` | `ARRAY<STRUCT>` |
| `percent_off_items_with_minimum_item_amount.item_tags.value` | `STRING` |
| `percent_off_items_with_minimum_item_amount.items` | `ARRAY<STRUCT>` |
| `percent_off_items_with_minimum_item_amount.items.value` | `STRING` |
| `percent_off_items_with_minimum_item_amount.limit` | `INTEGER` |
| `percent_off_items_with_minimum_item_amount.minimum_item_amount` | `NUMERIC` |
| `percent_off_msrp_items` | `STRUCT` |
| `percent_off_msrp_items.discount_percent` | `NUMERIC` |
| `percent_off_msrp_items.excluded_items` | `ARRAY<STRUCT>` |
| `percent_off_msrp_items.excluded_items.value` | `STRING` |
| `percent_off_msrp_items.items` | `ARRAY<STRUCT>` |
| `percent_off_msrp_items.items.value` | `STRING` |
| `percent_off_msrp_items.limit` | `INTEGER` |
| `percent_off_msrp_items.minimum_cumulative_msrp` | `NUMERIC` |
| `percent_off_msrp_items.minimum_subtotal` | `NUMERIC` |
| `percent_off_retail_price_items` | `STRUCT` |
| `percent_off_retail_price_items.discount_percent` | `NUMERIC` |
| `percent_off_retail_price_items.excluded_items` | `ARRAY<STRUCT>` |
| `percent_off_retail_price_items.excluded_items.value` | `STRING` |
| `percent_off_retail_price_items.items` | `ARRAY<STRUCT>` |
| `percent_off_retail_price_items.items.value` | `STRING` |
| `percent_off_retail_price_items.limit` | `INTEGER` |
| `percent_off_shipping` | `STRUCT` |
| `percent_off_shipping.discount_percent` | `NUMERIC` |
| `percent_off_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `percent_off_shipping.shipping_methods.value` | `STRING` |
| `percent_off_subtotal` | `STRUCT` |
| `percent_off_subtotal.discount_percent` | `NUMERIC` |
| `percent_off_subtotal_and_free_shipping` | `STRUCT` |
| `percent_off_subtotal_and_free_shipping.discount_percent` | `NUMERIC` |
| `percent_off_subtotal_and_free_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `percent_off_subtotal_and_free_shipping.shipping_methods.value` | `STRING` |
| `percent_off_subtotal_limit` | `STRUCT` |
| `percent_off_subtotal_limit.currency_code` | `STRING` |
| `percent_off_subtotal_limit.discount_percent` | `NUMERIC` |
| `percent_off_subtotal_limit.limit` | `NUMERIC` |
| `percent_off_subtotal_with_items_purchase` | `STRUCT` |
| `percent_off_subtotal_with_items_purchase.discount_percent` | `NUMERIC` |
| `percent_off_subtotal_with_items_purchase.items` | `ARRAY<STRUCT>` |
| `percent_off_subtotal_with_items_purchase.items.value` | `STRING` |
| `percent_off_subtotal_with_subtotal` | `STRUCT` |
| `percent_off_subtotal_with_subtotal.currency_code` | `STRING` |
| `percent_off_subtotal_with_subtotal.discount_percent` | `NUMERIC` |
| `percent_off_subtotal_with_subtotal.subtotal_amount` | `NUMERIC` |
| `quickbooks_code` | `STRING` |
| `restrict_by_postal_codes` | `ARRAY<STRUCT>` |
| `restrict_by_postal_codes.value` | `STRING` |
| `restrict_by_screen_branding_theme_codes` | `ARRAY<STRUCT>` |
| `restrict_by_screen_branding_theme_codes.invalidForThis` | `BOOLEAN` |
| `restrict_by_screen_branding_theme_codes.name` | `STRING` |
| `restrict_by_screen_branding_theme_codes.validForThis` | `BOOLEAN` |
| `restrict_by_screen_branding_theme_codes.validOnlyForThis` | `BOOLEAN` |
| `restrict_by_storefronts` | `ARRAY<STRUCT>` |
| `restrict_by_storefronts.invalidForThis` | `BOOLEAN` |
| `restrict_by_storefronts.name` | `STRING` |
| `restrict_by_storefronts.validForThis` | `BOOLEAN` |
| `restrict_by_storefronts.validOnlyForThis` | `BOOLEAN` |
| `skip_on_rebill` | `BOOLEAN` |
| `start_dts` | `DATETIME` |
| `super_coupon` | `BOOLEAN` |
| `tiered_amount_off_items` | `STRUCT` |
| `tiered_amount_off_items.item_tags` | `ARRAY<STRUCT>` |
| `tiered_amount_off_items.item_tags.value` | `STRING` |
| `tiered_amount_off_items.items` | `ARRAY<STRUCT>` |
| `tiered_amount_off_items.items.value` | `STRING` |
| `tiered_amount_off_items.limit` | `NUMERIC` |
| `tiered_amount_off_items.tiers` | `ARRAY<STRUCT>` |
| `tiered_amount_off_items.tiers.discount_amount` | `NUMERIC` |
| `tiered_amount_off_items.tiers.item_quantity` | `INTEGER` |
| `tiered_amount_off_items.tiers.quickbooks_code` | `STRING` |
| `tiered_amount_off_subtotal` | `STRUCT` |
| `tiered_amount_off_subtotal.items` | `ARRAY<STRUCT>` |
| `tiered_amount_off_subtotal.items.value` | `STRING` |
| `tiered_amount_off_subtotal.tiers` | `ARRAY<STRUCT>` |
| `tiered_amount_off_subtotal.tiers.discount_amount` | `NUMERIC` |
| `tiered_amount_off_subtotal.tiers.quickbooks_code` | `STRING` |
| `tiered_amount_off_subtotal.tiers.subtotal_amount` | `NUMERIC` |
| `tiered_percent_off_items` | `STRUCT` |
| `tiered_percent_off_items.item_tags` | `ARRAY<STRUCT>` |
| `tiered_percent_off_items.item_tags.value` | `STRING` |
| `tiered_percent_off_items.items` | `ARRAY<STRUCT>` |
| `tiered_percent_off_items.items.value` | `STRING` |
| `tiered_percent_off_items.limit` | `NUMERIC` |
| `tiered_percent_off_items.tiers` | `ARRAY<STRUCT>` |
| `tiered_percent_off_items.tiers.discount_percent` | `NUMERIC` |
| `tiered_percent_off_items.tiers.item_quantity` | `INTEGER` |
| `tiered_percent_off_items.tiers.quickbooks_code` | `STRING` |
| `tiered_percent_off_shipping` | `STRUCT` |
| `tiered_percent_off_shipping.quickbooks_code` | `STRING` |
| `tiered_percent_off_shipping.shipping_methods` | `ARRAY<STRUCT>` |
| `tiered_percent_off_shipping.shipping_methods.value` | `STRING` |
| `tiered_percent_off_shipping.tiers` | `ARRAY<STRUCT>` |
| `tiered_percent_off_shipping.tiers.discount_percent` | `NUMERIC` |
| `tiered_percent_off_shipping.tiers.quickbooks_code` | `STRING` |
| `tiered_percent_off_shipping.tiers.subtotal_amount` | `NUMERIC` |
| `tiered_percent_off_subtotal` | `STRUCT` |
| `tiered_percent_off_subtotal.items` | `ARRAY<STRUCT>` |
| `tiered_percent_off_subtotal.items.value` | `STRING` |
| `tiered_percent_off_subtotal.tiers` | `ARRAY<STRUCT>` |
| `tiered_percent_off_subtotal.tiers.discount_percent` | `NUMERIC` |
| `tiered_percent_off_subtotal.tiers.quickbooks_code` | `STRING` |
| `tiered_percent_off_subtotal.tiers.subtotal_amount` | `NUMERIC` |
| `tiered_percent_off_subtotal_based_on_msrp` | `STRUCT` |
| `tiered_percent_off_subtotal_based_on_msrp.items` | `ARRAY<STRUCT>` |
| `tiered_percent_off_subtotal_based_on_msrp.items.value` | `STRING` |
| `tiered_percent_off_subtotal_based_on_msrp.tiers` | `ARRAY<STRUCT>` |
| `tiered_percent_off_subtotal_based_on_msrp.tiers.discount_percent` | `NUMERIC` |
| `tiered_percent_off_subtotal_based_on_msrp.tiers.quickbooks_code` | `STRING` |
| `tiered_percent_off_subtotal_based_on_msrp.tiers.subtotal_amount` | `NUMERIC` |
| `usable_by` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw.uc_coupons`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
