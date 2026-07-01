---
type: "BigQuery View"
title: "ultracart_dw_medium.uc_storefront_customer_emails"
description: "Storefront email membership and status data."
resource: "urn:ultracart:bigquery:object:ultracart_dw_medium.uc_storefront_customer_emails"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_medium"
  - "uc_storefront_customer_emails"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_medium.uc_storefront_customer_emails

Storefront email membership and status data.

## Definition

- Dataset: [ultracart_dw_medium](/datasets/ultracart_dw_medium.md)
- Object name: `uc_storefront_customer_emails`
- Object type: `VIEW`
- Table family: [customers_support](/references/table_families.md#customers-support)
- Grain: One storefront email membership row.
- Canonical definition: [uc_storefront_customer_emails](/concepts/tables_by_name/uc_storefront_customer_emails.md)

## Schema Coverage

- Field paths: 20
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `campaign_name` | `STRING` |
| `clicked` | `BOOLEAN` |
| `clicked_dts` | `DATETIME` |
| `commseq_uuid` | `STRING` |
| `converted` | `BOOLEAN` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `email_uuid` | `STRING` |
| `esp_customer_uuid` | `STRING` |
| `flow_name` | `STRING` |
| `merchant_id` | `STRING` |
| `opened` | `BOOLEAN` |
| `opened_dts` | `DATETIME` |
| `order_id` | `STRING` |
| `partition_date` | `DATE` |
| `sent_dts` | `DATETIME` |
| `spam_complaint` | `BOOLEAN` |
| `spam_complaint_dts` | `DATETIME` |
| `subject` | `STRING` |
| `transport` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_medium.uc_storefront_customer_emails`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
