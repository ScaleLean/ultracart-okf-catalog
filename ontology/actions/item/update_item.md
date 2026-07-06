---
type: "Ontology Action"
action: update_item
family: item
object: item
resource: "urn:ultracart:ontology:action:update_item"
api:
  method: PUT
  path: /item/items/{merchant_item_oid}
  scope: item_write
  effect: "read-modify-write of one catalog item (pricing, content, shipping, subscription config)"
  docs: https://www.ultracart.com/api/resource_item.html
mutates: [item.*]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# update_item

Edit one catalog item, addressed by immutable `merchant_item_oid` (the human SKU
`merchant_item_id` is **mutable** — the API auto-resolves oid from the id, but the
audit row must pin the oid, since the id can be changed by this very action).
Read-modify-write: `GET` with `_expand`, edit, `PUT` the whole object.

The item object is the deepest in the API (pricing, pricing tiers, kit
definitions, variations/options, per-DC inventory & cogs, digital delivery,
auto-order subscription config, related/restriction rules, marketplace mappings).
Consequences ripple:

- **Pricing edits are live immediately** at checkout and — via
  `ItemAutoOrder` interplay — can affect future *rebill* pricing for existing
  subscribers (unless their auto-order items carry `arbitrary_unit_cost`
  overrides). Dry-run must diff `pricing.*` and flag items that are
  `auto_orderable` or referenced by active auto orders.
- **Subscription config** (`auto_order.steps[]`, allowed schedules, cancellation
  guards) governs live subscriber behavior — treat edits there as
  subscription-family changes in disguise.
- **Kit integrity**: editing `kit_definition` / components changes what physically
  ships; `kit_component_only` items must remain consistent with their parents.
- **Variations**: parent/child variant items are separate real items — editing a
  parent does not cascade.

Scope boundary: `PUT /item/items/batch` (multi-item), `DELETE` (destructive), and
gated-code/review/digital-library sub-resources are separate catalog entries
(`../catalog.md`); batch update and delete sit a tier higher.

Failure modes: sparse-PUT clobber of nested config (the classic here is wiping
`shipping.distribution_centers[]` inventory or `pricing_tiers[]` by omitting
them); lost update vs back-office merchandisers; renaming `merchant_item_id`
breaks external references (feeds, campaigns, channel-partner mappings); replay
no-op via idempotency key on (oid, payload hash).
