---
type: "UltraCart Table Definition"
title: "uc_storefront_upsell_path_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_upsell_path_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_upsell_path_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_upsell_path_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_storefront_upsell_path.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_storefront_upsell_path_streaming](/tables/ultracart_dw_streaming/uc_storefront_upsell_path_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
