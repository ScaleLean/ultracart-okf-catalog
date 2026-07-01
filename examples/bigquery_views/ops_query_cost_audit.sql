-- Source inspiration: UltraCart public Data Warehouse sample query "Finding Expensive Queries in a Project".
-- Grain: one row per normalized BigQuery query text in the selected billing project and date range.
WITH job_rows AS (
  SELECT
    query,
    total_bytes_processed / 1024 / 1024 / 1024.0 AS gb_processed,
    total_bytes_billed / 1024 / 1024 / 1024 / 1024 * 5.0 AS estimated_cost_usd
  FROM `{{ billing_project }}.region-{{ bq_region }}.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
  WHERE creation_time >= TIMESTAMP('{{ cost_start_date }}')
    AND creation_time < TIMESTAMP('{{ cost_end_date }}')
    AND job_type = 'QUERY'
    AND statement_type != 'SCRIPT'
)
SELECT
  query,
  ROUND(SUM(gb_processed), 2) AS gb_processed,
  ROUND(SUM(estimated_cost_usd), 2) AS estimated_cost_usd,
  COUNT(*) AS execution_count
FROM job_rows
GROUP BY query
ORDER BY estimated_cost_usd DESC, gb_processed DESC
LIMIT 100;
