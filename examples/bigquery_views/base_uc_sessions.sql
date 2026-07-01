-- Grain: one row per screen_recording_uuid.
-- Purpose: session behavior, landing page, and sparse order linkage.
WITH sessions AS (
  SELECT
    screen_recording_uuid,
    merchant_id,
    ucacid,
    start_timestamp,
    DATE(start_timestamp) AS session_date,
    visitor_first_seen,
    visitor_number,
    email_hash AS customer_hash,
    order_id,
    page_view_count,
    time_on_site,
    utm_source,
    utm_campaign,
    geolocation_country,
    geolocation_state,
    page_views
  FROM `{{ source_project }}.{{ access_dataset }}.uc_screen_recordings`
  WHERE partition_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {{ lookback_days }} DAY)
)
SELECT
  screen_recording_uuid,
  merchant_id,
  ucacid,
  start_timestamp,
  session_date,
  customer_hash,
  order_id,
  CASE WHEN visitor_first_seen = start_timestamp THEN 'new' ELSE 'returning' END AS visitor_type,
  page_view_count,
  time_on_site,
  utm_source,
  utm_campaign,
  geolocation_country,
  geolocation_state,
  REGEXP_REPLACE((SELECT pv.domain FROM UNNEST(page_views) AS pv ORDER BY pv.first_event_timestamp LIMIT 1), r'^www\\.', '') AS landing_domain,
  REGEXP_REPLACE(
    REGEXP_EXTRACT((SELECT pv.url FROM UNNEST(page_views) AS pv ORDER BY pv.first_event_timestamp LIMIT 1), r'^https?://[^/]+(/.*)?$'),
    r'/index\\.html$',
    '/'
  ) AS landing_path,
  (SELECT pv.referrer FROM UNNEST(page_views) AS pv ORDER BY pv.first_event_timestamp LIMIT 1) AS landing_referrer
FROM sessions;
