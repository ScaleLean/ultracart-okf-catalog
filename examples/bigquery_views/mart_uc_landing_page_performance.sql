-- Grain: one row per session_date, landing_domain, and landing_path.
-- Purpose: landing-page performance from session behavior and order linkage.
WITH sessions AS (
  SELECT
    session_date,
    landing_domain,
    landing_path,
    customer_hash,
    order_id,
    page_view_count,
    time_on_site
  FROM `{{ target_project }}.{{ target_dataset }}.base_uc_sessions`
)
SELECT
  session_date,
  landing_domain,
  landing_path,
  COUNT(*) AS sessions,
  COUNT(DISTINCT customer_hash) AS known_customers,
  COUNTIF(order_id IS NOT NULL) AS sessions_with_order,
  SAFE_DIVIDE(COUNTIF(order_id IS NOT NULL), COUNT(*)) AS session_to_order_rate,
  SUM(page_view_count) AS page_views,
  AVG(page_view_count) AS avg_page_views_per_session,
  AVG(time_on_site) AS avg_time_on_site
FROM sessions
GROUP BY session_date, landing_domain, landing_path;
