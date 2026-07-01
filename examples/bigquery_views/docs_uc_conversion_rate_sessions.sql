-- Source inspiration: UltraCart public Data Warehouse sample query "Conversion Rate from Analytics Sessions".
-- Grain: one row per session date.
WITH session_flags AS (
  SELECT
    client_session_oid,
    DATE(TIMESTAMP(session_dts), "{{ time_zone }}") AS session_date,
    IF(
      EXISTS (
        SELECT 1
        FROM UNNEST(hits) AS hit
        WHERE hit.page_view IS NOT NULL
      ),
      1,
      0
    ) AS has_page_view,
    IF(
      EXISTS (
        SELECT 1
        FROM UNNEST(hits) AS hit
        WHERE hit.checkout_add_items IS NOT NULL
          OR hit.page_view.url LIKE '%/checkout/%'
      ),
      1,
      0
    ) AS add_to_cart,
    IF(
      EXISTS (
        SELECT 1
        FROM UNNEST(hits) AS hit
        WHERE hit.checkout_initiate IS NOT NULL
          OR hit.page_view.url LIKE '%/checkout/%'
      ),
      1,
      0
    ) AS reached_checkout,
    IF(
      EXISTS (
        SELECT 1
        FROM UNNEST(hits) AS hit
        WHERE hit.ecommerce_payment IS NOT NULL
          OR hit.ecommerce_placed_order IS NOT NULL
      ),
      1,
      0
    ) AS placed_order
  FROM `{{ source_project }}.{{ access_dataset }}.uc_analytics_sessions`
  WHERE partition_date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE("{{ time_zone }}"), INTERVAL {{ lookback_days }} DAY), WEEK)
    AND DATE(TIMESTAMP(session_dts), "{{ time_zone }}")
      >= DATE_SUB(CURRENT_DATE("{{ time_zone }}"), INTERVAL {{ lookback_days }} DAY)
)
SELECT
  session_date,
  COUNTIF(has_page_view = 1) AS session_count,
  SUM(add_to_cart) AS add_to_cart_count,
  SUM(reached_checkout) AS reached_checkout_count,
  SUM(placed_order) AS placed_order_count,
  ROUND(SAFE_DIVIDE(SUM(add_to_cart), COUNTIF(has_page_view = 1)), 4) AS add_to_cart_rate,
  ROUND(SAFE_DIVIDE(SUM(reached_checkout), COUNTIF(has_page_view = 1)), 4) AS checkout_rate,
  ROUND(SAFE_DIVIDE(SUM(placed_order), COUNTIF(has_page_view = 1)), 4) AS order_conversion_rate
FROM session_flags
WHERE has_page_view = 1
GROUP BY session_date
ORDER BY session_date DESC;
