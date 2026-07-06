---
type: "Ontology Object"
object: analytics_session
domain: storefront_behavior
tier: core
resource: "urn:ultracart:ontology:object:analytics_session"
version: 1
grain: "one analytics session row per client_session_oid"
key:
  fields: [client_session_oid]
  identity_family: client_session_oid
source:
  binding: uc_analytics_sessions
  default_table: "{{source_project}}.{{dataset.medium}}.uc_analytics_sessions"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: client_session_oid
    type: INTEGER
    source: client_session_oid
    meaning: "UltraCart primary key for the analytics session"
  - name: client_id
    type: STRING
    source: client_id
    meaning: "the ucacid analytics client id (visitor cookie); joins affiliate_clicks, screen_recordings, surveys"
  - name: client_pointer_oid
    type: INTEGER
    source: client_pointer_oid
    meaning: "internal visitor pointer (same visitor across sessions)"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "customer identity when identified (base64 sha256; see identity spine)"
  - name: sms_hash
    type: STRING
    source: sms_hash
    meaning: "hashed SMS number when identified via SMS (raw sms excluded)"
  - name: customer_profile_oid
    type: INTEGER
    source: customer_profile_oid
    meaning: "registered profile if the visitor logged in (NULL for guests)"
  - name: order_id
    type: STRING
    source: order_id
    meaning: "order placed in this session, if any (session -> conversion link)"
  - name: session_at
    type: DATETIME
    source: session_dts
    meaning: "session timestamp"
  - name: first_seen_at
    type: DATETIME
    source: first_seen_dts
    meaning: "first activity in the session"
  - name: last_seen_at
    type: DATETIME
    source: last_seen_dts
    meaning: "last activity in the session"
  - name: visitor_number
    type: INTEGER
    source: visitor_number
    meaning: "sequential visitor number for the merchant"
  - name: new_visitor
    type: BOOLEAN
    source: new_visitor
    meaning: "first session ever seen for this visitor"
  - name: new_customer
    type: BOOLEAN
    source: new_customer
    meaning: "session belonged to a first-time customer"
  - name: is_bot
    type: BOOLEAN
    source: "(SELECT MAX(hits.session_start.bot) FROM UNNEST(hits) AS hits)"
    meaning: "session flagged as bot traffic (filter these out of behavior metrics)"
  - name: bounced
    type: BOOLEAN
    source: "(SELECT MAX(hits.session_start.bounce) FROM UNNEST(hits) AS hits)"
    meaning: "single-page bounce flag from session start"
  - name: channel
    type: STRING
    source: "(SELECT MAX(hits.session_start.channel) FROM UNNEST(hits) AS hits)"
    meaning: "UltraCart-classified acquisition channel for the session"
  - name: referrer
    type: STRING
    source: "(SELECT MAX(hits.session_start.referrer) FROM UNNEST(hits) AS hits)"
    meaning: "referrer URL at session start"
  - name: geo_country
    type: STRING
    source: "(SELECT MAX(hits.session_start.geolocation_country) FROM UNNEST(hits) AS hits)"
    meaning: "coarse geo: country (lat/long deliberately not exposed)"
  - name: geo_province
    type: STRING
    source: "(SELECT MAX(hits.session_start.geolocation_province) FROM UNNEST(hits) AS hits)"
    meaning: "coarse geo: province/state"
  - name: device_user_agent
    type: STRING
    source: "(SELECT MAX(hits.session_start.user_agent) FROM UNNEST(hits) AS hits)"
    meaning: "user-agent string at session start (device/browser signal)"
  - name: screen_recording_uuid
    type: STRING
    source: "(SELECT MAX(hits.session_recording.screen_recording_uuid) FROM UNNEST(hits) AS hits)"
    meaning: "linked screen recording, if one was captured — the bridge to the screen_recording surface"
  - name: utm_source
    type: STRING
    source: "(SELECT MAX(utms.utm_source) FROM UNNEST(utms) AS utms WHERE NOT utms.prior_session)"
    meaning: "utm_source captured during this session (prior-session carryover rows excluded; MAX collapses rare multi-touch sessions)"
  - name: utm_medium
    type: STRING
    source: "(SELECT MAX(utms.utm_medium) FROM UNNEST(utms) AS utms WHERE NOT utms.prior_session)"
    meaning: "utm_medium captured during this session"
  - name: utm_campaign
    type: STRING
    source: "(SELECT MAX(utms.utm_campaign) FROM UNNEST(utms) AS utms WHERE NOT utms.prior_session)"
    meaning: "utm_campaign captured during this session"
  - name: has_paid_click_id
    type: BOOLEAN
    source: "(SELECT COUNTIF(utms.gclid IS NOT NULL OR utms.fbclid IS NOT NULL OR utms.msclkid IS NOT NULL OR utms.ttclid IS NOT NULL) > 0 FROM UNNEST(utms) AS utms)"
    meaning: "any ad-platform click id (gclid/fbclid/msclkid/ttclid) on any touch"
  - name: utm_touch_count
    type: INTEGER
    source: "ARRAY_LENGTH(utms)"
    meaning: "UTM touch rows on the session (>1 means consult the excluded utms array for multi-touch detail)"
  - name: first_utm_at
    type: DATETIME
    source: "(SELECT MIN(utms.ts) FROM UNNEST(utms) AS utms)"
    meaning: "earliest UTM touch timestamp (including prior-session carryover)"
  - name: hit_count
    type: INTEGER
    source: "ARRAY_LENGTH(hits)"
    meaning: "total hit events in the session"
  - name: page_view_count
    type: INTEGER
    source: "(SELECT COUNT(hits.page_view.url) FROM UNNEST(hits) AS hits)"
    meaning: "page-view hits in the session"
