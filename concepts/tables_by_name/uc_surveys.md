---
type: "UltraCart Table Definition"
title: "uc_surveys"
description: "Survey definitions and response structures depending on nested fields."
resource: "urn:ultracart:bigquery:table-definition:uc_surveys"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_surveys"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_surveys

Survey definitions and response structures depending on nested fields.

## Grain

One survey row per survey_uuid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_surveys](/tables/ultracart_dw/uc_surveys.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_surveys](/tables/ultracart_dw_medium/uc_surveys.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_surveys](/tables/ultracart_dw_high/uc_surveys.md) |

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
| `questions.file_answers` | `ARRAY<STRUCT>` |
| `questions.file_answers.file_name` | `STRING` |
| `questions.file_answers.file_uuid` | `STRING` |
| `questions.file_answers.mime_type` | `STRING` |
| `questions.multiple_choice_answers` | `ARRAY<STRUCT>` |
| `questions.multiple_choice_answers.answer` | `STRING` |
| `questions.multiple_choice_answers.answer_hash` | `STRING` |
| `questions.multiple_choice_answers.critical` | `BOOLEAN` |
| `questions.multiple_choice_answers.important` | `BOOLEAN` |
| `questions.single_answer` | `STRUCT` |
| `questions.single_answer.answer` | `STRING` |
| `questions.single_answer.answer_hash` | `STRING` |
| `questions.single_answer.critical` | `BOOLEAN` |
| `questions.single_answer.important` | `BOOLEAN` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
