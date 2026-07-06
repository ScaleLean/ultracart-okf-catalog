---
type: "Ontology Action"
action: update_customer_profile
family: customer
object: customer_profile
resource: "urn:ultracart:ontology:action:update_customer_profile"
api:
  method: PUT
  path: /customer/customers/{customer_profile_oid}
  scope: customer_write
  effect: "read-modify-write of the registered customer profile (addresses, terms, tiers, flags)"
  docs: https://www.ultracart.com/api/resource_customer.html
mutates: [customer_profile.*]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# update_customer_profile

Edit a **registered customer profile** (`customer_profile_oid` — the stored
account: login, address books, terms, pricing tiers). This is NOT "the customer"
in the ontology's canonical sense: most buyers have no profile, and the
`customer` definition is an email-grain rollup of orders
(`definitions/customer.md`). This action only touches the profile record.

Read-modify-write like all UltraCart updates: `GET` with `_expand`, edit, `PUT`
the full object. The profile is wide (address books, `cards[]`, B2B permission
flags, loyalty, QuickBooks codes) — the clobber hazard is proportionally larger.

Hard boundaries for a registered implementation:
- **Never write `cards[]`** (stored payment methods) through this action —
  payment-instrument changes are a separate, higher-risk concern; the guard layer
  should strip/reject payloads touching them.
- **Changing `email` re-keys identity**: `email_hash` changes, severing the join
  to order history, auto orders, and marketing contact in the warehouse (see
  `identity/identity_spine.md`). Treat email changes as an owner-approved variant;
  the profile-merge endpoint (`PUT .../merge`) is often the right tool instead.
- Money-adjacent siblings on this family — `store_credit`,
  `adjust_cashback_balance` (both move stored value), `magic_link` (session
  takeover) — are high-tier and NOT covered by this file.
- Tier/terms edits (`pricing_tiers[]`, `terms`, `tax_exempt`,
  `allow_purchase_order`, …) change what the customer pays going forward —
  dry-run must diff them explicitly.

Failure modes: sparse-PUT wiping address books or flags (always round-trip the
expanded object); lost update against back-office edits; oid vs email addressing
(resolve the oid first, pin in audit row); replay must be a no-op when the target
fields already hold the requested values.
