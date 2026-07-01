-- Grain: one row per non-kit order item line.
-- Purpose: SKU sales and product-mix analysis without multiplying order facts.
WITH orders AS (
  SELECT
    order_id,
    merchant_id,
    creation_dts,
    DATE(creation_dts) AS order_date,
    customer_profile.customer_profile_oid AS customer_profile_oid,
    COALESCE(customer_profile.email_hash, billing.email_hash) AS customer_hash,
    auto_order.auto_order_oid AS auto_order_oid,
    items
  FROM `{{ source_project }}.{{ access_dataset }}.uc_orders`
  WHERE COALESCE(payment.test_order, FALSE) IS FALSE
)
SELECT
  o.order_id,
  o.merchant_id,
  o.creation_dts,
  o.order_date,
  o.customer_profile_oid,
  o.customer_hash,
  o.auto_order_oid,
  item.item_index,
  item.merchant_item_id,
  item.description,
  item.quantity,
  COALESCE(item.upsell, FALSE) AS is_upsell,
  COALESCE(item.kit_component, FALSE) AS is_kit_component,
  item.cost.value AS item_unit_price,
  item.total_cost_with_discount.value AS item_revenue_after_discount,
  item.cogs AS item_cogs,
  COALESCE(item.total_cost_with_discount.value, item.quantity * item.cost.value, 0) - COALESCE(item.cogs, 0) AS item_gross_profit
FROM orders AS o
CROSS JOIN UNNEST(o.items) AS item
WHERE NOT COALESCE(item.kit_component, FALSE);
