# Gohobi — Retail Growth Analytics

A public demonstration of the product and channel analysis behind a retail-growth consultancy problem: **how can a tea and homeware brand increase retail and wholesale sales within a limited marketing budget?**

The original consultancy involved market research, product opportunities, competitor positioning and a sales action plan. This repository is a newly written public coding edition of that analytical approach. All bundled sales and order records are synthetic; they are not altered copies of confidential client exports. Demonstration findings must not be described as Gohobi's actual performance or implemented revenue gains.

## Decisions and outputs

| Question | Method | Decision output |
|---|---|---|
| Which product categories warrant promotion? | Reconcile sales, normalize category labels, compare revenue/unit contributions and net revenue per unit | A candidate category for a gift-bundle test, with stock/cost checks |
| How large is the fulfilled UK wholesale base? | Distinguish order lines from orders, filter country and delivery status | Delivered-order and unit counts with a defined scope |
| What makes products difficult to discover or choose? | Structured review of navigation, positioning and purchase context | Sales plan connecting product grouping and content to acquisition objectives |

## Run

Python 3.10+, no additional packages. From this directory:

```bash
python3 retail.py
python3 -m unittest discover -s tests -v
```

Outputs are `build/results.json`, `build/categories.csv` and `build/sales_action_plan.md`. A readable [example action plan](examples/sales_action_plan.md) is included for browsing.

## Analysis process

1. **Reconcile money.** Check `gross + discounts + returns = net` and `net + taxes = total`. Discounts and returns are already signed, so they are not deducted twice.
2. **Normalize categories.** Strip whitespace and normalize case. Keep missing categories in an explicit bucket; do not drop legitimate rows just because product titles repeat.
3. **Compare product mix.** Calculate shares from category totals over portfolio totals, rather than averaging row-level percentages.
4. **Evaluate product value.** Divide category net sales by net units and compare with the portfolio's weighted net revenue per unit. Zero/nonpositive unit denominators produce no per-unit estimate.
5. **Define channel scope.** Count unique order IDs, distinguish delivery states and keep national scope explicit. Conflicting statuses/countries/currencies within one order raise an error.
6. **Translate findings.** Nominate a product experiment and channel follow-up, then specify what additional data would establish incremental impact.

```text
category revenue share = category net sales / portfolio net sales
category unit share = category net units / portfolio net units
revenue-per-unit index = category revenue per net unit / portfolio revenue per net unit
```

The product fixture has 9 records, including two case variants for matcha sets and repeated cup titles. The order fixture has 9 lines but only 7 unique orders; 3 UK orders are delivered, containing 23 units. They are deliberately small examples, not the original project's record counts.

## Commercial reasoning

A category with above-average revenue per unit may be worth investigating for gifting or bundled merchandising. That is a product-selection signal, not proof of higher margin, greater demand or promotion effectiveness. Validate costs, stock and demand before committing budget.

Navigation and storytelling are reviewed as possible purchase barriers. The [commercial review framework](commercial_review.md) makes the seven dimensions explicit. Selective wholesale is evaluated as another route to customer reach, with separate fulfillment and brand-fit considerations.

To quantify an intervention later, collect sessions, orders, net revenue, margin, returns and acquisition spend using compatible channel/time definitions. Do not infer conversion or customer acquisition cost from product totals or order counts alone. No live marketing experiment or client implementation is claimed by this edition.

## Validation and data scope

Tests cover category normalization, repeated titles, total-share reconciliation, zero-unit denominators, monetary identities, mixed currencies, unique-order counting and conflicting statuses. Financial totals require a single currency; different-country order counts are not converted into combined revenue. The two demonstration files are not joined because they do not share an order/product key.

Original client files, business contact details, customer information and the full team report are excluded from this public repository.
