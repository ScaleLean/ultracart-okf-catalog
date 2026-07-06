---
type: "Ontology Action Catalog"
resource: "urn:ultracart:ontology:actions:catalog"
version: 1
timestamp: "2026-07-06T00:00:00Z"
source: "UltraCart openapi.json (OpenAPI 3.0.1, 446 paths / 622 operations / 371 mutating-verb ops), mined 2026-07-05"
---

# Mutating-endpoint catalog — UltraCart REST API v2

Every POST/PUT/DELETE family in the spec, grouped by API tag. **Counts include the
`(read)` POST-query/search/batch-retrieve operations** noted in the mining doc —
those carry a query body on a POST verb and must be classified as *reads* by any
registry implementation, not writes. Risk tier is the family's *dominant* tier;
individual ops may sit a tier lower (folders, drafts) or higher (noted).

Only the curated subset gets an action file (see per-family directories); this table
documents the full surface so nothing is invisible to governance.

| Family | Mutating ops | Example ops | Risk tier |
|---|---|---|---|
| order | 22 | `PUT .../refund`, `POST .../cancel`, `POST .../process_payment`, `POST /order/orders` (insert), hold release, resend receipt/shipment emails | **high** (money) |
| auto_order | 11 | `PUT /auto_order/auto_orders/{oid}` (all schedule/state edits), `PUT .../pause`, item cancel, consolidate, establish-from-order | **high** (recurring billing) |
| customer | 16 | `PUT /customer/customers/{oid}`, merge, `POST .../store_credit`, `POST .../adjust_cashback_balance`, email_lists update, magic link, wishlist CRUD | medium (store_credit/cashback/magic_link: **high**) |
| item | 17 | `PUT /item/items/{oid}`, batch update, delete, gated codes CRUD/generate, reviews CRUD, digital library CRUD | medium (delete/batch: high) |
| coupon | 12 | `POST /coupon/coupons`, update, delete, batch insert/update, delete by_code/by_oid, generate/upload one-time codes, auto_apply rules | medium (batch/generate & auto_apply: **high** — bulk discount exposure) |
| storefront / email marketing | 104 | lists/segments CRUD+archive/sunset, `.../lists/{uuid}/subscribe`, campaign insert/**start**, flow insert/**backfill**, commseq **enroll**/test/release-waiting, emails/postcards CRUD+test, **globalUnsubscribe**, sending domains, Twilio, transactional-email update, experiments, code library, file manager | **high** (outbound contact; content/folder CRUD: low–medium) |
| webhook | 5 | add/update/delete webhook, delete by URL, reflow historical events | medium (webhooks egress order/customer data — review destination) |
| channel_partner | 9 | import order, cancel by partner/UC order id, `PUT .../orders/{id}/refund`, ship-to preferences CRUD | **high** (money) |
| fulfillment | 3 | ack orders, update DC inventory, upload shipments/tracking | medium (shipments trigger customer emails) |
| gift_certificate | 8 | create, update, delete, add ledger entry (balance adjust) | **high** (creates store value) |
| affiliate | 6 | insert/update/delete affiliate | medium |
| fraud | 5 | insert rule, rules from order, delete rule, decline email | medium (bad rule blocks checkout) |
| checkout | 14 | `PUT /checkout/cart`, `finalizeOrder`, handoff, profile login/register, browser key setup | medium (`finalizeOrder`: **high** — charges payment) |
| datawarehouse | 19 | custom reports/dashboards CRUD + execute, ad-hoc report execute/dryrun | low |
| conversation | 78 | webchat/SMS ops, **sms_unsubscribe**, canned messages/departments/engagements CRUD; PBX: phone-number purchase/delete, menus, queues, voicemail, agents | **high** (number purchase = money; support config: medium) |
| tax | 17 | activate/configure providers (avalara/sovos/taxjar/ultracart/self), setActive, self-provider jurisdiction rates CRUD | medium (misconfig = wrong tax collection) |
| user / sso / oauth / bulk / workflow / misc | 25 | user & group CRUD, sso authorize/token/revoke, oauth token/revoke/device, **`POST /bulk/{object}`** (+ upload-url, job delete), workflow tasks, conversation_embed device auth | **high** (bulk = mass mutation; user/group = access control; sso/oauth token ops: low) |

**Total: 371.** Sum of rows = 346 named-family ops + 25 in the residual row.

Cross-cutting notes for implementers:

- The two **never-execute surfaces** (`/bulk/{object}`; campaign start / flow
  backfill / commseq enroll / globalUnsubscribe) are defined in `README.md` and
  apply on top of any per-file risk tier.
- `(read)` POSTs in the mining doc (order/auto_order/customer/coupon query, batch
  retrieve, validate, format, DataTables, search, stats endpoints) are reads:
  register them under `{resource}_read`, no write guards needed.
- Update endpoints are **read-modify-write on the full object** (`_expand` on the
  GET, then PUT the whole object back). A sparse PUT silently clears omitted
  fields — every registered update implementation must GET-with-expansion first.
- REST API and back office operate in **EST; the BigQuery warehouse is UTC**.
  Any action that writes a date/time (e.g. `next_shipment_dts`) must convert.
