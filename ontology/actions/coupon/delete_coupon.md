---
type: "Ontology Action"
action: delete_coupon
family: coupon
object: coupon
resource: "urn:ultracart:ontology:action:delete_coupon"
api:
  method: DELETE
  path: /coupon/coupons/{coupon_oid}
  scope: coupon_write
  effect: "deletes one coupon by oid"
  docs: https://www.ultracart.com/api/resource_coupon.html
mutates: ["coupon (row removed)"]
risk: medium
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (risk >= medium)
  - dry_run
status: declared
---

# delete_coupon

Remove one coupon by `coupon_oid`. Deletion is the blunt instrument — for "stop
this promo" the gentler edit is updating the coupon's expiration via
`PUT /coupon/coupons/{coupon_oid}` (declared in `../catalog.md`), which preserves
history and redemption stats. Prefer expiring over deleting; register this action
for genuine mistakes (wrong code created, duplicate).

Addressing: the API pairs `coupon_oid` (internal) with `merchant_code` (human).
This action takes the **oid**; resolve from the code via a read first and pin the
oid in the audit row — codes are what operators type, oids are what must be
deleted. The bulk variants (`DELETE /coupon/coupons/by_code`, `by_oid` — multiple
at once) are bulk-tier surfaces outside this file.

Failure modes:
- **Live-promo breakage** — deleting a code that is printed in a scheduled or
  already-sent campaign turns future checkouts into "invalid coupon" errors at the
  worst moment. Guard: check the code is expired or was never announced; dry-run
  shows redemption count and expiration before the delete.
- **In-flight carts** — customers holding the code in an open cart lose the
  discount at finalize; expiring with a grace window avoids the support spike.
- Irreversible: there is no undelete; recreating the coupon produces a new oid and
  loses redemption history.
- Replay: deleting an already-deleted oid should surface as a no-op success in the
  implementation (idempotent delete), not an error escalation.
