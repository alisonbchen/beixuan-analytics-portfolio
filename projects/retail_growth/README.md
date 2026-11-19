# Gohobi — Customer Lifecycle and Sales Growth Strategy

**How can Gohobi turn product appeal and website traffic into completed purchases, repeat customers and sustainable sales growth, within limited marketing and operating resources?**

This consultancy examined the whole sales and marketing system of a tea and homeware brand. The team combined UK/EU market research, competitor positioning, Shopify/customer evidence and a five-stage Customer Acquisition Model to diagnose where commercial value was being lost and prioritize feasible growth actions across retail, events and wholesale.

## Main diagnosis

The complete project report identifies two central growth constraints: friction between adding products to the cart and completing a purchase, and weak progression from a first purchase to an ongoing customer relationship. Product appeal and satisfactory delivery were not sufficient to produce sustained customer value. The strategy therefore connects acquisition, conversion and retention instead of treating extra traffic or a single product promotion as the whole solution.

## Explore the project

- [Whole-project report](PROJECT_REPORT.md): client challenge, methods, lifecycle findings and strategic conclusion.
- [Prioritized action plan](ACTION_PLAN.md): the report’s impact/effort/timeline matrix, intended mechanisms and measurement requirements.
- [Customer lifecycle analysis](CUSTOMER_LIFECYCLE.md): channel, funnel and cohort reasoning, plus a reproducible synthetic demonstration.
- [Commercial review framework](commercial_review.md): seven dimensions of competitor positioning.
- [Scope and evidence](SCOPE_AND_EVIDENCE.md): original project work, confidentiality boundaries and new public implementations.

## Integrated analytical approach

| Workstream | What the team examined | Why it matters to the growth decision |
|---|---|---|
| Client problem definition | Brand appeal, traffic, inconsistent purchasing, limited long-term customer value and resource constraints | Defines the problem as commercial conversion and customer development, not simply market expansion |
| UK/EU market research | Tea/homeware trends, premium and gift-led consumption, product/market fit | Establishes where the offer can be relevant and differentiated |
| Competitor positioning | Two competitors across product range, price, narrative, shipping, experiences, channels and website presentation | Identifies opportunities to improve discovery, trust and brand-led reach |
| Awareness and consideration | Channel contributions, high-intent search, social discovery, product interest | Separates attracting visitors from generating purchase intent |
| Purchase | Add-to-cart, checkout and purchase progression, with mobile context | Locates a key commercial leakage point |
| Service and loyalty | Satisfaction, delivery, follow-up, repeat behavior and cohorts | Explains why a first purchase may not become an ongoing relationship |
| Recommendations | Seasonal gifting, bundles, narrative, content, events and selective wholesale | Prioritizes actions by impact, effort and implementation horizon |

## Result and deliverables

The team delivered a client-facing strategy report that locates the purchase-conversion and retention constraints, explains them in the context of brand/customer/market evidence, and sets out a prioritized sales and marketing response. These are analytical and strategic deliverables; the report does not establish an implemented revenue uplift.

The original priority matrix distinguishes quick seasonal gifting activity, medium-horizon bundle/narrative/content work and longer-horizon events/wholesale development. See the action plan for the individual impact and effort ratings, which are qualitative planning judgments rather than measured effects.

## Reproducible public code

Two supporting modules demonstrate the analytical mechanics with newly generated synthetic fixtures. They are not copies of client exports or the original project’s execution files.

```bash
python3 retail.py
python3 lifecycle.py
python3 -m unittest discover -s tests -v
```

Python 3.10+; no external packages. The modules produce:

- Product/category and fulfilled-order diagnostics: reconciliation, label normalization, weighted category comparisons and order scope.
- Customer lifecycle diagnostics: channel conversion, conditional funnel progression, drop-off and mature-cohort repeat rates.
- Readable [product/channel](examples/product_channel_diagnostic.md) and [lifecycle](examples/customer_lifecycle_diagnostic.md) examples.

## Evidence and confidentiality

This summary is grounded in the complete 33-page *Gohobi Consulting Project 2025/2026*, including its Customer Research, Recommendations and Conclusion sections. The original report says internal figures were modified for confidentiality. This public edition therefore explains its diagnoses and methods without redistributing the client tables, screenshots, financial amounts or exact internal rate series. All executable examples are explicitly synthetic. Market/industry comparisons belong to the project period, not a new audit of current conditions.
