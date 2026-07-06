---
type: "Ontology Action"
action: resend_receipt
family: order
object: order
resource: "urn:ultracart:ontology:action:resend_receipt"
api:
  method: POST
  path: /order/orders/{order_id}/resend_receipt
  scope: order_write
  effect: "re-sends the order receipt email to the order's billing email"
  docs: https://www.ultracart.com/api/resource_order.html
mutates: []
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# resend_receipt

Re-deliver the transactional receipt email for an existing order. Verified in the
mining catalog (§7 order family), alongside the sibling
`POST .../resend_shipment_confirmation` (not separately declared; same contract,
different document).

This is the registry's **transactional carve-out**: it is outbound contact, but a
single-recipient re-send of a document the customer already owns, so it tiers
**medium**, not high (see `../README.md`). It mutates no ontology state
(`mutates: []`) — the governance value is the audit trail and rate discipline.

Semantics & failure modes:
- Recipient is the **order's billing email** — it cannot re-route a receipt to an
  arbitrary address. For "send my receipt to my work email" requests, the order's
  email must be updated first (a different, riskier action) — do not chain that
  automatically.
- Transactional emails are a separate surface from marketing commseqs (mining §5);
  this send bypasses marketing consent — `global_unsubscribed` contacts still
  receive receipts. That is correct behavior, but agents must not use it as a
  side-channel to contact unsubscribed customers.
- Repeat-send abuse: the rate-limit docs flag rapid repeated content operations;
  the idempotency key should collapse duplicate user requests within a window
  (e.g. same order, same hour).
- Fails on orders with no billing email (some channel-partner imports) — surface
  the API error rather than retrying.
