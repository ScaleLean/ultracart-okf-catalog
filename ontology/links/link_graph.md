---
type: "Ontology Link Graph"
resource: "urn:ultracart:ontology:links"
generated: true
---

# Link graph (generated — do not hand-edit; `python3 scripts/generate_indexes.py`)

| From | Kind | To | On |
|---|---|---|---|
| affiliate | has_many | affiliate_click | `` |
| affiliate | has_many | affiliate_ledger | `` |
| affiliate | belongs_to | coupon | `` |
| affiliate_click | belongs_to | affiliate | `` |
| affiliate_click | belongs_to | screen_recording | `` |
| affiliate_click | belongs_to | analytics_session | `` |
| affiliate_click | has_many | affiliate_ledger | `` |
| affiliate_ledger | belongs_to | affiliate | `` |
| affiliate_ledger | belongs_to | order | `` |
| affiliate_ledger | belongs_to | item | `` |
| affiliate_ledger | belongs_to | affiliate_click | `` |
| analytics_session | converted_to | order | `` |
| analytics_session | belongs_to | customer | `` |
| analytics_session | belongs_to | customer_profile | `` |
| analytics_session | has_one | screen_recording | `` |
| auto_order | belongs_to | customer | `` |
| auto_order | originated_from | order | `` |
| auto_order | has_many | auto_order_item | `` |
| auto_order_item | belongs_to | auto_order | `` |
| auto_order_item | refers_to | item | `` |
| cart_abandon | belongs_to | customer | `` |
| cart_abandon | belongs_to | customer_profile | `` |
| cart_abandon | references | coupon | `` |
| cart_abandon | references | gift_certificate | `` |
| cart_abandon | belongs_to | storefront | `` |
| conversation | belongs_to | customer | `` |
| coupon | referenced_by | order | `` |
| coupon | belongs_to | affiliate | `` |
| customer_profile | has_many | order | `` |
| customer_profile | referred_by | affiliate | `` |
| customer_profile | has_one | gift_certificate | `` |
| customer_profile | same_person_as | marketing_contact | `` |
| email_list_membership | belongs_to | marketing_contact | `` |
| email_list_membership | belongs_to | customer | `` |
| email_segment_membership | belongs_to | marketing_contact | `` |
| email_segment_membership | belongs_to | customer | `` |
| email_send | belongs_to | marketing_contact | `` |
| email_send | belongs_to | customer | `` |
| email_send | converted_to | order | `` |
| experiment | belongs_to | storefront | `` |
| gift_certificate | belongs_to | customer | `` |
| gift_certificate | belongs_to | customer_profile | `` |
| gift_certificate | originated_from | order | `` |
| inventory_snapshot | belongs_to | item | `` |
| inventory_snapshot | caused_by | order | `` |
| item | has_many | inventory_snapshot | `` |
| item | referenced_by | order_item | `` |
| item | referenced_by | auto_order_item | `` |
| marketing_contact | same_person_as | customer | `` |
| marketing_contact | has_many | email_send | `` |
| marketing_contact | has_many | email_list_membership | `` |
| marketing_contact | has_many | email_segment_membership | `` |
| order | has_many | order_item | `` |
| order | belongs_to | customer_profile | `` |
| order | belongs_to | auto_order | `` |
| order | attributed_to | affiliate | `` |
| order | sold_via | storefront | `` |
| order_item | belongs_to | order | `` |
| order_item | refers_to | item | `` |
| payment_gateway | referenced_by | order | `` |
| pbx_call | belongs_to | support_ticket | `` |
| pbx_call | belongs_to | customer | `` |
| person_enrichment | belongs_to | customer | `` |
| person_enrichment | belongs_to | marketing_contact | `` |
| screen_recording | belongs_to | analytics_session | `` |
| screen_recording | converted_to | order | `` |
| screen_recording | belongs_to | customer | `` |
| screen_recording | attributed_to | email_send | `` |
| screen_recording | belongs_to | storefront | `` |
| storefront | has_many | order | `` |
| storefront | has_many | cart_abandon | `` |
| storefront | has_many | experiment | `` |
| storefront | has_many | screen_recording | `` |
| support_ticket | belongs_to | customer | `` |
| support_ticket | has_many | pbx_call | `` |
| upsell_offer_event | belongs_to | order | `` |
| upsell_offer_event | references | item | `` |
| workflow_task | references | order | `` |
| workflow_task | references | auto_order | `` |
