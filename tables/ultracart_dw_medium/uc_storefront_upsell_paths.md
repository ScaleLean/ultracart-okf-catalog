---
type: "BigQuery View"
title: "ultracart_dw_medium.uc_storefront_upsell_paths"
description: "Upsell path configuration."
resource: "urn:ultracart:bigquery:object:ultracart_dw_medium.uc_storefront_upsell_paths"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_medium"
  - "uc_storefront_upsell_paths"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_medium.uc_storefront_upsell_paths

Upsell path configuration.

## Definition

- Dataset: [ultracart_dw_medium](/datasets/ultracart_dw_medium.md)
- Object name: `uc_storefront_upsell_paths`
- Object type: `VIEW`
- Table family: [storefront_content](/references/table_families.md#storefront-content)
- Grain: One upsell path row per storefront_upsell_path_oid.
- Canonical definition: [uc_storefront_upsell_paths](/concepts/tables_by_name/uc_storefront_upsell_paths.md)

## Schema Coverage

- Field paths: 45
- Array fields: 10
- Struct fields: 12

## Field Paths

| Field path | Data type |
|---|---|
| `active` | `BOOLEAN` |
| `archived` | `BOOLEAN` |
| `customer_type` | `INTEGER` |
| `location` | `STRING` |
| `name` | `STRING` |
| `partition_oid` | `INTEGER` |
| `path_order` | `INTEGER` |
| `path_type` | `STRING` |
| `storefront_oid` | `INTEGER` |
| `storefront_upsell_path_oid` | `INTEGER` |
| `suppression_item_logic` | `STRING` |
| `suppression_items` | `ARRAY<STRUCT>` |
| `suppression_items.comparison` | `INTEGER` |
| `suppression_items.item_id` | `STRING` |
| `suppression_items.operator` | `STRING` |
| `suppression_total_quantity_comparison` | `INTEGER` |
| `suppression_total_quantity_operator` | `STRING` |
| `trigger_ages` | `ARRAY<STRUCT>` |
| `trigger_ages.value` | `STRING` |
| `trigger_genders` | `ARRAY<STRUCT>` |
| `trigger_genders.value` | `STRING` |
| `trigger_item_ids` | `ARRAY<STRUCT>` |
| `trigger_item_ids.value` | `STRING` |
| `trigger_item_logic` | `STRING` |
| `trigger_items` | `ARRAY<STRUCT>` |
| `trigger_items.comparison` | `INTEGER` |
| `trigger_items.item_id` | `STRING` |
| `trigger_items.operator` | `STRING` |
| `trigger_tags` | `ARRAY<STRUCT>` |
| `trigger_tags.value` | `STRING` |
| `trigger_total_quantity_comparison` | `INTEGER` |
| `trigger_total_quantity_operator` | `STRING` |
| `variations` | `ARRAY<STRUCT>` |
| `variations.name` | `STRING` |
| `variations.steps` | `ARRAY<STRUCT>` |
| `variations.steps.experiment` | `STRUCT` |
| `variations.steps.experiment.offers` | `ARRAY<STRUCT>` |
| `variations.steps.experiment.offers.downsell_offer_oid` | `INTEGER` |
| `variations.steps.experiment.offers.offer_oid` | `INTEGER` |
| `variations.steps.offer` | `STRUCT` |
| `variations.steps.offer.downsell_offer_oid` | `INTEGER` |
| `variations.steps.offer.offer_oid` | `INTEGER` |
| `variations.steps.type` | `STRING` |
| `variations.visibility_ordered_offer_oids` | `ARRAY<STRUCT>` |
| `variations.visibility_ordered_offer_oids.value` | `INTEGER` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_medium.uc_storefront_upsell_paths`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
