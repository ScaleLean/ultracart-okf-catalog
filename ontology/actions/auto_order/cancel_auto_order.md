---
type: "Ontology Action"
action: cancel_auto_order
family: auto_order
object: auto_order
resource: "urn:ultracart:ontology:action:cancel_auto_order"
api:
  method: PUT
  path: /auto_order/auto_orders/{auto_order_oid}
  scope: auto_order_write
  effect: "read-modify-write of the container: disables the auto order and records cancel fields (no dedicated cancel endpoint)"
  docs: https://www.ultracart.com/api/resource_auto_order.html
mutates: [auto_order.status, auto_order.enabled, auto_order.canceled_at, auto_order.canceled_by, auto_order.cancel_reason, auto_order.ended_at, auto_order.subscription_state]
risk: high
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium; owner-level for high)
  - dry_run
status: declared
---

# cancel_auto_order

Permanently end the whole subscription container. **There is no dedicated
"cancel auto order" endpoint** — full cancel is performed by updating the object
via `PUT` (`enabled = false` plus the cancel fields), or arrives as a side effect
of an order refund with `auto_order_cancel=true` (see
`../order/refund_order.md`). The public docs do not fully specify cancel/disable
semantics beyond the field documentation — implementations should verify observed
behavior per merchant before registering (flagged in mining §3).

Risk is **high**: this stops recurring revenue irreversibly-in-practice (there is
no documented "un-cancel"; recovery means establishing a new auto order from an
order via `POST .../reference_order_id/{reference_order_id}`, a new relationship
with a new oid).

Semantics:
- **Cancel reasons are a merchant-configured vocabulary**, fetched from
  `GET /auto_order/auto_orders/cancel_reasons` — never hard-code them; the guard
  layer should validate the supplied reason against the live list.
- `canceled_by_user` records who canceled (merchant vs customer) — set it
  truthfully; downstream churn analytics key on it.
- Distinguish from **`disabled`** (system-driven failed-rebill exhaustion,
  `disabled_dts`) and **single-item cancel**
  (`POST .../reference_order_id/{ref}/items/original/{original_item_id}/cancel`),
  which removes one line but keeps the container alive.
- Catalog-side cancellation guards may apply (`auto_order_cancel_charge_minimum_balance`,
  `auto_order_cancel_minimum_rebill_count/value`, `auto_order_cancel_item_id` —
  a cancellation fee item): dry-run must surface any charge the cancel triggers.

Failure modes: canceling minutes before `next_shipment_dts` can lose to an
in-flight rebill (refund path may then be needed); sparse-PUT clobber can wipe
unrelated fields while setting cancel state; replay must be a no-op on an
already-`canceled` container. EST/UTC applies to `canceled_dts` interpretation.
