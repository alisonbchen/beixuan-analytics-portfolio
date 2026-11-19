# Gohobi — Sales Growth Strategy and Action Plan

**Project objective: develop a practical sales and marketing strategy to grow Gohobi’s B2C and B2B revenue across its website/Shopify, Faire wholesale and in-person events, within limited marketing and operating resources.**

Gohobi is a tea, ceramics and homeware brand. The consultancy question was how its product offering, positioning, customer journey and channel choices should work together to support sustainable sales growth. The deliverable was a client-facing strategy report and sales recommendations. Product calculations support that decision; they are one workstream within the wider project.

## Read the project

- [Whole-project report](PROJECT_REPORT.md): business problem, research approach, integrated findings and strategic direction.
- [Sales and marketing action plan](ACTION_PLAN.md): how the recommendations address acquisition, conversion, basket value, repeat engagement and wholesale reach.
- [Scope and evidence](SCOPE_AND_EVIDENCE.md): what the client requested, what the shared report supports and what this public edition adds.
- [Commercial review framework](commercial_review.md): the seven dimensions used to examine competitor positioning.
- [Supporting diagnostic example](examples/product_channel_diagnostic.md): a small synthetic product/channel analysis that illustrates the quantitative method.

## How the project answers the growth question

| Workstream | Project question | How it contributes to the sales strategy |
|---|---|---|
| Client objectives and constraints | What growth does the business want, and what can its budget and team support? | Sets the scope and prioritizes feasible actions across retail and wholesale |
| UK/EU tea and homeware research | Which market trends and consumption occasions fit the existing offer? | Connects product selection, gifting and positioning to a commercial opportunity |
| Consumer and purchase journey | How do awareness, purchase decisions and repeat engagement connect? | Frames acquisition, conversion and retention questions and the measurement needed |
| Competitor and brand analysis | Where can Gohobi differentiate, and where might its offer be hard to understand? | Informs navigation, craftsmanship/origin storytelling, experiences and channel choices |
| Product and channel evidence | What do sales records say about product mix and fulfilled wholesale activity? | Supports product priorities and defines the size/scope of existing channel activity |
| Integrated recommendations | Which actions could support sales without a large new spending commitment? | Combines seasonal gifting, clearer brand communication, useful content, bundles, events and selective wholesale |

## Strategic direction from the team report

The report recommends making Gohobi’s existing offer easier to discover, understand and buy, while using gifting, experiences and suitable wholesale partners to extend its reach. The recommendations connect complementary tea/homeware products with seasonal occasions, communicate craftsmanship and origin, develop useful product content, integrate events into sales activity and keep wholesale partnerships selective.

The commercial contribution is an integrated growth strategy and a set of actionable sales choices. The shared report does not establish implemented revenue growth, conversion uplift or a measured return on marketing spend. Its market interpretations and competitor observations belong to the project period, not a fresh audit of today’s market.

## Supporting quantitative implementation

The code is a new public demonstration of one part of the consultancy workflow. All bundled products and orders are generated synthetic examples; confidential client exports and the full team report are not distributed.

```bash
python3 retail.py
python3 -m unittest discover -s tests -v
```

Python 3.10+; no third-party packages. Outputs go to `build/`:

- `results.json`: product mix and wholesale-order scope.
- `categories.csv`: category shares and net revenue per unit.
- `product_channel_diagnostic.md`: supporting findings and additional checks before a product/channel decision.

The implementation reconciles monetary identities, normalizes category labels, retains legitimate repeated product titles, compares category contributions and distinguishes order lines from unique delivered orders. It does not implement the entire consultancy project in Python or turn synthetic findings into client results.

## Evaluation and measurement

The project’s immediate output is the strategy and action framework. To evaluate a later implementation, use consistent channel/time definitions for net revenue, orders, average order value, conversion, repeat purchase, returns, contribution margin and acquisition spend. Market forecasts, recommendation counts and code outputs are not realized sales gains. See the action plan for how each lever would be assessed.
