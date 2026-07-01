---
type: "BigQuery View"
title: "ultracart_dw_high.uc_storefront_customer_sessions"
description: "Storefront customer session membership data."
resource: "urn:ultracart:bigquery:object:ultracart_dw_high.uc_storefront_customer_sessions"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_high"
  - "uc_storefront_customer_sessions"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_high.uc_storefront_customer_sessions

Storefront customer session membership data.

## Definition

- Dataset: [ultracart_dw_high](/datasets/ultracart_dw_high.md)
- Object name: `uc_storefront_customer_sessions`
- Object type: `VIEW`
- Table family: [customers_support](/references/table_families.md#customers-support)
- Grain: One storefront customer-session row.
- Canonical definition: [uc_storefront_customer_sessions](/concepts/tables_by_name/uc_storefront_customer_sessions.md)

## Schema Coverage

- Field paths: 20
- Array fields: 1
- Struct fields: 1

## Field Paths

| Field path | Data type |
|---|---|
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `end_dts` | `DATETIME` |
| `esp_customer_uuid` | `STRING` |
| `merchant_id` | `STRING` |
| `order_id` | `STRING` |
| `page_views` | `ARRAY<STRUCT>` |
| `page_views.bounce` | `BOOLEAN` |
| `page_views.start_dts` | `DATETIME` |
| `page_views.time_on_page_second` | `NUMERIC` |
| `page_views.url` | `STRING` |
| `partition_date` | `DATE` |
| `screen_recording_uuid` | `STRING` |
| `start_dts` | `DATETIME` |
| `utm_campaign` | `STRING` |
| `utm_content` | `STRING` |
| `utm_id` | `STRING` |
| `utm_medium` | `STRING` |
| `utm_source` | `STRING` |
| `utm_term` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_high.uc_storefront_customer_sessions`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
