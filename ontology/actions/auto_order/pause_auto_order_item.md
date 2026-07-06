---
type: "Ontology Action"
action: pause_auto_order_item
family: auto_order
object: auto_order_item
resource: "urn:ultracart:ontology:action:pause_auto_order_item"
api:
  method: PUT
  path: /auto_order/auto_orders/{auto_order_oid}
  scope: auto_order_write
  effect: "read-modify-write of the container: sets items[].paused = true on the targeted item"
  docs: https://www.ultracart.com/api/resource_auto_order.html
mutates: [auto_order_item.paused, auto_order.all_items_paused, auto_order.subscription_state]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# pause_auto_order_item

Suspend rebilling of one subscription item without ending the relationship. **Pause
is item-level** in UltraCart (`items[].paused`); there is no container pause flag —
a "paused subscription" is an active container whose items are all paused (the
`auto_order.subscription_state` derivation). Pausing the last unpaused item
therefore flips the container to `paused` in ontology terms.

This is one of six semantic actions sharing `PUT /auto_order/auto_orders/{oid}`.
The pattern is **read-modify-write**: `GET` the auto order with `_expand`, flip
`paused` on the item addressed by `auto_order_item_oid` (or `original_item_id`,
which the docs say controls scheduling), `PUT` the *entire object* back. A separate
container-level convenience endpoint exists (`PUT .../{auto_order_oid}/pause`) —
that pauses at the container scope and is not this action.

Failure modes:
- **Sparse-PUT clobber** — PUTting a partial object clears omitted fields. Always
  round-trip the full expanded object; diff before/after in dry-run.
- **Lost update** — no ETag/optimistic locking; a concurrent back-office edit
  between GET and PUT is silently overwritten. Keep the GET→PUT window short and
  record both snapshots in the audit row.
- **Race with the rebill scheduler** — pausing minutes before `next_shipment_dts`
  may lose to an in-flight rebill; treat a rebill order that appears anyway as
  expected, not a bug. Remember API datetimes are **EST**, warehouse is UTC.
- 429 on concurrency — serialize calls (see `../README.md`).

Idempotent by nature (pausing a paused item is a no-op), but the idempotency-key
guard still applies so replays don't clobber intervening edits.
