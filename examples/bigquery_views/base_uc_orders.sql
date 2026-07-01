-- Grain: one row per UltraCart order_id.
-- Purpose: safe commerce fact for dashboards, marts, and agent reasoning.
WITH source_orders AS (
  SELECT
    order_id,
    merchant_id,
    creation_dts,
    DATE(creation_dts) AS order_date,
    current_stage,
    channel_partner.channel_partner_code AS channel_partner_code,
    customer_profile.customer_profile_oid AS customer_profile_oid,
    COALESCE(customer_profile.email_hash, billing.email_hash) AS customer_hash,
    auto_order.auto_order_oid AS auto_order_oid,
    auto_order.original_order_id AS original_order_id,
    payment.test_order AS is_test_order,
    summary.subtotal.value AS subtotal,
    summary.subtotal_discount.value AS subtotal_discount,
    summary.subtotal_refunded.value AS subtotal_refunded,
    summary.total.value AS total,
    summary.total_refunded.value AS total_refunded,
    summary.tax.value AS tax,
    summary.shipping_handling_total.value AS shipping_handling_total,
    items
  FROM `{{ source_project }}.{{ access_dataset }}.uc_orders`
  WHERE COALESCE(payment.test_order, FALSE) IS FALSE
),
item_rollup AS (
  SELECT
    order_id,
    COUNTIF(NOT COALESCE(item.kit_component, FALSE)) AS item_count,
    COUNTIF(NOT COALESCE(item.kit_component, FALSE) AND COALESCE(item.upsell, FALSE)) AS upsell_item_count,
    COUNTIF(NOT COALESCE(item.kit_component, FALSE) AND NOT COALESCE(item.upsell, FALSE)) AS regular_item_count,
    SUM(IF(NOT COALESCE(item.kit_component, FALSE), item.quantity, 0)) AS quantity_sold,
    SUM(IF(NOT COALESCE(item.kit_component, FALSE), COALESCE(item.cogs, 0), 0)) AS order_cogs,
    SUM(IF(NOT COALESCE(item.kit_component, FALSE), item.quantity * COALESCE(item.cost.value, 0), 0)) AS item_subtotal,
    SUM(IF(NOT COALESCE(item.kit_component, FALSE), COALESCE(item.total_cost_with_discount.value, item.quantity * item.cost.value, 0), 0)) AS item_revenue_after_discount
  FROM source_orders
  LEFT JOIN UNNEST(items) AS item
  GROUP BY order_id
)
SELECT
  o.order_id,
  o.merchant_id,
  o.creation_dts,
  o.order_date,
  o.current_stage,
    o.channel_partner_code,
  o.customer_profile_oid,
  o.customer_hash,
  CASE
    WHEN o.auto_order_oid IS NULL THEN 'one_time'
    WHEN o.original_order_id IS NULL OR o.original_order_id = o.order_id THEN 'subscription_creation'
    ELSE 'subscription_rebill'
  END AS subscription_type,
  o.auto_order_oid,
  o.original_order_id,
  o.subtotal,
  o.subtotal_discount,
  o.subtotal_refunded,
  o.total,
  o.total_refunded,
  o.tax,
  o.shipping_handling_total,
  COALESCE(r.item_count, 0) AS item_count,
  COALESCE(r.regular_item_count, 0) AS regular_item_count,
  COALESCE(r.upsell_item_count, 0) AS upsell_item_count,
  COALESCE(r.quantity_sold, 0) AS quantity_sold,
  COALESCE(r.order_cogs, 0) AS order_cogs,
  COALESCE(r.item_subtotal, 0) AS item_subtotal,
  COALESCE(r.item_revenue_after_discount, 0) AS item_revenue_after_discount,
  COALESCE(o.subtotal, 0) - COALESCE(r.order_cogs, 0) AS gross_profit
FROM source_orders AS o
LEFT JOIN item_rollup AS r USING (order_id);
