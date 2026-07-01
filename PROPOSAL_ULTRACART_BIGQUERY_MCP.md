# Proposal: UltraCart BigQuery MCP With OKF-Aware Query Guidance

## Executive Summary

UltraCart should implement an official BigQuery MCP server that lets AI agents safely discover, validate, dry-run, and query UltraCart Data Warehouse projects. The MCP should pair live BigQuery access with an UltraCart OKF semantic layer so agents do not start from raw table names alone.

The core idea:

- The BigQuery MCP provides live execution, permissions, schema, dry-run, and result access.
- The UltraCart OKF catalog provides table meaning, safe query grain, access-layer guidance, nested-field patterns, monetary/currency field discovery, and starter query patterns.
- The MCP should automatically route UltraCart warehouse questions through the OKF before generating or running SQL.

This would make UltraCart warehouses substantially easier and safer for merchants, consultants, analysts, and AI agents to use.

## Why This Matters

UltraCart BigQuery warehouses are powerful but structurally complex:

- Data is spread across multiple access-layer datasets such as `ultracart_dw`, `ultracart_dw_low`, `ultracart_dw_medium`, `ultracart_dw_high`, and `ultracart_dw_streaming`.
- The current-state view layers and streaming mutation layer have different query semantics.
- Core records such as orders and customers contain deeply nested repeated fields.
- Many value fields are currency-aware structs, not simple numeric columns.
- A naive join across orders, items, sessions, UTMs, affiliates, and page views can easily double-count revenue or orders.
- Different merchants may have different enabled modules, empty feature tables, access permissions, and available fields.

An official MCP can make this safer by combining live BigQuery verification with UltraCart-authored semantic guidance.

## Recommended Product Shape

UltraCart should ship an official MCP server, tentatively named:

`ultracart-bigquery-mcp`

It should expose two classes of capability:

1. Live BigQuery tools for a merchant warehouse.
2. OKF semantic resources and helper tools for UltraCart-specific interpretation.

The MCP should not treat the OKF catalog as proof that a merchant has a field, table, permission, or runnable SQL path. Instead, the OKF should be the semantic preflight layer. Live BigQuery metadata and dry-runs remain the source of truth for the specific merchant project.

## Recommended Agent Workflow

For any question involving an UltraCart warehouse, a `uc_*` table, or an `ultracart_dw*` dataset, the MCP should guide agents through this sequence:

1. Identify the likely UltraCart warehouse context.
2. Load relevant OKF context:
   - table purpose
   - safe grain
   - join warnings
   - sensitivity/access layer
   - currency-aware fields
   - starter SQL patterns
3. Inspect live BigQuery metadata:
   - available datasets
   - available tables/views
   - live schema
   - access permissions
4. Generate SQL against the least-privileged dataset that can answer the business question.
5. Dry-run the SQL and report estimated bytes.
6. Execute only bounded, reviewed queries.
7. Return the result with notes on grain, access layer, field semantics, and remaining risks.

In short:

`OKF first for meaning. BigQuery second for proof.`

## Proposed MCP Resources

The MCP should expose OKF content as first-class MCP resources, for example:

```text
okf://ultracart/index
okf://ultracart/references/bigquery_usage
okf://ultracart/references/warehouse_layers
okf://ultracart/references/monetary_fields
okf://ultracart/references/sensitivity_guardrails
okf://ultracart/tables/uc_orders
okf://ultracart/tables/uc_customers
okf://ultracart/tables/uc_auto_orders
okf://ultracart/tables/uc_screen_recordings
okf://ultracart/examples/weekly_marketing_performance
```

These resources should be read-only and merchant-neutral.

## Proposed MCP Tools

### `get_ultracart_okf_context`

Input:

```json
{
  "question": "Which campaign/source combinations generate paid orders, revenue, and AOV weekly?",
  "known_tables": ["uc_orders"],
  "preferred_dataset": "ultracart_dw_medium"
}
```

Output:

