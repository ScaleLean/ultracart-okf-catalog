---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_towerdata_email_intelligence_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_towerdata_email_intelligence_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_towerdata_email_intelligence_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_towerdata_email_intelligence_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_towerdata_email_intelligence_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_towerdata_email_intelligence.
- Canonical definition: [uc_towerdata_email_intelligence_streaming](/concepts/tables_by_name/uc_towerdata_email_intelligence_streaming.md)

## Schema Coverage

- Field paths: 55
- Array fields: 0
- Struct fields: 5

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `aci` | `STRUCT` |
| `aci.big_spender` | `STRUCT` |
| `aci.big_spender.value` | `STRING` |
| `aci.deal_seeker` | `STRUCT` |
| `aci.deal_seeker.value` | `STRING` |
| `age` | `STRING` |
| `eam` | `STRUCT` |
| `eam.dateFirstSeen` | `STRING` |
| `eam.longevity` | `INTEGER` |
| `eam.month_last_open` | `STRING` |
| `eam.popularity` | `INTEGER` |
| `eam.velocity` | `INTEGER` |
| `education` | `STRING` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `financial_group` | `STRING` |
| `financial_segment` | `STRING` |
| `gender` | `STRING` |
| `home_owner_status` | `STRING` |
| `household_income` | `STRING` |
| `interests` | `STRUCT` |
| `interests.arts_and_crafts` | `STRING` |
| `interests.automotive` | `STRING` |
| `interests.baby_product_buyer` | `STRING` |
| `interests.beauty` | `STRING` |
| `interests.blogging` | `STRING` |
| `interests.books` | `STRING` |
| `interests.business` | `STRING` |
| `interests.charitable_donors` | `STRING` |
| `interests.cooking` | `STRING` |
| `interests.discount_shopper` | `STRING` |
| `interests.health_and_wellness` | `STRING` |
| `interests.high_end_brand_buyer` | `STRING` |
| `interests.home_and_garden` | `STRING` |
| `interests.home_improvement` | `STRING` |
| `interests.luxury_goods` | `STRING` |
| `interests.magazine_buyer` | `STRING` |
| `interests.news_and_current_events` | `STRING` |
| `interests.outdoor_and_adventure` | `STRING` |
| `interests.pets` | `STRING` |
| `interests.sports` | `STRING` |
| `interests.technology` | `STRING` |
| `interests.travel` | `STRING` |
| `length_of_residence` | `STRING` |
| `life_stage_group` | `STRING` |
| `life_stage_segment` | `STRING` |
| `marital_status` | `STRING` |
| `net_worth` | `STRING` |
| `occupation` | `STRING` |
| `partition_oid` | `INTEGER` |
| `presence_of_children` | `STRING` |
| `rfm_avg_dollars` | `STRING` |
| `rfm_online_avg_days` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_towerdata_email_intelligence_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
