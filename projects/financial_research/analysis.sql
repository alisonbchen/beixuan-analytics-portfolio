WITH metrics AS (
 SELECT company, fiscal_year, year_end, revenue,
  100.0 * operating_income / revenue AS gaap_margin_pct,
  100.0 * (revenue - adjusted_opex) / revenue AS derived_adjusted_margin_pct,
  LAG(revenue) OVER (PARTITION BY company ORDER BY fiscal_year) AS previous_revenue,
  LAG(100.0 * operating_income / revenue) OVER (PARTITION BY company ORDER BY fiscal_year) AS previous_gaap_margin,
  LAG(100.0 * (revenue - adjusted_opex) / revenue) OVER (PARTITION BY company ORDER BY fiscal_year) AS previous_adjusted_margin
 FROM financials
)
SELECT company, fiscal_year, year_end, revenue,
 100.0 * (revenue / previous_revenue - 1.0) AS revenue_growth_pct,
 gaap_margin_pct, gaap_margin_pct - previous_gaap_margin AS gaap_margin_change_pp,
 derived_adjusted_margin_pct, derived_adjusted_margin_pct - previous_adjusted_margin AS adjusted_margin_change_pp
FROM metrics ORDER BY company,fiscal_year;