```json
{
  "recommended_tables": ["uc_orders"],
  "safe_grain": "one row per paid order before aggregation",
  "recommended_fields": [
    "order_id",
    "creation_dts",
    "payment_status",
    "current_stage",
    "utms",
    "summary.total.value",
    "summary.total.currency_code"
  ],
  "join_warnings": [
    "Do not join unnested items and attribution touches in the same aggregate without pre-aggregating.",
    "Use order-level revenue before grouping by week and campaign/source."
  ],
  "access_notes": [
    "Start with the least-privileged current-state access layer that contains required fields.",
    "Do not use ultracart_dw_streaming for ordinary weekly reporting."
  ],
  "validation_required": [
    "Verify fields against live merchant schema.",
    "Dry-run generated SQL before execution."
  ]
}
```

### `list_ultracart_warehouse_datasets`

Lists accessible UltraCart warehouse datasets for the configured project, including access-layer interpretation:

- `ultracart_dw`
- `ultracart_dw_low`
- `ultracart_dw_medium`
- `ultracart_dw_high`
- `ultracart_dw_streaming`
- linked-account datasets when present

### `inspect_ultracart_table`

Returns live schema plus OKF context for a table.

Example:

```json
{
  "project": "merchant-project",
  "dataset": "ultracart_dw_medium",
  "table": "uc_orders"
}
```

Should return:

- live table/view existence
- live field paths
- OKF table purpose
- known nested arrays
- currency-aware structs
- sensitivity warnings
- common query grains

### `dry_run_ultracart_sql`

Runs BigQuery dry-run validation and returns:

- bytes processed estimate
- referenced tables
- detected access layer
- warnings if the query uses streaming tables for normal reporting
- warnings if the query uses `SELECT *`
- warnings if the query unnests multiple repeated fields without pre-aggregation

### `run_ultracart_query`

Executes bounded SQL after validation. It should require:

- explicit project
- explicit billing project
- maximum bytes billed
- row limit unless writing to a destination table
- clear indication whether raw row-level PII can be returned

## Suggested Tool Description Guardrails

Every BigQuery query-generation tool should include guidance like:

> For UltraCart projects, datasets beginning with `ultracart_dw`, or tables beginning with `uc_`, first consult the UltraCart OKF resources for table grain, access layer, sensitivity, monetary fields, and join warnings. Treat OKF as semantic guidance, not live validation. Always verify against live BigQuery metadata and dry-run SQL before claiming a query is runnable.

This matters because agents often overfit to column names and miss the warehouse semantics.

## Access Layer Guidance

The MCP should explain the UltraCart access model in plain language:

| Dataset | Use |
|---|---|
| `ultracart_dw` | Standard current-state reporting views without sensitive fields. |
| `ultracart_dw_low` | Low-access current-state reporting views with additional non-high-risk fields. |
| `ultracart_dw_medium` | Medium-access current-state reporting views with customer PII fields. |
| `ultracart_dw_high` | High-access current-state reporting views with the most restricted fields. |
| `ultracart_dw_streaming` | Physical mutation stream; use for freshness, delete behavior, and view validation, not ordinary reporting. |
| `ultracart_dw_linked*` | Parent-account linked-account reporting layers when present. |

The MCP should encourage least-privileged querying and make it clear that access level affects visible columns.

## Example: Weekly Marketing Performance

Business question:

> A general UltraCart merchant wants to understand weekly marketing performance. Which campaign/source combinations are generating paid orders, revenue, and average order value?

The MCP should guide the agent to:

- Start from `uc_orders`.
- Use one row per paid order before aggregation.
- Extract campaign/source from order UTM structures or equivalent order-level attribution fields.
- Aggregate after the order-level grain is stable.
- Compute revenue from currency-aware monetary structs, preserving `currency_code` where needed.
- Avoid joining order items, page views, sessions, and affiliate ledgers into the same raw aggregate unless each is pre-aggregated to a compatible grain.

Starter shape:

