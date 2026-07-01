---
type: "BigQuery View"
title: "ultracart_dw_high.uc_surveys"
description: "Survey definitions and response structures depending on nested fields."
resource: "urn:ultracart:bigquery:object:ultracart_dw_high.uc_surveys"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_high"
  - "uc_surveys"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_high.uc_surveys

Survey definitions and response structures depending on nested fields.

## Definition

- Dataset: [ultracart_dw_high](/datasets/ultracart_dw_high.md)
- Object name: `uc_surveys`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One survey row per survey_uuid.
- Canonical definition: [uc_surveys](/concepts/tables_by_name/uc_surveys.md)

## Schema Coverage

- Field paths: 43
- Array fields: 4
- Struct fields: 5

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
| `questions.file_answers` | `ARRAY<STRUCT>` |
| `questions.file_answers.file_name` | `STRING` |
| `questions.file_answers.file_uuid` | `STRING` |
| `questions.file_answers.mime_type` | `STRING` |
| `questions.multiple_choice_answers` | `ARRAY<STRUCT>` |
| `questions.multiple_choice_answers.answer` | `STRING` |
| `questions.multiple_choice_answers.answer_hash` | `STRING` |
| `questions.multiple_choice_answers.critical` | `BOOLEAN` |
| `questions.multiple_choice_answers.important` | `BOOLEAN` |
| `questions.page_name` | `STRING` |
| `questions.page_number` | `INTEGER` |
| `questions.question` | `STRING` |
| `questions.questionPosition` | `INTEGER` |
| `questions.question_name` | `STRING` |
| `questions.question_type` | `STRING` |
| `questions.single_answer` | `STRUCT` |
| `questions.single_answer.answer` | `STRING` |
| `questions.single_answer.answer_hash` | `STRING` |
| `questions.single_answer.critical` | `BOOLEAN` |
| `questions.single_answer.important` | `BOOLEAN` |
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
FROM `{{ source_project }}.ultracart_dw_high.uc_surveys`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
