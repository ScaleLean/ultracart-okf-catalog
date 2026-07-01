-- Source inspiration: UltraCart public Data Warehouse auto-order cohort examples.
-- Grain: one row per subscription cohort month, primary item, and month number.
WITH auto_orders AS (
  SELECT
    auto_order_oid,
    items[SAFE_OFFSET(0)].original_item_id AS primary_item_id,
    DATE_TRUNC(DATE(original_order.creation_dts), MONTH) AS cohort_month,
    original_order.summary.subtotal.value - COALESCE(original_order.summary.subtotal_refunded.value, 0) AS original_net_revenue,
    ARRAY(
      SELECT AS STRUCT
        DATE_TRUNC(DATE(rebill.creation_dts), MONTH) AS activity_month,
        rebill.summary.subtotal.value - COALESCE(rebill.summary.subtotal_refunded.value, 0) AS net_revenue
      FROM UNNEST(rebill_orders) AS rebill
      WHERE rebill.payment.payment_dts IS NOT NULL
        AND COALESCE(rebill.payment.test_order, FALSE) IS FALSE
    ) AS rebill_activity
  FROM `{{ source_project }}.{{ access_dataset }}.uc_auto_orders`
  WHERE original_order.creation_dts IS NOT NULL
    AND original_order.payment.payment_dts IS NOT NULL
    AND COALESCE(original_order.payment.test_order, FALSE) IS FALSE
),
original_rows AS (
  SELECT
    cohort_month,
    primary_item_id,
    0 AS cohort_month_number,
    COUNT(*) AS auto_order_count,
    SUM(original_net_revenue) AS net_revenue
  FROM auto_orders
  GROUP BY cohort_month, primary_item_id
),
rebill_rows AS (
  SELECT
    auto_orders.cohort_month,
    auto_orders.primary_item_id,
    DATE_DIFF(rebill.activity_month, auto_orders.cohort_month, MONTH) AS cohort_month_number,
    COUNT(DISTINCT auto_orders.auto_order_oid) AS auto_order_count,
    SUM(rebill.net_revenue) AS net_revenue
  FROM auto_orders
  CROSS JOIN UNNEST(rebill_activity) AS rebill
  WHERE rebill.activity_month >= auto_orders.cohort_month
  GROUP BY auto_orders.cohort_month, auto_orders.primary_item_id, cohort_month_number
)
SELECT
  cohort_month,
  primary_item_id,
  cohort_month_number,
  SUM(auto_order_count) AS auto_order_count,
  ROUND(SUM(net_revenue), 2) AS net_revenue
FROM (
  SELECT
    cohort_month,
    primary_item_id,
    cohort_month_number,
    auto_order_count,
    net_revenue
  FROM original_rows
  UNION ALL
  SELECT
    cohort_month,
    primary_item_id,
    cohort_month_number,
    auto_order_count,
    net_revenue
  FROM rebill_rows
)
WHERE cohort_month >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL {{ lookback_days }} DAY), MONTH)
GROUP BY cohort_month, primary_item_id, cohort_month_number
ORDER BY cohort_month DESC, primary_item_id, cohort_month_number;