links:
  - to: order
    kind: converted_to
    on: "analytics_session.order_id = order.order_id"
  - to: customer
    kind: belongs_to
    on: "analytics_session.email_hash_b64 = customer.email_hash_b64"
  - to: customer_profile
    kind: belongs_to
    on: "analytics_session.customer_profile_oid = customer_profile.customer_profile_oid"
  - to: screen_recording
    kind: has_one
    on: "analytics_session.screen_recording_uuid = screen_recording.screen_recording_uuid"
pii: pseudonymous
excluded_fields:
  - email            # raw email (permissive tiers only) — use email_hash_b64
  - sms              # raw SMS number — use sms_hash (hashed twin exists in this table)
  - hits             # 400+ nested event paths; carries raw user_ip, names, addresses inside session_start / ecommerce_* events
  - utms             # full multi-touch array; session-level scalars derived above
consumers: []
---

# AnalyticsSession

UltraCart's own analytics session: one visit by one visitor (`client_id` = the
**ucacid**), with a nested `hits[]` trail replaying page views, cart events, checkout
steps, e-commerce outcomes, and even email engagement inside the session. The canonical
view keeps the session scalars and derives a handful of aggregates; the `hits[]` array
itself is excluded (it is where raw `user_ip`, names, and addresses hide — see
`excluded_fields`). Note the raw-IP situation is inverted vs `screen_recording`: here IP
only exists inside the excluded `hits[]`, and SMS has a hashed twin (`sms_hash`) which is
what we expose.

**Three overlapping session surfaces — pick the right one:**

- **analytics_session** (this object, `uc_analytics_sessions`): the *behavioral/funnel*
  surface. Richest event trail (checkout steps, cart abandons, bot flags, in-session
  commerce outcomes). Ask it: "what did the visitor do?", funnel drop-off, bounce/bot
  filtering, session-level conversion.
- **screen_recording** (`uc_screen_recordings`): the *acquisition/replay* surface — URL
  and referrer params, ad-platform click IDs, comms campaign/flow attribution. Ask it:
  "where did the visitor come from?" and "which pages, in what order?". It is also the
  identity spine other tables reference (`screen_recording_uuid` on affiliate clicks and
  ESP sessions).
- **storefront_customer_session** (`uc_storefront_customer_sessions`, modeled in
  marketing_comms): the *ESP/marketing-audience* view of the same visit. Ask it
  audience-scoped questions ("sessions of customers on list X").

The three link via `screen_recording_uuid` (exposed here when a recording exists),
`ucacid` (`client_id` here = `ucacid` on screen recordings, affiliate clicks, surveys),
and `order_id` when the visit converted.

Gotchas:
- `utm_*` scalars exclude touches inherited from prior sessions (`prior_session` rows);
  `utm_touch_count`/`first_utm_at` cover the full array. Multi-touch attribution needs
  the raw `utms[]` — model it separately if ever required.
- Always filter `is_bot` for engagement metrics; `session_start.fake_bot` also exists
  inside the excluded hits array.
- `customer_profile_oid` is only set for logged-in profile sessions; `email_hash_b64`
  identifies more sessions (identified guests) — prefer it for person-level joins.

## Change log
- v1 (2026-07-06) — initial.
