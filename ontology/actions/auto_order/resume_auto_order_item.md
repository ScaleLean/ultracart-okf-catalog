---
type: "Ontology Action"
action: resume_auto_order_item
family: auto_order
object: auto_order_item
resource: "urn:ultracart:ontology:action:resume_auto_order_item"
api:
  method: PUT
  path: /auto_order/auto_orders/{auto_order_oid}
  scope: auto_order_write
  effect: "read-modify-write of the container: sets items[].paused = false (and normally a future items[].next_shipment_dts)"
  docs: https://www.ultracart.com/api/resource_auto_order.html
mutates: [auto_order_item.paused, auto_order_item.next_shipment_dts, auto_order.all_items_paused, auto_order.subscription_state]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
  - validate next_shipment_dts is in the future before unpausing
status: declared
---

# resume_auto_order_item

Reverse of `pause_auto_order_item`: sets `items[].paused = false` via the same
read-modify-write `PUT` of the full container object. In ontology terms this moves
a `paused` subscription back to `active` once any item is unpaused.

**The billing hazard**: an item paused for months may still carry a
`next_shipment_dts` in the past. Unpausing it can make the item immediately
eligible for processing — i.e. **a charge fires as a side effect of a "resume"**.
The extra guard is therefore mandatory: on resume, always set
`items[].next_shipment_dts` to an explicit, customer-agreed future date in the same
PUT. Dry-run output must display the effective next bill date.

Failure modes:
- **Immediate rebill** from a stale past `next_shipment_dts` (above) — the
  costliest mistake in this family; treat a resume without a date as invalid input.
- **EST vs UTC** — the API interprets datetimes in EST; the warehouse shows UTC.
  Computing "tomorrow" from a warehouse timestamp without converting shifts the
  bill date by the offset.
- **Sparse-PUT clobber / lost update / scheduler race / 429** — identical to
  `pause_auto_order_item.md`; round-trip the full object, serialize, audit both
  snapshots.
- Resuming an item on a `canceled`/`disabled` container does not revive the
  container — check `auto_order.status = 'active'` first; reactivating an ended
  container is out of scope for this action.
