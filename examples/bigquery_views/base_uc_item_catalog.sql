-- Grain: one row per merchant_item_oid.
-- Purpose: product/SKU dimension for order-item enrichment.
SELECT
  merchant_item_oid,
  merchant_item_id,
  merchant_id,
  creation_dts,
  last_modified_dts,
  description,
  pricing.cost AS item_price,
  pricing.cogs AS item_cogs,
  pricing.currency_code AS currency_code,
  physical.weight.value AS weight_value,
  physical.weight.uom AS weight_uom,
  auto_order.auto_orderable AS auto_orderable,
  auto_order.auto_order_upsell AS auto_order_upsell,
  ARRAY_LENGTH(tags.tags) AS tag_count,
  ARRAY_LENGTH(options) AS option_count
FROM `{{ source_project }}.{{ access_dataset }}.uc_items`;
