---
type: "BigQuery View"
title: "ultracart_dw_low.uc_conversations"
description: "UltraCart conversation metadata and redacted message structure."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_conversations"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_conversations"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_conversations

UltraCart conversation metadata and redacted message structure.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_conversations`
- Object type: `VIEW`
- Table family: [customers_support](/references/table_families.md#customers-support)
- Grain: One conversation row per conversation_uuid.
- Canonical definition: [uc_conversations](/concepts/tables_by_name/uc_conversations.md)

## Schema Coverage

- Field paths: 62
- Array fields: 4
- Struct fields: 5

## Field Paths

| Field path | Data type |
|---|---|
| `base_language_iso_code` | `STRING` |
| `closed` | `BOOLEAN` |
| `conversation_arn` | `STRING` |
| `conversation_uuid` | `STRING` |
| `customer_first_message_unresponded_to_dts` | `DATETIME` |
| `last_conversation_message_body` | `STRING` |
| `last_conversation_message_body_hash` | `STRING` |
| `last_conversation_participant_arn` | `STRING` |
| `last_conversation_participant_name` | `STRING` |
| `last_conversation_participant_name_hash` | `STRING` |
| `last_interactive_message_dts` | `DATETIME` |
| `last_message_dts` | `DATETIME` |
| `medium` | `STRING` |
| `merchant_id` | `STRING` |
| `message_count` | `INTEGER` |
| `messages` | `ARRAY<STRUCT>` |
| `messages.author_conversation_participant_arn` | `STRING` |
| `messages.author_conversation_participant_name_hash` | `STRING` |
| `messages.body_hash` | `STRING` |
| `messages.client_message_id` | `STRING` |
| `messages.conversation_message_uuid` | `STRING` |
| `messages.delay_until_dts` | `DATETIME` |
| `messages.language_iso_code` | `STRING` |
| `messages.merchant_id` | `STRING` |
| `messages.message_dts` | `DATETIME` |
| `messages.message_epoch` | `INTEGER` |
| `messages.message_type` | `STRING` |
| `messages.translations` | `ARRAY<STRUCT>` |
| `messages.translations.language_iso_code` | `STRING` |
| `messages.transport_statuses` | `ARRAY<STRUCT>` |
| `messages.transport_statuses.conversation_participant_arn` | `STRING` |
| `messages.transport_statuses.status` | `STRING` |
| `messages.type` | `STRING` |
| `participants` | `ARRAY<STRUCT>` |
| `participants.conversation_participant_arn` | `STRING` |
| `participants.conversation_participant_name_hash` | `STRING` |
| `participants.conversation_participant_uuid` | `STRING` |
| `participants.email` | `STRING` |
| `participants.email_hash` | `STRING` |
| `participants.joined_dts` | `DATETIME` |
| `participants.language_iso_code` | `STRING` |
| `participants.last_message_dts` | `DATETIME` |
| `participants.left_dts` | `DATETIME` |
| `participants.profile_image_url_hash` | `STRING` |
| `participants.sms_phone_number` | `STRING` |
| `participants.sms_phone_number_hash` | `STRING` |
| `participants.status` | `STRING` |
| `participants.timezone` | `STRING` |
| `participants.unread_messages` | `INTEGER` |
| `partition_date` | `DATE` |
| `sentiment` | `STRUCT` |
| `sentiment.last_detect_sentiment` | `DATETIME` |
| `sentiment.mixed` | `NUMERIC` |
| `sentiment.negative` | `NUMERIC` |
| `sentiment.neutral` | `NUMERIC` |
| `sentiment.positive` | `NUMERIC` |
| `sentiment.sentiment` | `STRING` |
| `start_dts` | `DATETIME` |
| `unread_messages` | `BOOLEAN` |
| `virtual_agent` | `BOOLEAN` |
| `virtual_agent_cost` | `NUMERIC` |
| `visible` | `BOOLEAN` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_low.uc_conversations`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
