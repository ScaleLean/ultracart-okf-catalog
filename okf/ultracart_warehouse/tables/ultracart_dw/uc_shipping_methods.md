---
type: "BigQuery View"
title: "ultracart_dw.uc_shipping_methods"
description: "Shipping method configuration."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_shipping_methods"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_shipping_methods"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_shipping_methods

Shipping method configuration.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_shipping_methods`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One shipping method row per shipping_method_oid.
- Canonical definition: [uc_shipping_methods](/concepts/tables_by_name/uc_shipping_methods.md)

## Schema Coverage

- Field paths: 197
- Array fields: 17
- Struct fields: 28

## Field Paths

| Field path | Data type |
|---|---|
| `account_code` | `STRING` |
| `allow_third_party_billing` | `BOOLEAN` |
| `allow_third_party_billing_approved_customers_only` | `BOOLEAN` |
| `allowed_for_free_shipping` | `BOOLEAN` |
| `allowed_for_free_shipping_comparison` | `STRING` |
| `allowed_for_free_shipping_uom_weight` | `STRING` |
| `allowed_for_free_shipping_us48` | `BOOLEAN` |
| `allowed_for_free_shipping_weight` | `STRUCT` |
| `allowed_for_free_shipping_weight.uom` | `STRING` |
| `allowed_for_free_shipping_weight.value` | `NUMERIC` |
| `apo_fpo_markup` | `NUMERIC` |
| `beoe_only` | `BOOLEAN` |
| `blackouts` | `ARRAY<STRUCT>` |
| `blackouts.blacked_out_date` | `DATETIME` |
| `calculation_type` | `STRING` |
| `comment` | `STRING` |
| `commercial_percentage_discount` | `NUMERIC` |
| `cost_ranges` | `ARRAY<STRUCT>` |
| `cost_ranges.minimum_cost` | `NUMERIC` |
| `cost_ranges.shipping_cost` | `NUMERIC` |
| `countries` | `ARRAY<STRUCT>` |
| `countries.country` | `STRING` |
| `countries.handling_charge` | `NUMERIC` |
| `countries.maximumPackageLength` | `STRUCT` |
| `countries.maximumPackageLength.uom` | `STRING` |
| `countries.maximumPackageLength.value` | `NUMERIC` |
| `countries.maximum_customs_value` | `NUMERIC` |
| `custom_tracking_url` | `STRING` |
| `delivery_on_friday` | `BOOLEAN` |
| `delivery_on_monday` | `BOOLEAN` |
| `delivery_on_saturday` | `BOOLEAN` |
| `delivery_on_sunday` | `BOOLEAN` |
| `delivery_on_thursday` | `BOOLEAN` |
| `delivery_on_tuesday` | `BOOLEAN` |
| `delivery_on_wednesday` | `BOOLEAN` |
| `disabled` | `BOOLEAN` |
| `discount_if_item_count` | `INTEGER` |
| `discount_if_order_subtotal` | `NUMERIC` |
| `discount_if_order_subtotal_and_us48` | `NUMERIC` |
| `disocunt_if_cheapest` | `BOOLEAN` |
| `display_name` | `STRING` |
| `each_additional_item_markup` | `NUMERIC` |
| `estimated_delivery_num1` | `INTEGER` |
| `estimated_delivery_num2` | `INTEGER` |
| `estimated_delivery_type` | `STRING` |
| `export_as_shipping_method` | `STRING` |
| `filter_other_methods_when_available` | `BOOLEAN` |
| `first_item_markup` | `NUMERIC` |
| `flat_fee_markup` | `NUMERIC` |
| `force_to_distribution_center_oid` | `INTEGER` |
| `hazmat_fee_per_entire_shipment` | `NUMERIC` |
| `hazmat_fee_per_package` | `NUMERIC` |
| `individual_package_comparison` | `STRING` |
| `individual_package_uom_Weight` | `STRING` |
| `individual_package_weight` | `STRUCT` |
| `individual_package_weight.uom` | `STRING` |
| `individual_package_weight.value` | `NUMERIC` |
| `insurance_calculation_type` | `STRING` |
| `insurance_threshold` | `NUMERIC` |
| `insurance_unit` | `NUMERIC` |
| `insurance_unit_cost` | `NUMERIC` |
| `invalid_for_restrictions` | `ARRAY<STRUCT>` |
| `invalid_for_restrictions.value` | `STRING` |
| `invalid_for_screen_branding_theme_restrictions` | `ARRAY<STRUCT>` |
| `invalid_for_screen_branding_theme_restrictions.value` | `STRING` |
| `item_costs` | `ARRAY<STRUCT>` |
| `item_costs.cost` | `NUMERIC` |
| `item_costs.each_additional_item_markup` | `NUMERIC` |
| `item_costs.filter_to_if_available` | `BOOLEAN` |
| `item_costs.first_item_markup` | `NUMERIC` |
| `item_costs.fixed_shipping_cost` | `NUMERIC` |
| `item_costs.flat_fee_markup` | `NUMERIC` |
| `item_costs.free_shipping` | `BOOLEAN` |
| `item_costs.item_currency_code` | `STRING` |
| `item_costs.merchant_item_id` | `STRING` |
| `item_costs.merchant_item_oid` | `INTEGER` |
| `item_costs.per_item_fee_markup` | `NUMERIC` |
| `item_costs.percentage_markup` | `NUMERIC` |
| `item_costs.percentage_of_item_markup` | `NUMERIC` |
| `item_costs.relax_restrictions_on_upsell` | `BOOLEAN` |
| `item_costs.shipping_method_validity` | `STRING` |
| `item_costs.signature_required` | `BOOLEAN` |
| `least_cost_routes` | `ARRAY<STRUCT>` |
| `least_cost_routes.maximum_longest_dimension` | `STRUCT` |
| `least_cost_routes.maximum_longest_dimension.uom` | `STRING` |
| `least_cost_routes.maximum_longest_dimension.value` | `NUMERIC` |
| `least_cost_routes.maximum_second_longest_dimension` | `STRUCT` |
| `least_cost_routes.maximum_second_longest_dimension.uom` | `STRING` |
| `least_cost_routes.maximum_second_longest_dimension.value` | `NUMERIC` |
| `least_cost_routes.maximum_subtotal` | `NUMERIC` |
| `least_cost_routes.maximum_weight` | `STRUCT` |
| `least_cost_routes.maximum_weight.uom` | `STRING` |
| `least_cost_routes.maximum_weight.value` | `NUMERIC` |
| `least_cost_routes.route_to_shipping_method_oid` | `INTEGER` |
| `least_cost_routes.shipping_method_last_cost_route_oid` | `INTEGER` |
| `life_gate_fee` | `NUMERIC` |
| `life_gate_option` | `BOOLEAN` |
| `life_gate_required_for_residential` | `BOOLEAN` |
| `limit_package_weight` | `STRUCT` |
| `limit_package_weight.uom` | `STRING` |
| `limit_package_weight.value` | `NUMERIC` |
| `max_weight` | `STRUCT` |
| `max_weight.uom` | `STRING` |
| `max_weight.value` | `NUMERIC` |
| `maximum_insured_value` | `NUMERIC` |
| `maximum_order_fee` | `NUMERIC` |
| `maximum_package_count` | `INTEGER` |
| `maximum_value` | `NUMERIC` |
| `merchant_id` | `STRING` |
| `minimum_cost` | `NUMERIC` |
| `minimum_order_fee_limit` | `NUMERIC` |
| `no_realtime_charge` | `BOOLEAN` |
| `order_day_cutoff_time` | `DATETIME` |
| `order_days_before` | `INTEGER` |
| `packages` | `ARRAY<STRUCT>` |
| `packages.package_oid` | `INTEGER` |
| `partition_oid` | `INTEGER` |
| `percent_ranges` | `ARRAY<STRUCT>` |
| `percent_ranges.minimum_cost` | `NUMERIC` |
| `percent_ranges.percentage` | `NUMERIC` |
| `percentage_markup` | `NUMERIC` |
| `pickup` | `BOOLEAN` |
| `po_box_markup` | `NUMERIC` |
| `pricing_tier_markup` | `ARRAY<STRUCT>` |
| `pricing_tier_markup.apo_fpo_markup` | `NUMERIC` |
| `pricing_tier_markup.each_additional_item_markup` | `NUMERIC` |
| `pricing_tier_markup.first_item_markup` | `NUMERIC` |
| `pricing_tier_markup.flat_fee_markup` | `NUMERIC` |
| `pricing_tier_markup.hazmat_fee_per_entire_shipment` | `NUMERIC` |
| `pricing_tier_markup.hazmat_fee_per_package` | `NUMERIC` |
| `pricing_tier_markup.lift_gate_fee` | `NUMERIC` |
| `pricing_tier_markup.minimum_order_fee` | `NUMERIC` |
| `pricing_tier_markup.minimum_order_fee_limit` | `NUMERIC` |
| `pricing_tier_markup.percentage_markup` | `NUMERIC` |
| `pricing_tier_markup.po_box_markup` | `NUMERIC` |
| `pricing_tier_markup.pricing_tier_oid` | `INTEGER` |
| `pricing_tier_markup.residential_markup` | `NUMERIC` |
| `pricing_tier_markup.saturday_fee` | `NUMERIC` |
| `pricing_tier_markup.shipping_method_pricing_tier_markup_oid` | `INTEGER` |
| `pricing_tier_restrictions` | `ARRAY<STRUCT>` |
| `pricing_tier_restrictions.pricing_tier_oid` | `INTEGER` |
| `pricing_tier_restrictions.validity` | `STRING` |
| `radius_miles` | `INTEGER` |
| `radius_zip_codes` | `STRING` |
| `require_delivery_date` | `BOOLEAN` |
| `residential_markup` | `NUMERIC` |
| `residential_percentage_discount` | `NUMERIC` |
| `restrict_shipment_on_friday` | `BOOLEAN` |
| `restrict_shipment_on_monday` | `BOOLEAN` |
| `restrict_shipment_on_saturday` | `BOOLEAN` |
| `restrict_shipment_on_sunday` | `BOOLEAN` |
| `restrict_shipment_on_thursday` | `BOOLEAN` |
| `restrict_shipment_on_tuesday` | `BOOLEAN` |
| `restrict_shipment_on_wednesday` | `BOOLEAN` |
| `saturday_fee` | `NUMERIC` |
| `shipment_cut_off_time_friday` | `DATETIME` |
| `shipment_cut_off_time_monday` | `DATETIME` |
| `shipment_cut_off_time_saturday` | `DATETIME` |
| `shipment_cut_off_time_sunday` | `DATETIME` |
| `shipment_cut_off_time_thursday` | `DATETIME` |
| `shipment_cut_off_time_tuesday` | `DATETIME` |
| `shipment_cut_off_time_wednesday` | `DATETIME` |
| `shipping_method` | `STRING` |
| `shipping_method_discounts` | `ARRAY<STRUCT>` |
| `shipping_method_discounts.commercial_percentage_discount` | `NUMERIC` |
| `shipping_method_discounts.minimum_weight` | `STRUCT` |
| `shipping_method_discounts.minimum_weight.uom` | `STRING` |
| `shipping_method_discounts.minimum_weight.value` | `NUMERIC` |
| `shipping_method_discounts.residential_percentage_discount` | `NUMERIC` |
| `shipping_method_oid` | `INTEGER` |
| `signature_required` | `NUMERIC` |
| `states` | `ARRAY<STRUCT>` |
| `states.country` | `STRING` |
| `states.handling_charge` | `NUMERIC` |
| `states.province_state` | `STRING` |
| `total_shipment_comparison` | `STRING` |
| `total_shipment_uom_weight` | `STRING` |
| `total_shipment_weight` | `STRUCT` |
| `total_shipment_weight.uom` | `STRING` |
| `total_shipment_weight.value` | `NUMERIC` |
| `tracking_number_type` | `STRING` |
| `uom_weight` | `STRING` |
| `valid_only_for_restrictions` | `ARRAY<STRUCT>` |
| `valid_only_for_restrictions.value` | `STRING` |
| `valid_only_for_screen_branding_theme_restrictions` | `ARRAY<STRUCT>` |
| `valid_only_for_screen_branding_theme_restrictions.value` | `STRING` |
| `valid_only_zip_codes` | `STRING` |
| `weight_ranges` | `ARRAY<STRUCT>` |
| `weight_ranges.minimum_weight` | `STRUCT` |
| `weight_ranges.minimum_weight.uom` | `STRING` |
| `weight_ranges.minimum_weight.value` | `NUMERIC` |
| `weight_ranges.shipping_cost` | `NUMERIC` |
| `weight_ranges.uom_weight` | `STRING` |
| `zip_percentage_markup` | `ARRAY<STRUCT>` |
| `zip_percentage_markup.markup_percentage` | `NUMERIC` |
| `zip_percentage_markup.shipping_method_zip_percentage_range_oid` | `INTEGER` |
| `zip_percentage_markup.zip_range` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw.uc_shipping_methods`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
