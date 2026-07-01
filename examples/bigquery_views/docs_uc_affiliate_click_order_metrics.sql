-- Source inspiration: UltraCart public Data Warehouse sample query "Affiliate Click -> Order Metrics".
-- Grain: one row per click date, affiliate, landing page, and sub-id.
WITH click_rows AS (
  SELECT
    affiliate_click_oid,
    affiliate_oid,
    DATE(TIMESTAMP(click_dts), "{{ time_zone }}") AS click_date,
    landing_page,
    COALESCE(sub_id, '') AS sub_id
  FROM `{{ source_project }}.{{ access_dataset }}.uc_affiliate_clicks`
  WHERE DATE(TIMESTAMP(click_dts), "{{ time_zone }}")
    >= DATE_SUB(CURRENT_DATE("{{ time_zone }}"), INTERVAL {{ lookback_days }} DAY)
),
ledger_by_click AS (
  SELECT
    affiliate_click_oid,
    order_id,
    SUM(COALESCE(transaction_amount, 0)) AS commission_amount
  FROM `{{ source_project }}.{{ access_dataset }}.uc_affiliate_ledgers`
  WHERE affiliate_click_oid IS NOT NULL
  GROUP BY affiliate_click_oid, order_id
),
order_totals AS (
  SELECT
    order_id,
    COALESCE(summary.total.value, 0) - COALESCE(summary.total_refunded.value, 0) AS net_total
  FROM `{{ source_project }}.{{ access_dataset }}.uc_orders`
  WHERE payment.payment_dts IS NOT NULL
    AND COALESCE(payment.test_order, FALSE) IS FALSE
)
SELECT
  click_rows.click_date,
  click_rows.affiliate_oid,
  click_rows.landing_page,
  click_rows.sub_id,
  COUNT(DISTINCT click_rows.affiliate_click_oid) AS click_count,
  COUNT(DISTINCT ledger_by_click.order_id) AS order_count,
  ROUND(SUM(COALESCE(order_totals.net_total, 0)), 2) AS net_revenue,
  ROUND(SUM(COALESCE(ledger_by_click.commission_amount, 0)), 2) AS commission_amount,
  ROUND(SAFE_DIVIDE(COUNT(DISTINCT ledger_by_click.order_id), COUNT(DISTINCT click_rows.affiliate_click_oid)), 4) AS click_to_order_rate,
  ROUND(SAFE_DIVIDE(SUM(COALESCE(order_totals.net_total, 0)), COUNT(DISTINCT ledger_by_click.order_id)), 2) AS average_order_value
FROM click_rows
LEFT JOIN ledger_by_click
  ON ledger_by_click.affiliate_click_oid = click_rows.affiliate_click_oid
LEFT JOIN order_totals
  ON order_totals.order_id = ledger_by_click.order_id
GROUP BY click_rows.click_date, click_rows.affiliate_oid, click_rows.landing_page, click_rows.sub_id
ORDER BY click_rows.click_date DESC, net_revenue DESC;
