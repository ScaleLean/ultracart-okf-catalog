---
type: "BigQuery View"
title: "ultracart_dw.uc_surveys"
description: "Survey definitions and response structures depending on nested fields."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_surveys"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_surveys"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_surveys

Survey definitions and response structures depending on nested fields.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_surveys`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One survey row per survey_uuid.
- Canonical definition: [uc_surveys](/concepts/tables_by_name/uc_surveys.md)

## Schema Coverage

- Field paths: 29
- Array fields: 2
- Struct fields: 2

## Field Paths

| Field path | Data type |
|---|---|
| `add_coupon_code` | `STRING` |
| `add_item_id` | `STRING` |
| `correct_answer_count` | `INTEGER` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `expiration_dts` | `DATETIME` |
| `incorrect_answer_count` | `INTEGER` |
| `merchant_id` | `STRING` |
| `order_id` | `STRING` |
| `order_item_id` | `STRING` |
| `partition_date` | `DATE` |
| `questions` | `ARRAY<STRUCT>` |
| `questions.correct` | `BOOLEAN` |
| `questions.page_name` | `STRING` |
| `questions.page_number` | `INTEGER` |
| `questions.question` | `STRING` |
| `questions.questionPosition` | `INTEGER` |
| `questions.question_name` | `STRING` |
| `questions.question_type` | `STRING` |
| `questions.visible_choices` | `ARRAY<STRUCT>` |
| `questions.visible_choices.text` | `STRING` |
| `questions.visible_choices.value` | `STRING` |
| `survey_dts` | `DATETIME` |
| `survey_name` | `STRING` |
| `survey_type` | `STRING` |
| `survey_uuid` | `STRING` |
| `ucacid` | `STRING` |
| `uri` | `STRING` |
| `widget_id` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw.uc_surveys`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
