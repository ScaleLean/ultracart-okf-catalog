---
type: "Ontology Action"
action: swap_auto_order_item
family: auto_order
object: auto_order_item
resource: "urn:ultracart:ontology:action:swap_auto_order_item"
api:
  method: PUT
  path: /auto_order/auto_orders/{auto_order_oid}
  scope: auto_order_write
  effect: "read-modify-write of the container: sets items[].arbitrary_item_id so future rebills ship a different item"
  docs: https://www.ultracart.com/api/resource_auto_order.html
mutates: [auto_order_item.arbitrary_item_id, auto_order_item.next_item_id]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# swap_auto_order_item

Change *what ships* on future rebills without touching the schedule. UltraCart
models swap via **`items[].arbitrary_item_id`** — "item id that should be rebilled
instead of the normal schedule" — while `next_item_id` is a **calculated,
read-only** reflection of what will actually ship next. Same read-modify-write
`PUT` of the full container as the rest of the family.

Semantics:
- The schedule anchor stays `original_item_id` (the docs: it "controls
  scheduling") — a swap does **not** re-key the item, so frequency,
  `next_shipment_dts`, and rebill history remain attached to the original line.
- Price follows the new item unless overridden: `arbitrary_unit_cost`
  (+ `arbitrary_unit_cost_remaining_orders`), `arbitrary_quantity`, and
  `arbitrary_percentage_discount` ride the same item record. A swap that should
  keep the old price must set the override explicitly in the same PUT.
- Clearing a swap = nulling `arbitrary_item_id` (revert to the scheduled item).

Failure modes:
- **Invalid / non-auto-orderable target SKU** — the target must be a live item;
  check `item.auto_orderable` and its `auto_order_schedules[]` allow the current
  frequency, or the next rebill can fail and start dunning
  (`auto_order.failure_reason`).
- **Silent price change** — swapping to a differently-priced item without an
  explicit `arbitrary_unit_cost` decision changes what the customer is charged;
  dry-run must show old vs new unit cost side by side.
- Catalog-side subscription config on the *target* item (upgrade/downgrade lists,
  `cancel_other_auto_orders`, step schedules) can trigger side effects — review in
  dry-run.
- Never write `next_item_id` (calculated); never fabricate oids — address the item
  by its existing `auto_order_item_oid`.
- Sparse-PUT clobber, lost update, 429 — shared mitigations in
  `pause_auto_order_item.md`.
