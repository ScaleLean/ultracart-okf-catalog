---
type: "Ontology Action"
action: add_contact_to_list
family: marketing
object: email_list_membership
resource: "urn:ultracart:ontology:action:add_contact_to_list"
api:
  method: POST
  path: /storefront/{storefront_oid}/email/lists/{email_list_uuid}/subscribe
  scope: storefront_write
  effect: "subscribes customer(s) to an email list (creates membership rows)"
  docs: https://www.ultracart.com/api/resource_storefront.html
mutates: ["email_list_membership (new row)", marketing_contact.list_count]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# add_contact_to_list

Add a marketing contact to an email **list** (explicit-membership audience;
contrast segments, which are rule-built and cannot be "added to"). The endpoint
accepts a batch of customers — a registered implementation of *this* action must
cap it to a small, named set of contacts; feeding it a large array turns it into a
bulk import, which is a different (high-tier) use governed by the bulk rules in
`../README.md`. A customer-side alternative exists
(`POST /customer/customers/{customer_profile_oid}/email_lists`) for
profile-holders; this action uses the list-side endpoint because most marketing
contacts have no customer profile.

**Membership is targeting, not consent** (see the `marketing_contact` object):
adding someone to a list does NOT make them emailable — `global_unsubscribed`
still suppresses them, and conversely adding a never-consented address to an
active list is a compliance violation the API will happily perform. The guard
layer must require a recorded consent basis (signup source, checkout opt-in,
explicit request) in the audit row.

Failure modes:
- **List-triggered flows**: flows with a list-subscribe trigger fire on this
  action — adding a contact can send email immediately. Dry-run must enumerate
  flows triggered by the target list before the live call.
- Scoping: lists are per-**storefront**; the same person is a different
  `esp_customer_uuid` under another storefront — adding on the wrong
  `storefront_oid` silently targets the wrong audience.
- Replay must not re-fire subscribe side effects (idempotency key on
  list_uuid + contact set); subscribing an existing member should be a no-op.
- Archived lists: subscribing to an archived list is invalid — resolve list state
  first.
