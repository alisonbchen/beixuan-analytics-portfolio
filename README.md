# Beixuan Chen — Applied Analytics Portfolio

Applied analytics portfolio spanning data engineering, business intelligence, market strategy, and financial research, with project summaries, reproducible code, and analytical findings.

Four runnable projects connect data preparation and analysis to service planning, educational evaluation, retail growth and financial research.

| Project | Decision supported | Implementation | What to inspect |
|---|---|---|---|
| [NYC 311 Demand Explorer](projects/nyc311) | Which boroughs and reported issues warrant further service-demand review? | Python, SQLite, CSV validation, JSON API, browser dashboard | Reconciliation, repeatable loads, fixed share denominators |
| [Education Outcomes Database](projects/education_outcomes) | Can attendance-group results justify changing tutoring provision? | Six-table relational schema, SQL views, cohort validation | Join grain, missing scores, stage/attendance confounding |
| [Gohobi — Retail Growth Analytics](projects/retail_growth) | Which products and channel actions merit limited marketing spend? | Python, Decimal reconciliation, category and order analysis | Product priority, fulfilled-order scope, sales action plan |
| [Payment Networks Financial Research](projects/financial_research) | Do GAAP and adjusted profitability changes tell the same story? | Public SEC filings, SQLite window functions, financial comparisons | Fiscal-period differences, growth versus margin changes |

## Run all projects

Python 3.10 or newer. No third-party Python packages, credentials or network connection are needed for the bundled demonstrations.

```bash
python3 run_all.py
```

This runs all four analyses and their focused tests. Generated databases and results go into ignored `build/` folders. To explore the dashboard afterward:

```bash
cd projects/nyc311
python3 src/app.py
```

Open `http://127.0.0.1:8000`.

## Scope and authorship

These are newly organized public implementations based on my team-project work and analytical questions. They are not an archive of the original submissions or original execution environment. The project pages explain the methods, decisions and limitations.

The NYC public edition uses Python/SQLite and a standard-library web server so it can run without a Spark cluster, PostgreSQL instance or Flask installation. It demonstrates the ingestion → validation → summary → API workflow. It does not claim to execute the original PySpark/PostgreSQL/Flask system or reproduce its historical full-data snapshot.

The education project is a new implementation of the cohort-analysis problem, with a synthetic fixture and programme-specific keys. It includes improvements to missing-value handling and join grain. Original team files and report text are not redistributed.

## Data included

- NYC: a deliberately small, clearly labelled synthetic CSV. An optional downloader fetches four non-identifying fields directly from NYC Open Data.
- Education: generated synthetic records with numeric keys, no names or contact details.
- Retail: generated synthetic product and wholesale-order fixtures, plus a consultancy analysis framework.
- Finance: six company-year numeric observations transcribed from publicly available SEC filings, with source URLs.
- No client sales exports, internship records, personal contact details or private reports are included.

The synthetic outputs are demonstrations, not observed business or public-service improvements. The financial project uses public reported amounts and derived calculations. GitHub Actions runs the offline demonstrations and focused tests on Python 3.10 and 3.12.
