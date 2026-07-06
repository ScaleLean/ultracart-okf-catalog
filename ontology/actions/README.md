# Actions Registry — governed writes against UltraCart REST API v2

The ontology's write surface. Layer-1 answers "what data exists"; definitions answer
"what words mean"; **actions answer "what may be done"** — every state-changing
operation an agent or tool could perform against the store, declared with its risk
and the guards an implementation must satisfy.

Base URL: `https://secure.ultracart.com/rest/v2` (HTTPS mandatory). Full mutating
surface: **371 operations** — see `catalog.md` for the grouped reference. Individual
action files exist only for the **curated governed set**: the semantic actions a
merchant is actually expected to register for agent use.

## Declared vs registered

- **`status: declared`** — the action exists in the catalog and its contract
  (endpoint, mutated ontology fields, risk, guard template) is specified. Declared
  means *documented*, **not permitted**. Nothing may execute a declared action.
- **`status: registered:<merchant>`** — a specific merchant has implemented the
  action with all `required_guards` satisfied and listed it in their overlay. Only
  registered actions are executable, and only through the guarded implementation.

An action file never contains credentials, and registration never weakens the guard
template — a merchant may add guards, not remove them.

## Risk tiers

| Tier | Rule | Examples |
|---|---|---|
| **high** | Moves money, initiates **marketing outbound contact**, mutates consent irreversibly, or acts in **bulk** | refund, cancel order/auto-order, campaign start, flow enroll/backfill, globalUnsubscribe, `/bulk/{object}`, gift-certificate creation, PBX number purchase |
| **medium** | Single-record state change on live commerce/marketing data | pause a subscription item, update an item, edit a customer profile, list add/remove, create/delete one coupon |
| **low** | Reversible config/metadata with no customer-visible effect | report definitions, folders, drafts, tags |

Carve-out: a *transactional, single-recipient re-send* (e.g. resend receipt) is
**medium**, not high — it re-delivers a document the customer already owns. All
*marketing* sends are high, no exceptions.

## Required guards (template)

Every registered implementation MUST provide, per call:

1. **`idempotency_key`** — caller-supplied key; replaying the same key must not
   re-apply the mutation (UltraCart has no native idempotency header — the
   implementation must keep its own key ledger).
2. **`audit_row (action, actor, dry_run, payload)`** — append-only audit record
   written *before* the API call: action urn, human/agent actor, dry-run flag,
   full request payload, and afterwards the response envelope.
3. **`approval_gate (risk >= medium)`** — a human approval step for every medium
   and high action. For high actions the approver must be the **owner** (not the
   requesting agent's operator).
4. **`dry_run`** — every implementation exposes a dry-run mode that resolves the
   target object, computes the exact payload/diff, and stops. Agents default to
   dry-run; a live call requires the approval gate's explicit output.

## Auth & scopes

Three schemes (see mining notes / authentication.html): `x-ultracart-simple-key`
(own-account, IP-restrict it), OAuth 2.0 authorization-code for third-party apps,
and the browser key (checkout-side only — never for governed actions). OAuth scopes
are **per resource family, split read/write**: `{resource}_read` / `{resource}_write`
(`order_write`, `auto_order_write`, `customer_write`, `coupon_write`, `item_write`,
`storefront_write`, `affiliate_write`, `channel_partner_write`, …). Each action file
declares its scope under `api.scope`. Registered implementations request the
narrowest write scope set that covers their actions — never a blanket grant.

## Rate limits

Documented: **1,000 requests/hour and 10,000/day**, leaky-bucket (no fixed reset),
enforced per authorized application AND per IP. Exceeding returns **429 Too Many
Requests**. **Concurrent calls from the same app/IP also 429** — the docs say to
serialize; implementations must run actions through a single-flight queue with
backoff on 429. Aggressive polling is separately flagged as abuse — use webhooks.

## Never-execute surfaces

Two generic surfaces are **never executed by agents without explicit owner
approval**, regardless of registration status:

1. **`POST /bulk/{object}`** (+ `upload-url`, job delete) — the generic bulk-job
   channel. It can mass-mutate any supported object class in one call; a single
   malformed job is a store-wide incident. Owner approval per job, always.
2. **Mass-enrollment / mass-contact marketing ops** — campaign **start**
   (`PUT .../campaigns/{uuid}/start`), flow **backfill**, commseq **enroll**, and
   **`POST .../email/globalUnsubscribe`**. The first three contact many people at
   once; the last irreversibly destroys a consent relationship. Owner approval per
   invocation, always — even for merchants that have registered `send_campaign` or
   `global_unsubscribe`, the approval gate cannot be delegated below the owner.

## File format

See `../SPEC.md` (§ File format — action). One file per **semantic action**;
several actions may share one HTTP endpoint (the six auto-order actions all ride
`PUT /auto_order/auto_orders/{auto_order_oid}`) — the semantic layer, not the HTTP
layer, is the unit of governance.
