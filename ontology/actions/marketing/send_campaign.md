---
type: "Ontology Action"
action: send_campaign
family: marketing
object: email_send
resource: "urn:ultracart:ontology:action:send_campaign"
api:
  method: PUT
  path: /storefront/{storefront_oid}/email/campaigns/{email_campaign_uuid}/start
  scope: storefront_write
  effect: "starts a one-shot campaign: mass outbound send to the campaign's target lists/segments"
  docs: https://www.ultracart.com/api/resource_storefront.html
mutates: ["email_send (mass insert — one row per recipient)"]
risk: high
required_guards:
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate (owner-level, per invocation — never-execute surface, see ../README.md)
  - dry_run
status: declared
---

# send_campaign

Fire a one-shot campaign at its configured audience. Campaigns compile to a
commseq (the `begin | wait | email | merge | condition | end` step machine); the
`start` call is the point of no return — after it, the send is executing against
every targeted list/segment member, surfacing in the warehouse as a mass insert
of `email_send` rows (`campaign_name` populated, `flow_name` null).

This is mass outbound contact: **high risk and on the never-execute list**
(`../README.md`) together with flow backfill and commseq enroll. Owner approval
per invocation, always — a campaign send cannot be un-sent, and a bad one burns
deliverability reputation (spam complaints raise
`marketing_contact.spam_complaint_count`, shrinking `marketing_reachable`
permanently).

Pre-flight that a registered implementation must run in dry-run:
- **Audience resolution**: which lists/segments the campaign targets and the
  *current* recipient count (segments are rule-built and drift — the audience at
  start-time is not the audience at authoring-time). Suppression math
  (global unsubscribes, prior spam complainers) should be shown.
- **Content check**: test-send exists as a separate endpoint
  (`POST .../emails/{uuid}/test`) — require a completed test send before start.
- **Coupon dependencies**: codes referenced in the content must exist and not be
  expired (see `../coupon/create_coupon.md`).

Failure modes:
- **Double send** — the catastrophic replay. Idempotency key binds to the
  campaign uuid; a start on an already-started campaign must be refused, not
  retried. A 429/timeout on start must be resolved by *reading* campaign state,
  never by re-calling start.
- Wrong storefront: campaigns are storefront-scoped; uuid collisions across
  scopes are prevented by the path, but audience expectations differ per
  storefront — confirm scope in the approval prompt.
- Partially-failing sends (bad sending-domain config) leave the campaign in a
  degraded state — check sending-domain verification status pre-flight.
