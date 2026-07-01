---
type: "UltraCart Table Definition"
title: "uc_screen_recordings"
description: "Session and page-view trail with URL/referrer parameters, attribution click IDs, UTM recovery, and sparse order linkage."
resource: "urn:ultracart:bigquery:table-definition:uc_screen_recordings"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_screen_recordings"
  - "attribution_sessions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_screen_recordings

Session and page-view trail with URL/referrer parameters, attribution click IDs, UTM recovery, and sparse order linkage.

## Grain

One current session or recording row per screen_recording_uuid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_screen_recordings](/tables/ultracart_dw/uc_screen_recordings.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_screen_recordings](/tables/ultracart_dw_low/uc_screen_recordings.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_screen_recordings](/tables/ultracart_dw_medium/uc_screen_recordings.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_screen_recordings](/tables/ultracart_dw_high/uc_screen_recordings.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `ad_platform` | `STRUCT` |
| `ad_platform.fbc` | `STRING` |
| `ad_platform.fbclid` | `STRING` |
| `ad_platform.fbp` | `STRING` |
| `ad_platform.gacid` | `STRING` |
| `ad_platform.glcid` | `STRING` |
| `ad_platform.msclkid` | `STRING` |
| `ad_platform.ttclid` | `STRING` |
| `communications_campaign_name` | `STRING` |
| `communications_campaign_uuid` | `STRING` |
| `communications_email_subject` | `STRING` |
| `communications_email_uuid` | `STRING` |
| `communications_flow_name` | `STRING` |
| `communications_flow_uuid` | `STRING` |
| `email_domain` | `STRING` |
| `email_hash` | `STRING` |
| `end_timestamp` | `DATETIME` |
| `geolocation` | `STRUCT` |
| `geolocation.lat` | `NUMERIC` |
| `geolocation.lon` | `NUMERIC` |
| `geolocation_country` | `STRING` |
| `geolocation_state` | `STRING` |
| `language_iso_code` | `STRING` |
| `merchant_id` | `STRING` |
| `merchant_notes` | `STRING` |
| `missing_external_tracking` | `BOOLEAN` |
| `order_id` | `STRING` |
| `page_view_count` | `INTEGER` |
| `page_views` | `ARRAY<STRUCT>` |
| `page_views.domain` | `STRING` |
| `page_views.events` | `ARRAY<STRUCT>` |
| `page_views.events.name` | `STRING` |
| `page_views.events.params` | `ARRAY<STRUCT>` |
| `page_views.events.params.name` | `STRING` |
| `page_views.events.params.value_hash` | `STRING` |
| `page_views.events.prior_page_view` | `BOOLEAN` |
| `page_views.events.timestamp` | `DATETIME` |
| `page_views.events.ts` | `INTEGER` |
| `page_views.first_event_timestamp` | `DATETIME` |
| `page_views.http_post` | `BOOLEAN` |
| `page_views.last_event_timestamp` | `DATETIME` |
| `page_views.params` | `ARRAY<STRUCT>` |
| `page_views.params.name` | `STRING` |
| `page_views.params.value` | `STRING` |
| `page_views.referrer` | `STRING` |
| `page_views.referrer_params` | `ARRAY<STRUCT>` |
| `page_views.referrer_params.name` | `STRING` |
| `page_views.referrer_params.value` | `STRING` |
| `page_views.referrer_raw` | `STRING` |
| `page_views.screen_recording_page_view_uuid` | `STRING` |
| `page_views.time_on_page` | `INTEGER` |
| `page_views.timing_dom_content_loaded` | `INTEGER` |
| `page_views.timing_loaded` | `INTEGER` |
| `page_views.url` | `STRING` |
| `partition_date` | `DATE` |
| `preferred_language` | `STRING` |
| `referrer_domain` | `STRING` |
| `screen_recording_uuid` | `STRING` |
| `start_timestamp` | `DATETIME` |
| `storefronts` | `ARRAY<STRUCT>` |
| `storefronts.storefront_host_name` | `STRING` |
| `storefronts.storefront_oid` | `INTEGER` |
| `time_on_site` | `INTEGER` |
| `ucacid` | `STRING` |
| `user_agent` | `STRUCT` |
| `user_agent.device` | `STRUCT` |
| `user_agent.device.name` | `STRING` |
| `user_agent.name` | `STRING` |
| `user_agent.original` | `STRING` |
| `user_agent.os` | `STRUCT` |
| `user_agent.os.full` | `STRING` |
| `user_agent.os.name` | `STRING` |
| `user_agent.os.version` | `STRING` |
| `user_agent.version` | `STRING` |
| `user_agent_raw` | `STRING` |
| `user_ip` | `STRING` |
| `user_properties` | `ARRAY<STRUCT>` |
| `user_properties.name` | `STRING` |
| `user_properties.value` | `STRUCT` |
| `user_properties.value.bd` | `NUMERIC` |
| `user_properties.value.bool` | `BOOLEAN` |
| `user_properties.value.json` | `STRING` |
| `user_properties.value.num` | `INTEGER` |
| `user_properties.value.text` | `STRING` |
| `utm_campaign` | `STRING` |
| `utm_source` | `STRING` |
| `visitor_first_seen` | `DATETIME` |
| `visitor_number` | `INTEGER` |
| `window_height` | `INTEGER` |
| `window_width` | `INTEGER` |
| `email` | `STRING` |
| `page_views.events.params.value` | `STRUCT` |
| `page_views.events.params.value.bd` | `NUMERIC` |
| `page_views.events.params.value.bool` | `BOOLEAN` |
| `page_views.events.params.value.json` | `STRING` |
| `page_views.events.params.value.num` | `INTEGER` |
| `page_views.events.params.value.text` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
