---
type: "Ontology Action"
action: skip_next_shipment
family: auto_order
object: auto_order_item
resource: "urn:ultracart:ontology:action:skip_next_shipment"
api:
  method: PUT
  path: /auto_order/auto_orders/{auto_order_oid}
  scope: auto_order_write
  effect: "read-modify-write of the container: advances items[].next_shipment_dts by one frequency interval"
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

# skip_next_shipment

Skip exactly one upcoming rebill. **There is no dedicated skip endpoint** in the
API — skip is performed by advancing `items[].next_shipment_dts` by one frequency
interval (mining §3). This action is `change_next_shipment_date` with the target
date *derived* rather than caller-supplied: new date = current `next_shipment_dts`
+ one `frequency` period (`Weekly`, `Monthly`, `Every 45 Days`, …, or
`arbitrary_schedule_days` for N-day cycles).

Why it is a distinct semantic action: "skip one" is what customers ask for, its
payload is deterministic given current state, and its idempotency contract differs
— **replaying a skip must not skip twice**. The idempotency key must bind to the
*observed* pre-skip `next_shipment_dts`, so a retry against already-advanced state
is a no-op, not a second skip.

Failure modes:
- **Double skip** on retry/replay (above) — the family's signature failure; the
  key-binding rule is the defense.
- **Race with the rebill scheduler**: skipping shortly before the scheduled run
  can lose the race — the rebill fires *and* the date advances. Check
  `future_schedules[]` / recent `rebill_orders[]` afterwards.
- Frequency arithmetic in the wrong timezone (**EST API vs UTC warehouse**) drifts
  the bill date; compute in EST.
- Items with `remaining_repeat_count` / `no_order_after_dts`: advancing past the
  stop boundary quietly ends the schedule (`calculated_next_shipment_dts` goes
  null) — surface that in dry-run output rather than discovering it later.
- Sparse-PUT clobber, lost update, 429 — shared mitigations in
  `pause_auto_order_item.md`.
