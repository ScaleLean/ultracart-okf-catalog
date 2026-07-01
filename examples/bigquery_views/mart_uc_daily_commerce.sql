-- Grain: one row per order_date.
-- Purpose: compact commerce KPI rollup built from base_uc_orders.
WITH orders AS (
  SELECT
    order_date,
    customer_hash,
    subscription_type,
    subtotal,
    subtotal_discount,
    subtotal_refunded,
    total,
    total_refunded,
    order_cogs,
    gross_profit,
    item_count,
    quantity_sold
  FROM `{{ target_project }}.{{ target_dataset }}.base_uc_orders`
)
SELECT
  order_date,
  COUNT(*) AS order_count,
  COUNT(DISTINCT customer_hash) AS customer_count,
  COUNTIF(subscription_type = 'one_time') AS one_time_order_count,
  COUNTIF(subscription_type = 'subscription_creation') AS subscription_creation_order_count,
  COUNTIF(subscription_type = 'subscription_rebill') AS subscription_rebill_order_count,
  SUM(subtotal) AS subtotal,
  SUM(subtotal_discount) AS subtotal_discount,
  SUM(subtotal_refunded) AS subtotal_refunded,
  SUM(total) AS total,
  SUM(total_refunded) AS total_refunded,
  SUM(order_cogs) AS order_cogs,
  SUM(gross_profit) AS gross_profit,
  SAFE_DIVIDE(SUM(gross_profit), NULLIF(SUM(subtotal), 0)) AS gross_margin,
  SUM(item_count) AS item_count,
  SUM(quantity_sold) AS quantity_sold
FROM orders
GROUP BY order_date;
