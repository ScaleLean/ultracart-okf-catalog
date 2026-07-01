---
type: "UltraCart Table Definition"
title: "uc_conversation_pbx_calls"
description: "PBX call metadata for support and operations."
resource: "urn:ultracart:bigquery:table-definition:uc_conversation_pbx_calls"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_conversation_pbx_calls"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_conversation_pbx_calls

PBX call metadata for support and operations.

## Grain

One call row per call_uuid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_conversation_pbx_calls](/tables/ultracart_dw/uc_conversation_pbx_calls.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_conversation_pbx_calls](/tables/ultracart_dw_low/uc_conversation_pbx_calls.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_conversation_pbx_calls](/tables/ultracart_dw_medium/uc_conversation_pbx_calls.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_conversation_pbx_calls](/tables/ultracart_dw_high/uc_conversation_pbx_calls.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `account_sid` | `STRING` |
| `agents` | `ARRAY<STRUCT>` |
| `agents.agent_extension` | `STRING` |
| `agents.agent_id` | `STRING` |
| `agents.agent_name` | `STRING` |
| `agents.agent_user_id` | `STRING` |
| `agents.answered` | `BOOLEAN` |
| `agents.call_sid` | `STRING` |
| `agents.joined_at_dts` | `DATETIME` |
| `agents.left_at_dts` | `DATETIME` |
| `agents.role` | `STRING` |
| `agents.worker_sid` | `STRING` |
| `ai_agent_engagements` | `ARRAY<STRUCT>` |
| `ai_agent_engagements.agent_name` | `STRING` |
| `ai_agent_engagements.agent_uuid` | `STRING` |
| `ai_agent_engagements.cost` | `STRUCT` |
| `ai_agent_engagements.cost.amount` | `NUMERIC` |
| `ai_agent_engagements.cost.billed_minutes` | `NUMERIC` |
| `ai_agent_engagements.cost.cost_per_minute` | `NUMERIC` |
| `ai_agent_engagements.cost.currency` | `STRING` |
| `ai_agent_engagements.ended_at_dts` | `DATETIME` |
| `ai_agent_engagements.engagement_type` | `STRING` |
| `ai_agent_engagements.session_uuid` | `STRING` |
| `ai_agent_engagements.started_at_dts` | `DATETIME` |
| `ai_agent_engagements.status` | `STRING` |
| `ai_agent_engagements.tool_calls` | `ARRAY<STRUCT>` |
| `ai_agent_engagements.tool_calls.called_at_dts` | `DATETIME` |
| `ai_agent_engagements.tool_calls.completed_at_dts` | `DATETIME` |
| `ai_agent_engagements.tool_calls.duration_ms` | `INTEGER` |
| `ai_agent_engagements.tool_calls.error_message` | `STRING` |
| `ai_agent_engagements.tool_calls.success` | `BOOLEAN` |
| `ai_agent_engagements.tool_calls.tool_call_uuid` | `STRING` |
| `ai_agent_engagements.tool_calls.tool_name` | `STRING` |
| `ai_agent_engagements.whispers` | `ARRAY<STRUCT>` |
| `ai_agent_engagements.whispers.message` | `STRING` |
| `ai_agent_engagements.whispers.priority` | `STRING` |
| `ai_agent_engagements.whispers.whisper_uuid` | `STRING` |
| `ai_agent_engagements.whispers.whispered_at_dts` | `DATETIME` |
| `ai_summary` | `STRUCT` |
| `ai_summary.action_items` | `ARRAY<STRUCT>` |
| `ai_summary.action_items.value` | `STRING` |
| `ai_summary.call_category` | `STRING` |
| `ai_summary.completion_tokens` | `INTEGER` |
| `ai_summary.cost` | `NUMERIC` |
| `ai_summary.cost_currency` | `STRING` |
| `ai_summary.generated_at_dts` | `DATETIME` |
| `ai_summary.key_topics` | `ARRAY<STRUCT>` |
| `ai_summary.key_topics.value` | `STRING` |
| `ai_summary.model` | `STRING` |
| `ai_summary.prompt_tokens` | `INTEGER` |
| `ai_summary.sentiment` | `STRING` |
| `ai_summary.summary` | `STRING` |
| `call_sid` | `STRING` |
| `call_uuid` | `STRING` |
| `caller` | `STRUCT` |
| `caller.caller_id_hash` | `STRING` |
| `caller.city` | `STRING` |
| `caller.country` | `STRING` |
| `caller.phone_number_hash` | `STRING` |
| `caller.state` | `STRING` |
| `conference_sid` | `STRING` |
| `context_merchant_id` | `STRING` |
| `created_at_dts` | `DATETIME` |
| `customer_name_hash` | `STRING` |
| `customer_profile_oid` | `STRING` |
| `disposition` | `STRING` |
| `email_hash` | `STRING` |
| `financial` | `STRUCT` |
| `financial.ai_agent_billed_minutes` | `NUMERIC` |
| `financial.ai_agent_cost` | `NUMERIC` |
| `financial.ai_agent_cost_currency` | `STRING` |
| `financial.ai_summary_cost` | `NUMERIC` |
| `financial.call_currency` | `STRING` |
| `financial.call_price` | `NUMERIC` |
| `financial.call_price_estimated` | `BOOLEAN` |
| `financial.transcription_cost` | `NUMERIC` |
| `holds` | `ARRAY<STRUCT>` |
| `holds.held_by_agent_id` | `STRING` |
| `holds.hold_duration_seconds` | `INTEGER` |
| `holds.hold_end_dts` | `DATETIME` |
| `holds.hold_start_dts` | `DATETIME` |
| `merchant_id` | `STRING` |
| `notes` | `STRING` |
| `notes_finalized_dts` | `DATETIME` |
| `partition_date` | `DATE` |
| `recording_sids` | `ARRAY<STRUCT>` |
| `recording_sids.value` | `STRING` |
| `recordings` | `ARRAY<STRUCT>` |
| `recordings.channels` | `INTEGER` |
| `recordings.duration_seconds` | `INTEGER` |
| `recordings.is_primary` | `BOOLEAN` |
| `recordings.recording_s3_key` | `STRING` |
| `recordings.recording_sid` | `STRING` |
| `recordings.recording_url` | `STRING` |
| `recordings.status` | `STRING` |
| `recordings.transcript` | `STRUCT` |
| `recordings.transcript.full_transcript_s3_key` | `STRING` |
| `recordings.transcript.job_name` | `STRING` |
| `recordings.transcript.language_code` | `STRING` |
| `recordings.transcript.provider` | `STRING` |
| `recordings.transcript.segments` | `ARRAY<STRUCT>` |
| `recordings.transcript.segments.agent_id` | `STRING` |
| `recordings.transcript.segments.channel` | `STRING` |
| `recordings.transcript.segments.confidence` | `NUMERIC` |
| `recordings.transcript.segments.end_time` | `NUMERIC` |
| `recordings.transcript.segments.speaker` | `STRING` |
| `recordings.transcript.segments.start_time` | `NUMERIC` |
| `recordings.transcript.segments.text_hash` | `STRING` |
| `recordings.transcript.status` | `STRING` |
| `recordings.transcript.transcript_json_s3_key` | `STRING` |
| `routing` | `STRUCT` |
| `routing.call_type` | `STRING` |
| `routing.direction` | `STRING` |
| `routing.queue` | `STRUCT` |
| `routing.queue.answered_at_dts` | `DATETIME` |
| `routing.queue.entered_at_dts` | `DATETIME` |
| `routing.queue.queue_name` | `STRING` |
| `routing.queue.queue_uuid` | `STRING` |
| `routing.queue.result` | `STRING` |
| `routing.queue.wait_seconds` | `INTEGER` |
| `status` | `STRING` |
| `timeline` | `STRUCT` |
| `timeline.answer_dts` | `DATETIME` |
| `timeline.created_dts` | `DATETIME` |
| `timeline.end_dts` | `DATETIME` |
| `timeline.queue_wait_seconds` | `INTEGER` |
| `timeline.talk_time_seconds` | `INTEGER` |
| `timeline.total_duration_seconds` | `INTEGER` |
| `transfers` | `ARRAY<STRUCT>` |
| `transfers.transfer_reason` | `STRING` |
| `transfers.transfer_type` | `STRING` |
| `transfers.transferred_at_dts` | `DATETIME` |
| `transfers.transferred_by_agent_id` | `STRING` |
| `transfers.transferred_to_hash` | `STRING` |
| `updated_at_dts` | `DATETIME` |
| `zoho_desk_ticket_id` | `STRING` |
| `zoho_desk_ticket_url` | `STRING` |
| `caller.caller_id` | `STRING` |
| `caller.phone_number` | `STRING` |
| `customer_name` | `STRING` |
| `email` | `STRING` |
| `recordings.transcript.segments.text` | `STRING` |
| `transfers.transferred_to` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
