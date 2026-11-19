# Customer lifecycle diagnosis

## How the report approaches the problem

The Customer Acquisition Model follows awareness → consideration → purchase → service → loyalty/expansion. The team combines channel evidence, funnel progression, qualitative experience and a cohort view to explain why product/brand appeal is not translating into enough completed and sustained purchasing.

| Stage | Report-level finding | Strategic interpretation |
|---|---|---|
| Awareness | Sources of traffic differ in commercial intent; search is important, while social exposure does not translate directly into equivalent sales | Evaluate traffic quality and the role of each channel rather than volume alone |
| Consideration | Product interest and cart activity exist, with uneven product/page performance | Improve clarity, context and trust; do not equate interest with purchase |
| Purchase | Significant loss occurs between cart and completed purchase | Investigate the purchase experience and test changes with comparable funnel definitions |
| Service | Product satisfaction and delivery do not emerge as the dominant problem | A satisfactory first transaction does not automatically create an ongoing relationship |
| Loyalty/expansion | Repeat engagement is limited and follow-up lacks a clear ongoing structure | Assess post-purchase relationship development using mature customer cohorts |

The report’s internal numbers were modified for confidentiality. This public page preserves the reasoning without reproducing the client’s rate series, screenshots or transaction amounts. The synthetic calculations below are new public demonstrations, not reconstructions of the client tables.

## Reproduce the methods

```bash
python3 lifecycle.py
```

The generated report compares three synthetic channel groups, calculates conditional funnel progression and evaluates repeat behavior by cohort horizon. A [readable example](examples/customer_lifecycle_diagnostic.md) is included.

### Funnel denominator discipline

Overall conversion uses all eligible sessions. Cart-to-purchase progression uses add-to-cart sessions. A loss between those stages is not a subtraction between two percentages that use different denominators. Inputs must describe a compatible period, attribution rule and session population.

The demonstration fixture assumes sequential, session-based stages. Real tracking may include skipped events, cross-device journeys or incomplete instrumentation; those require explicit treatment rather than silently imposing the same nesting rule.

### Cohort maturity

Recent cohorts may not have reached later follow-up horizons. A blank or immature month is not a zero-return cohort. The code excludes unobserved cells from the horizon’s eligible denominator and aggregates counts before calculating a weighted rate.

A cohort rate for one month is not customer lifetime value or a causal effect of follow-up activity. The project identifies where further commercial attention is warranted; implementation outcomes require a valid measurement design.
