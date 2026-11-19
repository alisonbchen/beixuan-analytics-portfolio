# Payment Networks — Public Financial Research

An independent comparison of Visa and Mastercard using six company-year observations from their FY2025 annual filings. The question is whether reported revenue and profitability changes tell the same story when GAAP and company-adjusted expense bases are examined separately.

## Run

Python 3.10+ and SQLite from the standard library; no network request or API credential is needed.

```bash
python3 research.py
python3 -m unittest discover -s tests -v
```

Outputs: `build/metrics.json`, `build/metrics.csv` and `build/comparison.md`. See the checked-in [example comparison](examples/comparison.md).

## Method

- Manually transcribe revenue, GAAP operating income and disclosed adjusted operating expenses for FY2023–FY2025; retain filing URLs in every source row.
- Validate unique company/year keys and positive revenue.
- Load observations into SQLite and use window functions to calculate consecutive-year growth and margin changes.
- Compare GAAP operating margin with a **derived adjusted margin**, calculated as `(revenue − disclosed adjusted operating expenses) / revenue`.
- Explain why a change in reported profitability requires reading reconciliation items before drawing an operational conclusion.

Year-on-year revenue growth is a percentage; a change between margin percentages is a percentage-point difference. Missing prior years produce no year-on-year estimate. Source amounts are rounded USD millions, so calculations can differ slightly from company-reported rounded percentages.

## Findings to inspect

The FY2025 calculation highlights different GAAP and adjusted-margin movements, particularly for Visa. The example report shows the arithmetic; the filings' non-GAAP reconciliations identify the relevant adjustments. Differences in company definitions and fiscal periods remain important when comparing these measures.

Visa's fiscal year ends September 30; Mastercard's ends December 31. This is not a same-calendar-period comparison. Company-specific adjusted expenses are not a harmonized accounting measure. The project compares disclosed financial performance; it does not calculate valuation, expected share-price returns or an optimized portfolio.

## Sources and provenance

The numeric inputs were rechecked against the public filings during portfolio preparation. Only the small numeric transcription is included, not full filing text.

| Company | Source | Filing sections |
|---|---|---|
| Visa | [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm) | Consolidated Statements of Operations; non-GAAP financial results/reconciliations |
| Mastercard | [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm) | Consolidated Statement of Operations; Non-GAAP Financial Information |

[`financials.json`](data/financials.json) contains one source URL per observation; [`analysis.sql`](analysis.sql) contains the calculations. Tests check growth arithmetic, percentage-point changes, duplicate keys and missing-year behavior.
