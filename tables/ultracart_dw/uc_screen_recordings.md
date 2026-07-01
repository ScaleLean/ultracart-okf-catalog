---
type: "BigQuery View"
title: "ultracart_dw.uc_screen_recordings"
description: "Session and page-view trail with URL/referrer parameters, attribution click IDs, UTM recovery, and sparse order linkage."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_screen_recordings"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_screen_recordings"
  - "attribution_sessions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_screen_recordings

Session and page-view trail with URL/referrer parameters, attribution click IDs, UTM recovery, and sparse order linkage.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_screen_recordings`
- Object type: `VIEW`
- Table family: [attribution_sessions](/references/table_families.md#attribution-sessions)
- Grain: One current session or recording row per screen_recording_uuid.
- Canonical definition: [uc_screen_recordings](/concepts/tables_by_name/uc_screen_recordings.md)

## Schema Coverage

- Field paths: 90
- Array fields: 7
- Struct fields: 13

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw.uc_screen_recordings`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
