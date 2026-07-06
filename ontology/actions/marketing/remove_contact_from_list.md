---
type: "Ontology Action"
action: remove_contact_from_list
family: marketing
object: email_list_membership
resource: "urn:ultracart:ontology:action:remove_contact_from_list"
api:
  method: DELETE
  path: /storefront/{storefront_oid}/email/lists/{email_list_uuid}/customers/{email_customer_uuid}
  scope: storefront_write
  effect: "removes one contact's membership from one email list"
  docs: https://www.ultracart.com/api/resource_storefront.html
mutates: ["email_list_membership (row removed)", marketing_contact.list_count]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# remove_contact_from_list

Remove one contact (`email_customer_uuid` = the ontology's `esp_customer_uuid`)
from one list. Naturally single-record and idempotent — the safest action in the
marketing family, and the correct response to "stop sending me the newsletter"
when the request is list-specific.

**This is NOT an unsubscribe.** Leaving a list does not flip
`marketing_contact.global_unsubscribed`; the contact remains reachable via other
lists, segments (rule-built — they re-include people regardless of list edits),
and flow enrollments already in progress. For "never email me again," the correct
action is `global_unsubscribe.md` (high-tier). Registered implementations should
ask which intent applies rather than guessing downward — under-suppressing a
genuine unsubscribe request is a compliance failure, not a courtesy.

Failure modes:
- **Segment re-inclusion** — a contact removed from a list can still be targeted
  by any segment whose `filter_profile_equation_json` matches them; dry-run should
  note overlapping segments when determinable.
- **In-flight commseq enrollments** are not terminated by list removal; customers
  mid-flow keep receiving that flow's steps (flow exit conditions govern that).
- Wrong-storefront scoping: `esp_customer_uuid` is per storefront — resolve the
  uuid under the same `storefront_oid` as the list.
- Replay/404: deleting an already-removed membership should be treated as no-op
  success by the implementation.
