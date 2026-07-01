-- Grain: one row per screen-recording page view.
-- Purpose: page journey and conversion-event analysis.
WITH sessions AS (
  SELECT
    screen_recording_uuid,
    merchant_id,
    ucacid,
    order_id,
    page_views
  FROM `{{ source_project }}.{{ access_dataset }}.uc_screen_recordings`
  WHERE partition_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {{ lookback_days }} DAY)
)
SELECT
  s.screen_recording_uuid,
  s.merchant_id,
  s.ucacid,
  s.order_id,
  ROW_NUMBER() OVER (
    PARTITION BY s.screen_recording_uuid
    ORDER BY pv.first_event_timestamp
  ) AS page_view_number,
  pv.screen_recording_page_view_uuid,
  pv.first_event_timestamp AS page_view_dts,
  pv.domain,
  pv.url,
  REGEXP_EXTRACT(pv.url, r'^https?://[^/]+(/.*)?$') AS path,
  pv.referrer,
  pv.time_on_page,
  EXISTS (
    SELECT 1
    FROM UNNEST(pv.events) AS event
    WHERE LOWER(event.name) IN ('add to cart', 'add_to_cart')
  ) AS has_add_to_cart
FROM sessions AS s
CROSS JOIN UNNEST(s.page_views) AS pv;
