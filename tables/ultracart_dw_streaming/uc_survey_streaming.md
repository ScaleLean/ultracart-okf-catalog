---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_survey_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_survey_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_survey_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_survey_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_survey_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_survey.
- Canonical definition: [uc_survey_streaming](/concepts/tables_by_name/uc_survey_streaming.md)

## Schema Coverage

- Field paths: 45
- Array fields: 4
- Struct fields: 5

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
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
FROM `{{ source_project }}.ultracart_dw_streaming.uc_survey_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
