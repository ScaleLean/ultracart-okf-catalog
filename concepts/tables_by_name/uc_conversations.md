---
type: "UltraCart Table Definition"
title: "uc_conversations"
description: "UltraCart conversation metadata and redacted message structure."
resource: "urn:ultracart:bigquery:table-definition:uc_conversations"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_conversations"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_conversations

UltraCart conversation metadata and redacted message structure.

## Grain

One conversation row per conversation_uuid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_conversations](/tables/ultracart_dw/uc_conversations.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_conversations](/tables/ultracart_dw_low/uc_conversations.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_conversations](/tables/ultracart_dw_medium/uc_conversations.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_conversations](/tables/ultracart_dw_high/uc_conversations.md) |

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
| `messages.author_conversation_participant_name` | `STRING` |
| `messages.body` | `STRING` |
| `messages.media_urls` | `ARRAY<STRUCT>` |
| `messages.media_urls.value` | `STRING` |
| `messages.translations.body` | `STRING` |
| `participants.conversation_participant_name` | `STRING` |
| `participants.profile_image_url` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
