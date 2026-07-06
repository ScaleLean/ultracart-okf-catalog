---
type: "Ontology Action"
action: refund_order
family: order
object: order
resource: "urn:ultracart:ontology:action:refund_order"
api:
  method: PUT
  path: /order/orders/{order_id}/refund
  scope: order_write
  effect: "refunds payment (full or partial via edited order object); optional reject, auto-order cancel, store-credit issue"
  docs: https://www.ultracart.com/api/resource_order.html
mutates: [order.current_stage, order.total_refunded, order.refund_dts, order.payment_status]
risk: high
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium; owner-level for high)
  - dry_run
  - precheck GET /order/orders/{order_id}/refundable
status: declared
---

# refund_order

Return money to a customer. The request body is the **(partially edited) order
object** — a partial refund is expressed by editing item quantities/prices before
the PUT, not by a "refund amount" scalar — plus query flags:

- `reject_after_refund` — refund then move the order to `Rejected`
- `skip_customer_notification` — suppress the refund email
- `auto_order_cancel` (+ `auto_order_cancel_reason`) — also cancel the linked
  subscription (couples this action to `../auto_order/cancel_auto_order.md`)
- `manual_refund` — *record* a refund done externally (no money moves; the only
  non-money variant of this action)
- `reverse_affiliate_transactions` — claw back affiliate credit
- `issue_store_credit` — refund to store credit instead of the original payment
  (requires loyalty configured; store credit rides the customer's internal gift
  certificate)

**Mandatory pre-check**: `GET /order/orders/{order_id}/refundable` returns
`refundable` plus the **merchant-configured reason-code lists**
(`order_level_refund_reasons`, `order_level_reject_reasons`,
`item_level_refund_reasons`, `item_level_return_reasons`) and flags for whether a
reason is required. Reasons are merchant-defined code lists, **not fixed enums** —
validate against the live response, never a hard-coded list.

In the warehouse the effect surfaces as `summary.total_refunded.value` and
`refund_dts`; payment status moves to `Refunded`. In ontology terms `revenue_order`
still includes refunded orders (stage usually remains `Completed Order` unless
`reject_after_refund`) — revenue reporting must net `total_refunded`, which is why
the definition prose flags it.

Failure modes:
- **Double refund on retry** — the classic. A 429/timeout after the gateway
  processed but before the response landed must NOT be retried blind; re-check
  `refundable` / `total_refunded` first. Idempotency key binds to
  (order_id, edited-total).
- Editing the order object wrongly (sparse object) can alter line items beyond the
  refund intent — dry-run must show the exact order diff and computed refund total.
- `issue_store_credit` without loyalty configured fails; `auto_order_cancel` reason
  must come from the merchant's cancel-reason list.
- Payment-method limits: gateway refund windows expire (old orders may only accept
  `manual_refund`), and non-card methods (Check, COD, Wire) have no gateway to
  reverse — expect `manual_refund` there.
