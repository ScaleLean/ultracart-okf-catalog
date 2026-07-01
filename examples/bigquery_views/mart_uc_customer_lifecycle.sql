-- Grain: one row per customer_profile_oid/customer_hash.
-- Purpose: lifecycle/RFM example from safe customer and order surfaces.
WITH orders AS (
  SELECT
    customer_profile_oid,
    customer_hash,
    order_date,
    subtotal,
    gross_profit,
    subscription_type
  FROM `{{ target_project }}.{{ target_dataset }}.base_uc_orders`
),
customers AS (
  SELECT
    customer_profile_oid,
    customer_hash,
    signup_dts,
    marketing_consent,
    global_unsubscribed
  FROM `{{ target_project }}.{{ target_dataset }}.base_uc_customers`
),
subscriptions AS (
  SELECT
    customer_profile_oid,
    customer_hash,
    COUNTIF(enabled) AS active_auto_orders,
    COUNT(*) AS lifetime_auto_orders
  FROM `{{ target_project }}.{{ target_dataset }}.base_uc_auto_orders`
  GROUP BY customer_profile_oid, customer_hash
),
order_rollup AS (
  SELECT
    customer_profile_oid,
    customer_hash,
    COUNT(*) AS order_count,
    SUM(subtotal) AS lifetime_subtotal,
    SUM(gross_profit) AS lifetime_gross_profit,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date,
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) AS days_since_last_order,
    COUNTIF(subscription_type = 'subscription_creation') AS subscription_creation_orders,
    COUNTIF(subscription_type = 'subscription_rebill') AS subscription_rebill_orders
  FROM orders
  WHERE customer_hash IS NOT NULL OR customer_profile_oid IS NOT NULL
  GROUP BY customer_profile_oid, customer_hash
)
SELECT
  COALESCE(r.customer_profile_oid, c.customer_profile_oid, s.customer_profile_oid) AS customer_profile_oid,
  COALESCE(r.customer_hash, c.customer_hash, s.customer_hash) AS customer_hash,
  c.signup_dts,
  c.marketing_consent,
  c.global_unsubscribed,
  r.order_count,
  r.lifetime_subtotal,
  r.lifetime_gross_profit,
  SAFE_DIVIDE(r.lifetime_subtotal, NULLIF(r.order_count, 0)) AS average_order_value,
  r.first_order_date,
  r.last_order_date,
  r.days_since_last_order,
  COALESCE(s.active_auto_orders, 0) AS active_auto_orders,
  COALESCE(s.lifetime_auto_orders, 0) AS lifetime_auto_orders,
  r.subscription_creation_orders,
  r.subscription_rebill_orders,
  CASE
    WHEN r.order_count IS NULL THEN 'no_orders'
    WHEN r.days_since_last_order <= 30 THEN 'active_30d'
    WHEN r.days_since_last_order <= 90 THEN 'active_90d'
    WHEN r.days_since_last_order <= 365 THEN 'lapsed_365d'
    ELSE 'dormant'
  END AS lifecycle_segment
FROM order_rollup AS r
FULL OUTER JOIN customers AS c
  ON r.customer_profile_oid = c.customer_profile_oid
  OR (r.customer_profile_oid IS NULL AND r.customer_hash = c.customer_hash)
FULL OUTER JOIN subscriptions AS s
  ON COALESCE(r.customer_profile_oid, c.customer_profile_oid) = s.customer_profile_oid
  OR (
    COALESCE(r.customer_profile_oid, c.customer_profile_oid) IS NULL
    AND COALESCE(r.customer_hash, c.customer_hash) = s.customer_hash
  );
