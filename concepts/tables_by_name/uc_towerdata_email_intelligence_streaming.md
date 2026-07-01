---
type: "UltraCart Table Definition"
title: "uc_towerdata_email_intelligence_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_towerdata_email_intelligence_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_towerdata_email_intelligence_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_towerdata_email_intelligence_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_towerdata_email_intelligence.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_towerdata_email_intelligence_streaming](/tables/ultracart_dw_streaming/uc_towerdata_email_intelligence_streaming.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
