---
type: "BigQuery View"
title: "ultracart_dw_low.uc_storefront_upsell_offers"
description: "Upsell offer configuration."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_storefront_upsell_offers"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_storefront_upsell_offers"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_storefront_upsell_offers

Upsell offer configuration.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_storefront_upsell_offers`
- Object type: `VIEW`
- Table family: [storefront_content](/references/table_families.md#storefront-content)
- Grain: One upsell offer row per storefront_upsell_offer_oid.
- Canonical definition: [uc_storefront_upsell_offers](/concepts/tables_by_name/uc_storefront_upsell_offers.md)

## Schema Coverage

- Field paths: 103
- Array fields: 21
- Struct fields: 21

## Field Paths

| Field path | Data type |
|---|---|
| `active` | `BOOLEAN` |
| `add_accessory_item_ids` | `ARRAY<STRUCT>` |
| `add_accessory_item_ids.value` | `STRING` |
| `allow_upsell_item_in_cart_already` | `BOOLEAN` |
| `arbitrary_unit_cost` | `NUMERIC` |
| `arbitrary_unit_cost_friday` | `NUMERIC` |
| `arbitrary_unit_cost_monday` | `NUMERIC` |
| `arbitrary_unit_cost_saturday` | `NUMERIC` |
| `arbitrary_unit_cost_sunday` | `NUMERIC` |
| `arbitrary_unit_cost_thursday` | `NUMERIC` |
| `arbitrary_unit_cost_tuesday` | `NUMERIC` |
| `arbitrary_unit_cost_wednesday` | `NUMERIC` |
| `end_date` | `DATETIME` |
| `first_time_item` | `BOOLEAN` |
| `first_time_store` | `BOOLEAN` |
| `free_shipping` | `BOOLEAN` |
| `lock_shipping` | `BOOLEAN` |
| `max_quantity` | `INTEGER` |
| `migrate_accessory_item_ids_from` | `ARRAY<STRUCT>` |
| `migrate_accessory_item_ids_from.value` | `STRING` |
| `migrate_accessory_item_ids_to` | `ARRAY<STRUCT>` |
| `migrate_accessory_item_ids_to.value` | `STRING` |
| `name` | `STRING` |
| `offer_container_cjson` | `STRING` |
| `offsite_content_url` | `STRING` |
| `partition_oid` | `INTEGER` |
| `path_location` | `STRING` |
| `path_name` | `STRING` |
| `removable_on_confirmation` | `BOOLEAN` |
| `remove_accessory_item_ids` | `ARRAY<STRUCT>` |
| `remove_accessory_item_ids.value` | `STRING` |
| `remove_trigger_item` | `BOOLEAN` |
| `require_all_trigger_item_ids` | `BOOLEAN` |
| `screenshot_large_full_length_url` | `STRING` |
| `screenshot_large_view_port_url` | `STRING` |
| `screenshot_medium_full_length_url` | `STRING` |
| `screenshot_medium_view_port_url` | `STRING` |
| `screenshot_small_full_length_url` | `STRING` |
| `screenshot_small_view_port_url` | `STRING` |
| `skip_previous_customers` | `BOOLEAN` |
| `start_date` | `DATETIME` |
| `storefront_oid` | `INTEGER` |
| `storefront_upsell_offer_oid` | `INTEGER` |
| `suppress_large` | `BOOLEAN` |
| `suppress_medium` | `BOOLEAN` |
| `suppress_small` | `BOOLEAN` |
| `suppression_count_across_all_trigger_items` | `BOOLEAN` |
| `suppression_country_codes` | `ARRAY<STRUCT>` |
| `suppression_country_codes.value` | `STRING` |
| `suppression_item_ids` | `ARRAY<STRUCT>` |
| `suppression_item_ids.value` | `STRING` |
| `suppression_item_logic` | `STRING` |
| `suppression_items` | `ARRAY<STRUCT>` |
| `suppression_items.comparison` | `INTEGER` |
| `suppression_items.item_id` | `STRING` |
| `suppression_items.operator` | `STRING` |
| `suppression_operator` | `STRING` |
| `suppression_operator_comparison_quantity` | `INTEGER` |
| `suppression_payment_methods` | `ARRAY<STRUCT>` |
| `suppression_payment_methods.value` | `STRING` |
| `suppression_shipping_methods` | `ARRAY<STRUCT>` |
| `suppression_shipping_methods.value` | `STRING` |
| `suppression_state_codes` | `ARRAY<STRUCT>` |
| `suppression_state_codes.value` | `STRING` |
| `suppression_tags` | `ARRAY<STRUCT>` |
| `suppression_tags.value` | `STRING` |
| `suppression_total_quantity_comparison` | `INTEGER` |
| `suppression_total_quantity_operator` | `STRING` |
| `test_only` | `BOOLEAN` |
| `thumbnail_large_full_length_url` | `STRING` |
| `thumbnail_large_view_port_url` | `STRING` |
| `thumbnail_medium_full_length_url` | `STRING` |
| `thumbnail_medium_view_port_url` | `STRING` |
| `thumbnail_small_full_length_url` | `STRING` |
| `thumbnail_small_view_port_url` | `STRING` |
| `trigger_ages` | `ARRAY<STRUCT>` |
| `trigger_ages.value` | `STRING` |
| `trigger_count_across_all_trigger_items` | `BOOLEAN` |
| `trigger_country_codes` | `ARRAY<STRUCT>` |
| `trigger_country_codes.value` | `STRING` |
| `trigger_genders` | `ARRAY<STRUCT>` |
| `trigger_genders.value` | `STRING` |
| `trigger_item_ids` | `ARRAY<STRUCT>` |
| `trigger_item_ids.value` | `STRING` |
| `trigger_item_logic` | `STRING` |
| `trigger_items` | `ARRAY<STRUCT>` |
| `trigger_items.comparison` | `INTEGER` |
| `trigger_items.item_id` | `STRING` |
| `trigger_items.operator` | `STRING` |
| `trigger_operator` | `STRING` |
| `trigger_operator_comparison_quantity` | `INTEGER` |
| `trigger_payment_methods` | `ARRAY<STRUCT>` |
| `trigger_payment_methods.value` | `STRING` |
| `trigger_shipping_methods` | `ARRAY<STRUCT>` |
| `trigger_shipping_methods.value` | `STRING` |
| `trigger_state_codes` | `ARRAY<STRUCT>` |
| `trigger_state_codes.value` | `STRING` |
| `trigger_tags` | `ARRAY<STRUCT>` |
| `trigger_tags.value` | `STRING` |
| `trigger_total_quantity_comparison` | `INTEGER` |
| `trigger_total_quantity_operator` | `STRING` |
| `upsell_item_ids` | `ARRAY<STRUCT>` |
| `upsell_item_ids.value` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_low.uc_storefront_upsell_offers`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
