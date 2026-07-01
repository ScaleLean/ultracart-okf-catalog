-- Source inspiration: UltraCart public Data Warehouse sample queries "Coupon Usage Summary" and "Coupon Usage Detail".
-- Grain: one row per base coupon code for paid, non-test orders.
WITH order_coupon_rows AS (
  SELECT
    order_header.order_id,
    DATE(TIMESTAMP(order_header.creation_dts), "{{ time_zone }}") AS order_date,
    UPPER(coupon.base_coupon_code) AS base_coupon_code,
    UPPER(coupon.coupon_code) AS coupon_code,
    COALESCE(order_header.summary.subtotal.value, 0)
      - COALESCE(order_header.summary.subtotal_discount.value, 0) AS subtotal_after_discount,
    COALESCE(order_header.summary.total.value, 0)
      - COALESCE(order_header.summary.total_refunded.value, 0) AS net_total
  FROM `{{ source_project }}.{{ access_dataset }}.uc_orders` AS order_header
  CROSS JOIN UNNEST(order_header.coupons) AS coupon
  WHERE DATE(TIMESTAMP(order_header.creation_dts), "{{ time_zone }}")
      >= DATE_SUB(CURRENT_DATE("{{ time_zone }}"), INTERVAL {{ lookback_days }} DAY)
    AND order_header.payment.payment_dts IS NOT NULL
    AND COALESCE(order_header.payment.test_order, FALSE) IS FALSE
)
SELECT
  base_coupon_code,
  COUNT(DISTINCT order_id) AS order_count,
  COUNT(DISTINCT coupon_code) AS distinct_coupon_code_count,
  MIN(order_date) AS first_order_date,
  MAX(order_date) AS last_order_date,
  ROUND(SUM(subtotal_after_discount), 2) AS subtotal_after_discount,
  ROUND(SUM(net_total), 2) AS net_total
FROM order_coupon_rows
WHERE base_coupon_code IS NOT NULL
GROUP BY base_coupon_code
ORDER BY net_total DESC, order_count DESC, base_coupon_code;
