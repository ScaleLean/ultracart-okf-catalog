---
type: "Ontology Action"
action: global_unsubscribe
family: marketing
object: marketing_contact
resource: "urn:ultracart:ontology:action:global_unsubscribe"
api:
  method: POST
  path: /storefront/{storefront_oid}/email/globalUnsubscribe
  scope: storefront_write
  effect: "globally unsubscribes a person from ALL marketing communication for the merchant (irreversible in practice)"
  docs: https://www.ultracart.com/api/resource_storefront.html
mutates: [marketing_contact.global_unsubscribed, marketing_contact.is_emailable]
risk: high
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (owner-level, per invocation — never-execute surface, see ../README.md)
  - dry_run
status: declared
---

# global_unsubscribe

The consent kill switch: sets `EmailCustomer.global_unsubscribe` — "globally
unsubscribed from all communication" — suppressing the person across **every
list, segment, campaign, and flow** for the merchant. In ontology terms it flips
`marketing_contact.global_unsubscribed` true and `is_emailable` false, removing
the person from `marketing_reachable` permanently.

**This is the irreversible one.** No documented API legitimately restores the
relationship: even where a flag could technically be rewritten (the
`PUT .../email/customers/{uuid}` surface carries unsubscribe flags), re-consent
must come from the *customer* through a fresh opt-in — an agent or merchant
flipping it back is a consent violation, and deliverability providers treat
mail-after-unsubscribe as spam. Model it as one-way.

Because it destroys an asset (a consented relationship) irreversibly, this action
is on the registry's **never-execute list** (`../README.md`): owner-level approval
per invocation, even for merchants that have registered it. The legitimate caller
is a suppression workflow honoring an explicit customer request or a compliance
event (spam complaint, legal demand) — the audit row must record that basis.

Failure modes & quirks:
- **Wrong person** — matching by email string across storefronts: resolve the
  exact contact (per-storefront `esp_customer_uuid` / normalized email) and show
  it in dry-run; there is no undo for a mis-aimed unsubscribe.
- **Under-suppression the other way**: this acts per merchant/storefront scope —
  a person asking "stop all email" who exists under multiple storefronts needs
  the action per scope; verify coverage.
- Transactional email (receipts, shipment notices) is a separate surface and is
  NOT suppressed — set expectations in customer-facing replies.
- SMS has its own path (`PUT /conversation/conversations/{uuid}/sms_unsubscribe`)
  — a full contact-suppression request touches both.
- Replay is naturally idempotent; still audit each invocation.
