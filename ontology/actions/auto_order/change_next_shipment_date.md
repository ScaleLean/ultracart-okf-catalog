---
type: "Ontology Action"
action: change_next_shipment_date
family: auto_order
object: auto_order_item
resource: "urn:ultracart:ontology:action:change_next_shipment_date"
api:
  method: PUT
  path: /auto_order/auto_orders/{auto_order_oid}
  scope: auto_order_write
  effect: "read-modify-write of the container: sets items[].next_shipment_dts to a caller-supplied date"
  docs: https://www.ultracart.com/api/resource_auto_order.html
mutates: [auto_order_item.next_shipment_dts, auto_order.next_attempt_at]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# change_next_shipment_date

Move one subscription item's next rebill to an explicit date. Per the API docs the
schedule **lives on the item**: "changing next ship date = updating
`items[].next_shipment_dts` via PUT" — there is no dedicated endpoint. Same
read-modify-write pattern as the rest of the family: GET with `_expand`, set the
field on the item addressed by `auto_order_item_oid`/`original_item_id`, PUT the
full object back.

Semantics and quirks:
- **EST timezone quirk** — the REST API and back office run in **EST**; the
  BigQuery warehouse stores UTC. A date computed from warehouse data and written
  raw lands hours off, which around midnight is a ±1 *day* error on the bill date.
  Convert explicitly; dry-run must show the date as the API will interpret it.
- `calculated_next_shipment_dts` is **read-only** (null when no more shipments) —
  never write it; after the PUT, re-GET and confirm it reflects the new date.
- Moving the date does not change `frequency`; the *following* rebill is computed
  from the new date + frequency.
- Dates in the past make the item immediately eligible for processing — reject
  past dates at the guard layer (same hazard as `resume_auto_order_item`).
- `no_order_after_dts` still wins: a next-shipment date beyond it means no rebill.

Failure modes: sparse-PUT clobber, lost update (no optimistic locking), race with
an in-flight rebill near the old date, 429 on concurrent calls — see
`pause_auto_order_item.md` for the shared mitigations.
