---
type: "Ontology Action"
action: create_coupon
family: coupon
object: coupon
resource: "urn:ultracart:ontology:action:create_coupon"
api:
  method: POST
  path: /coupon/coupons
  scope: coupon_write
  effect: "inserts one coupon (merchant_code + typed discount definition)"
  docs: https://www.ultracart.com/api/resource_coupon.html
mutates: ["coupon (new row)"]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# create_coupon

Insert a single coupon. UltraCart models coupon behavior as ~40 discrete typed
schemas (`CouponAmountOffSubtotal`, `CouponFreeShipping`,
`CouponBuyOneGetOne...`, `CouponFreeItemsWithMixMatchPurchase`, …) — exactly one
type block should be populated on the coupon object, alongside `merchant_code`,
description, expiration, and usage restrictions.

Scope boundary for this action (single, bounded discount): the same family's
**batch insert** (`POST /coupon/coupons/batch`), **one-time code generation**
(`POST .../generate_codes`, `.../upload_codes`), and **auto-apply rules**
(`POST /coupon/auto_apply`) are bulk/high-tier surfaces — declared in
`../catalog.md`, not covered by this file. Auto-apply especially: it attaches
discounts to *future carts with no code at all*, a store-wide pricing change.

Failure modes:
- **Unbounded discount** — a coupon with no expiration (`expiration_dts`), no
  usage limit, and a percent-off-subtotal type is a standing liability; dry-run
  must display type, value, expiration, and usage caps, and the guard layer should
  refuse open-ended percent coupons without owner approval.
- **Code collision** — inserting an existing `merchant_code` fails (or worse,
  diverges from the operator's intent); check
  `GET /coupon/coupons/merchant_code/{code}` first. Replay with the same
  idempotency key must not create a second coupon under a mutated code.
- Stacking: coupon interaction with pricing tiers, mix-and-match groups, and other
  coupons is merchant-configured — a coupon that is safe alone can compound.
- Marketing coupling: coupon codes referenced by campaigns/flows go live the
  moment the send fires — coordinate with the marketing family before creating
  codes announced in scheduled sends.
