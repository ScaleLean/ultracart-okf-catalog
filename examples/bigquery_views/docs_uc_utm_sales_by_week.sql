-- Source inspiration: UltraCart public Data Warehouse sample query "UTM Sales By Week".
-- Grain: one row per order week and UTM source/campaign.
WITH order_rows AS (
  SELECT
    DATE_TRUNC(DATE(TIMESTAMP(order_header.creation_dts), "{{ time_zone }}"), WEEK) AS order_week,
    COALESCE((
      SELECT property.value
      FROM UNNEST(order_header.properties) AS property
      WHERE property.name = 'ucasource'
      LIMIT 1
    ), order_header.utms[SAFE_OFFSET(0)].utm_source, '(none)') AS utm_source,
    COALESCE((
      SELECT property.value
      FROM UNNEST(order_header.properties) AS property
      WHERE property.name = 'ucacampaign'
      LIMIT 1
    ), order_header.utms[SAFE_OFFSET(0)].utm_campaign, '(none)') AS utm_campaign,
    order_header.order_id,
    COALESCE(order_header.summary.subtotal.value, 0)
      - COALESCE(order_header.summary.subtotal_discount.value, 0) AS subtotal_after_discount,
    COALESCE(order_header.summary.total.value, 0)
      - COALESCE(order_header.summary.total_refunded.value, 0) AS net_total
  FROM `{{ source_project }}.{{ access_dataset }}.uc_orders` AS order_header
  WHERE DATE(TIMESTAMP(order_header.creation_dts), "{{ time_zone }}")
      >= DATE_SUB(CURRENT_DATE("{{ time_zone }}"), INTERVAL {{ lookback_days }} DAY)
    AND order_header.payment.payment_status = 'Processed'
    AND COALESCE(order_header.payment.test_order, FALSE) IS FALSE
)
SELECT
  order_week,
  utm_source,
  utm_campaign,
  COUNT(DISTINCT order_id) AS order_count,
  ROUND(SUM(subtotal_after_discount), 2) AS subtotal_after_discount,
  ROUND(SUM(net_total), 2) AS net_total,
  ROUND(SAFE_DIVIDE(SUM(net_total), COUNT(DISTINCT order_id)), 2) AS average_order_value
FROM order_rows
GROUP BY order_week, utm_source, utm_campaign
ORDER BY order_week DESC, net_total DESC;
