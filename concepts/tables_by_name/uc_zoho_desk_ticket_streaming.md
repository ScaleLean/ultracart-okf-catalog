---
type: "UltraCart Table Definition"
title: "uc_zoho_desk_ticket_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_zoho_desk_ticket_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_zoho_desk_ticket_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_zoho_desk_ticket_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_zoho_desk_ticket.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_zoho_desk_ticket_streaming](/tables/ultracart_dw_streaming/uc_zoho_desk_ticket_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `account_id` | `STRING` |
| `approval_count` | `STRING` |
| `assignee` | `STRUCT` |
| `assignee.email` | `STRING` |
| `assignee.email_hash` | `STRING` |
| `assignee.first_name` | `STRING` |
| `assignee.first_name_hash` | `STRING` |
| `assignee.id` | `STRING` |
| `assignee.last_name` | `STRING` |
| `assignee.last_name_hash` | `STRING` |
| `assignee.name` | `STRING` |
| `assignee.name_hash` | `STRING` |
| `assignee.photo_url` | `STRING` |
| `assignee.role_name` | `STRING` |
| `assignee_id` | `STRING` |
| `attachment_count` | `STRING` |
| `attachments` | `ARRAY<STRUCT>` |
| `attachments.content_type` | `STRING` |
| `attachments.creator_id` | `STRING` |
| `attachments.file_id` | `STRING` |
| `attachments.file_name` | `STRING` |
| `attachments.file_name_hash` | `STRING` |
| `attachments.file_url` | `STRING` |
| `attachments.id` | `STRING` |
| `attachments.is_public` | `BOOLEAN` |
| `attachments.size` | `INTEGER` |
| `attachments.uploaded_time` | `STRING` |
| `attachments.view_url` | `STRING` |
| `category` | `STRING` |
| `cf` | `ARRAY<STRUCT>` |
| `cf.key` | `STRING` |
| `cf.value` | `STRING` |
| `channel` | `STRING` |
| `channel_code` | `STRING` |
| `channel_related_info` | `ARRAY<STRUCT>` |
| `channel_related_info.key` | `STRING` |
| `channel_related_info.value` | `STRING` |
| `classification` | `STRING` |
| `closed_time` | `DATETIME` |
| `comment_count` | `STRING` |
| `comments` | `ARRAY<STRUCT>` |
| `comments.attachments` | `ARRAY<STRUCT>` |
| `comments.attachments.content_type` | `STRING` |
| `comments.attachments.creator_id` | `STRING` |
| `comments.attachments.file_id` | `STRING` |
| `comments.attachments.file_name` | `STRING` |
| `comments.attachments.file_name_hash` | `STRING` |
| `comments.attachments.file_url` | `STRING` |
| `comments.attachments.id` | `STRING` |
| `comments.attachments.is_public` | `BOOLEAN` |
| `comments.attachments.size` | `INTEGER` |
| `comments.attachments.uploaded_time` | `STRING` |
| `comments.attachments.view_url` | `STRING` |
| `comments.author_id` | `STRING` |
| `comments.author_type` | `STRING` |
| `comments.commented_time` | `STRING` |
| `comments.commenter` | `STRUCT` |
| `comments.commenter.email` | `STRING` |
| `comments.commenter.email_hash` | `STRING` |
| `comments.commenter.first_name` | `STRING` |
| `comments.commenter.first_name_hash` | `STRING` |
| `comments.commenter.id` | `STRING` |
| `comments.commenter.last_name` | `STRING` |
| `comments.commenter.last_name_hash` | `STRING` |
| `comments.commenter.name` | `STRING` |
| `comments.commenter.name_hash` | `STRING` |
| `comments.commenter.photo_url` | `STRING` |
| `comments.commenter.role_name` | `STRING` |
| `comments.commenter.type` | `STRING` |
| `comments.content` | `STRING` |
| `comments.content_hash` | `STRING` |
| `comments.content_type` | `STRING` |
| `comments.id` | `STRING` |
| `comments.is_public` | `BOOLEAN` |
| `comments.mentions` | `ARRAY<STRUCT>` |
| `comments.mentions.id` | `STRING` |
| `comments.mentions.name` | `STRING` |
| `comments.mentions.photo_url` | `STRING` |
| `comments.mentions.type` | `STRING` |
| `comments.modified_time` | `STRING` |
| `comments.ticket_id` | `STRING` |
| `contact` | `STRUCT` |
| `contact.account` | `ARRAY<STRUCT>` |
| `contact.account.key` | `STRING` |
| `contact.account.value` | `STRING` |
| `contact.company_name` | `STRING` |
| `contact.email` | `STRING` |
| `contact.email_hash` | `STRING` |
| `contact.first_name` | `STRING` |
| `contact.first_name_hash` | `STRING` |
| `contact.id` | `STRING` |
| `contact.is_spam` | `BOOLEAN` |
| `contact.last_name` | `STRING` |
| `contact.last_name_hash` | `STRING` |
| `contact.mobile` | `STRING` |
| `contact.mobile_hash` | `STRING` |
| `contact.name` | `STRING` |
| `contact.name_hash` | `STRING` |
| `contact.phone` | `STRING` |
| `contact.phone_hash` | `STRING` |
| `contact.photo_url` | `STRING` |
| `contact.type` | `STRING` |
| `contact_id` | `STRING` |
| `contract_id` | `STRING` |
| `created_by` | `STRING` |
| `created_time` | `DATETIME` |
| `custom_fields` | `ARRAY<STRUCT>` |
| `custom_fields.key` | `STRING` |
| `custom_fields.value` | `STRING` |
| `customer_response_time` | `DATETIME` |
| `department` | `STRUCT` |
| `department.id` | `STRING` |
| `department.name` | `STRING` |
| `department_id` | `STRING` |
| `description` | `STRING` |
| `description_hash` | `STRING` |
| `due_date` | `DATETIME` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `entity_skills` | `ARRAY<STRUCT>` |
| `entity_skills.value` | `STRING` |
| `follower_count` | `STRING` |
| `id` | `STRING` |
| `is_archived` | `BOOLEAN` |
| `is_deleted` | `BOOLEAN` |
| `is_escalated` | `BOOLEAN` |
| `is_following` | `BOOLEAN` |
| `is_over_due` | `BOOLEAN` |
| `is_public` | `BOOLEAN` |
| `is_read` | `BOOLEAN` |
| `is_response_overdue` | `BOOLEAN` |
| `is_spam` | `BOOLEAN` |
| `is_trashed` | `BOOLEAN` |
| `language` | `STRING` |
| `layout_details` | `STRUCT` |
| `layout_details.id` | `STRING` |
| `layout_details.layout_name` | `STRING` |
| `layout_id` | `STRING` |
| `merchant_id` | `STRING` |
| `modified_by` | `STRING` |
| `modified_time` | `DATETIME` |
| `onhold_time` | `DATETIME` |
| `partition_date` | `DATE` |
| `phone` | `STRING` |
| `phone_hash` | `STRING` |
| `portal_url` | `STRING` |
| `priority` | `STRING` |
| `product` | `STRUCT` |
| `product.id` | `STRING` |
| `product.name` | `STRING` |
| `product_id` | `STRING` |
| `resolution` | `STRING` |
| `resolution_hash` | `STRING` |
| `response_due_date` | `DATETIME` |
| `secondary_contacts` | `ARRAY<STRUCT>` |
| `secondary_contacts.account` | `ARRAY<STRUCT>` |
| `secondary_contacts.account.key` | `STRING` |
| `secondary_contacts.account.value` | `STRING` |
| `secondary_contacts.company_name` | `STRING` |
| `secondary_contacts.email` | `STRING` |
| `secondary_contacts.email_hash` | `STRING` |
| `secondary_contacts.first_name` | `STRING` |
| `secondary_contacts.first_name_hash` | `STRING` |
| `secondary_contacts.id` | `STRING` |
| `secondary_contacts.is_spam` | `BOOLEAN` |
| `secondary_contacts.last_name` | `STRING` |
| `secondary_contacts.last_name_hash` | `STRING` |
| `secondary_contacts.mobile` | `STRING` |
| `secondary_contacts.mobile_hash` | `STRING` |
| `secondary_contacts.name` | `STRING` |
| `secondary_contacts.name_hash` | `STRING` |
| `secondary_contacts.phone` | `STRING` |
| `secondary_contacts.phone_hash` | `STRING` |
| `secondary_contacts.photo_url` | `STRING` |
| `secondary_contacts.type` | `STRING` |
| `sentiment` | `STRING` |
| `shared_departments` | `ARRAY<STRUCT>` |
| `shared_departments.id` | `STRING` |
| `shared_departments.name` | `STRING` |
| `skills_info` | `ARRAY<STRUCT>` |
| `skills_info.id` | `STRING` |
| `skills_info.name` | `STRING` |
| `sla_id` | `STRING` |
| `source` | `STRUCT` |
| `source.app_name` | `STRING` |
| `source.app_photo_url` | `STRING` |
| `source.ext_id` | `STRING` |
| `source.permalink` | `STRING` |
| `source.type` | `STRING` |
| `source.uuid` | `STRING` |
| `status` | `STRING` |
| `status_type` | `STRING` |
| `sub_category` | `STRING` |
| `subject` | `STRING` |
| `subject_hash` | `STRING` |
| `tag_count` | `STRING` |
| `task_count` | `STRING` |
| `team` | `STRUCT` |
| `team.id` | `STRING` |
| `team.logo_url` | `STRING` |
| `team.name` | `STRING` |
| `team_id` | `STRING` |
| `thread_count` | `STRING` |
| `threads` | `ARRAY<STRUCT>` |
| `threads.attachments` | `ARRAY<STRUCT>` |
| `threads.attachments.content_type` | `STRING` |
| `threads.attachments.creator_id` | `STRING` |
| `threads.attachments.file_id` | `STRING` |
| `threads.attachments.file_name` | `STRING` |
| `threads.attachments.file_name_hash` | `STRING` |
| `threads.attachments.file_url` | `STRING` |
| `threads.attachments.id` | `STRING` |
| `threads.attachments.is_public` | `BOOLEAN` |
| `threads.attachments.size` | `INTEGER` |
| `threads.attachments.uploaded_time` | `STRING` |
| `threads.attachments.view_url` | `STRING` |
| `threads.bcc_email_addresses` | `ARRAY<STRUCT>` |
| `threads.bcc_email_addresses.value` | `STRING` |
| `threads.bcc_email_addresses_hash` | `STRING` |
| `threads.cc_email_addresses` | `ARRAY<STRUCT>` |
| `threads.cc_email_addresses.value` | `STRING` |
| `threads.cc_email_addresses_hash` | `STRING` |
| `threads.content` | `STRING` |
| `threads.content_hash` | `STRING` |
| `threads.content_type` | `STRING` |
| `threads.direction` | `STRING` |
| `threads.from_email_address` | `STRING` |
| `threads.from_email_address_hash` | `STRING` |
| `threads.hashtags` | `ARRAY<STRUCT>` |
| `threads.hashtags.value` | `STRING` |
| `threads.id` | `STRING` |
| `threads.is_public` | `BOOLEAN` |
| `threads.mentions` | `ARRAY<STRUCT>` |
| `threads.mentions.value` | `STRING` |
| `threads.sent_time` | `STRING` |
| `threads.ticket_id` | `STRING` |
| `threads.to_email_addresses` | `ARRAY<STRUCT>` |
| `threads.to_email_addresses.value` | `STRING` |
| `threads.to_email_addresses_hash` | `STRING` |
| `ticket_number` | `STRING` |
| `time_entry_count` | `STRING` |
| `web_url` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
