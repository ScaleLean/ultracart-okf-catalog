---
type: "Ontology Action"
action: cancel_order
family: order
object: order
resource: "urn:ultracart:ontology:action:cancel_order"
api:
  method: POST
  path: /order/orders/{order_id}/cancel
  scope: order_write
  effect: "cancels the order; by default refunds/voids payment, or parks in Held Orders with skip_refund_and_hold"
  docs: https://www.ultracart.com/api/resource_order.html
mutates: [order.current_stage, order.payment_status]
risk: high
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium; owner-level for high)
  - dry_run
status: declared
---

# cancel_order

Stop an order before fulfillment. Distinct from `refund_order.md`: cancel targets
the order lifecycle (get it out of the shipping pipeline), refund targets money on
an order that stands. Parameters:

- `lock_self_ship_orders` — prevent a self-shipped order from being picked/packed
  concurrently with the cancel.
- `skip_refund_and_hold` — do **not** refund; move the order to **Held Orders**
  instead. This is the reversible variant (release later via
  `PUT .../hold/release` or `hold/add_items_and_release`).

Risk is high because the default path reverses payment (void or refund depending
on settlement state) — money moves. With `skip_refund_and_hold` the money risk
drops but the order silently leaves the fulfillment flow; ontology stage moves to
`Hold`, which `revenue_order` excludes — a held order disappears from revenue
until released.

Failure modes:
- **Too late to cancel** — an order already in `Shipping Department` may be
  physically picked; a cancel that succeeds in software but not on the dock ends
  as a ship + refund + return. Guard: check `current_stage` and DC acknowledgement
  first; prefer `lock_self_ship_orders`.
- **Auto-order origin** — canceling the original order of a subscription does not
  cancel the auto order; pair with `../auto_order/cancel_auto_order.md` or the
  refund flag `auto_order_cancel` when the intent is "stop everything".
- Replay must be a no-op on an already-canceled/rejected order (idempotency key on
  order_id + observed stage).
- Cancel emails: unlike refund there is no documented skip-notification flag here;
  assume the customer is notified.