```sql
WITH order_level AS (
  SELECT
    DATE_TRUNC(DATE(order_datetime, @reporting_time_zone), WEEK(MONDAY)) AS week_start,
    COALESCE(utm_source, '(unknown)') AS source,
    COALESCE(utm_campaign, '(unknown)') AS campaign,
    order_id,
    total_value,
    currency_code
  FROM `{{ source_project }}.{{ access_dataset }}.uc_orders`
  WHERE order_datetime >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @lookback_days DAY)
    AND is_paid_order = TRUE
)
SELECT
  week_start,
  source,
  campaign,
  currency_code,
  COUNT(DISTINCT order_id) AS paid_orders,
  SUM(total_value) AS revenue,
  SAFE_DIVIDE(SUM(total_value), COUNT(DISTINCT order_id)) AS average_order_value
FROM order_level
GROUP BY week_start, source, campaign, currency_code
ORDER BY week_start DESC, revenue DESC;
```

The exact field names should be selected from live schema inspection plus the OKF table context. The MCP should not claim this exact SQL runs until it has been dry-run against the merchant project.

## Security And Privacy Requirements

The MCP should:

- Prefer metadata, dry-runs, and aggregate queries before row-level reads.
- Avoid returning raw PII unless explicitly allowed.
- Prefer hashed identifiers when raw emails, addresses, or phone numbers are not required.
- Warn before querying higher-access datasets.
- Never persist merchant row samples into public OKF resources.
- Redact merchant project IDs from shared reports unless explicitly intended.
- Require explicit billing project and maximum bytes billed.
- Support audit logging of executed SQL, bytes billed, caller, and timestamp.

## Query Safety Requirements

The MCP should warn or block when it sees:

- `SELECT *` against large nested tables.
- Direct ordinary-reporting queries against `ultracart_dw_streaming`.
- Multiple independent `UNNEST` operations that can multiply rows.
- Joins between order header, item lines, attribution touches, sessions, and affiliate events without pre-aggregation.
- Missing date filters on large behavior/session tables.
- Aggregation of currency-aware values without preserving or filtering currency code.
- Claims that structural catalog validation proves SQL execution.

## Implementation Options

### Option A: OKF Bundled With MCP

Ship a reviewed OKF bundle inside the MCP package.

Pros:

- Easy install.
- Stable default context.
- Works without network access to a separate OKF service.

Cons:

- Requires MCP package releases when OKF changes.

### Option B: OKF Loaded From Versioned URL

MCP reads a signed/versioned OKF artifact from UltraCart-hosted infrastructure.

Pros:

- OKF updates can ship independently.
- Central source of truth.

Cons:

- Requires availability/version handling.

### Option C: Hybrid

Bundle a baseline OKF snapshot and optionally refresh from an UltraCart-hosted version.

Recommendation: start with Option C.

## Proposed Rollout

### Phase 1: Read-only MCP

- BigQuery authentication through Google ADC or service account.
- Dataset/table/schema listing.
- OKF resources exposed through MCP.
- OKF context helper tool.
- SQL dry-run support.
- No row-level query execution by default.

### Phase 2: Controlled Query Execution

- Bounded aggregate query execution.
- Maximum bytes billed.
- Required row limits.
- PII-safe result controls.
- Query warnings for known UltraCart grain risks.

### Phase 3: Report Workflows

- Saved report definitions.
- Replayable SQL and chart/report manifests.
- Standard merchant dashboards.
- Query-cost audit tools.
- Optional linked-account rollups.

## Success Criteria

The project is successful if:

- Agents can answer common merchant warehouse questions without guessing table meaning.
- Generated SQL is routinely dry-run before execution.
- Weekly marketing, order economics, subscriptions, affiliate, and product reports use safe grains.
- Currency-aware values are easy to discover and handled correctly.
- Sensitive fields are not casually exposed.
- The MCP clearly distinguishes OKF semantic guidance from live merchant validation.

## Final Recommendation

UltraCart should implement the BigQuery MCP as an official, read-only-first analytics interface for AI agents. The MCP should automatically consult the UltraCart OKF catalog whenever it detects UltraCart warehouse datasets or `uc_*` tables.

This makes the OKF catalog the semantic preflight layer and BigQuery the live proof layer. That combination is the safest path: agents get enough UltraCart-specific context to write better SQL, while final claims still depend on live schema checks, permissions, dry-runs, and bounded execution.
