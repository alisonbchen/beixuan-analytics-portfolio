"""Public retail-growth demonstration: synthetic products, order scope and action plan."""
import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE = Path(__file__).resolve().parent


def ratio(numerator, denominator, multiplier=1):
    return float(numerator / denominator * multiplier) if denominator > 0 else None


def analyze_products(path):
    groups = defaultdict(lambda: {"records":0, "net_units":Decimal(0), "net_sales":Decimal(0)})
    total_units = total_sales = Decimal(0)
    currencies, raw_types, count = set(), set(), 0
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            count += 1
            try:
                gross, discounts, returns, net, taxes, total, units = [Decimal(row[k]) for k in
                    ["gross_sales","discounts","returns","net_sales","taxes","total_sales","net_units"]]
            except (InvalidOperation, KeyError) as error:
                raise ValueError("missing or nonnumeric sales field") from error
            if not all(x.is_finite() for x in [gross, discounts, returns, net, taxes, total, units]):
                raise ValueError("sales fields must be finite")
            if abs(gross+discounts+returns-net) > Decimal('0.005') or abs(net+taxes-total) > Decimal('0.005'):
                raise ValueError(f"sales reconciliation failed at row {count}")
            currency = row.get("currency", "").strip().upper()
            if not currency:
                raise ValueError("currency is required for comparable revenue aggregation")
            currencies.add(currency)
            raw_types.add(row.get("product_type", ""))
            category = row.get("product_type", "").strip().casefold() or "uncategorized"
            group = groups[category]
            group["records"] += 1
            group["net_units"] += units
            group["net_sales"] += net
            total_units += units
            total_sales += net
    if len(currencies) != 1:
        raise ValueError("use a single currency or an explicitly documented FX conversion first")
    average = total_sales/total_units if total_units > 0 else None
    categories = []
    for category, values in sorted(groups.items(), key=lambda x:(-x[1]["net_sales"],x[0])):
        per_unit = values["net_sales"]/values["net_units"] if values["net_units"] > 0 else None
        categories.append({"category":category,"records":values["records"],
            "net_units":str(values["net_units"]),"net_sales":str(values["net_sales"]),
            "net_sales_share_pct":ratio(values["net_sales"],total_sales,100),
            "net_unit_share_pct":ratio(values["net_units"],total_units,100),
            "revenue_per_net_unit":float(per_unit) if per_unit is not None else None,
            "revenue_per_unit_index":float(per_unit/average) if per_unit is not None and average is not None and average > 0 else None})
    return {"data_kind":"synthetic retail demonstration", "currency":next(iter(currencies)),
            "product_records":count,"raw_type_values":len(raw_types),"normalized_categories":len(groups),
            "net_sales":str(total_sales),"net_units":str(total_units),"categories":categories}


def analyze_orders(path):
    orders, lines = {}, 0
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            lines += 1
            key = row["order_id"].strip()
            context = (row["country"].strip().casefold(),row["status"].strip().casefold(),row["currency"].strip().upper())
            if not key or not all(context):
                raise ValueError("order ID, country, status and currency are required")
            units = Decimal(row["units"])
            if not units.is_finite() or units < 0:
                raise ValueError("order units must be finite and nonnegative")
            if key in orders and orders[key]["context"] != context:
                raise ValueError("one order has conflicting country, status or currency")
            entry = orders.setdefault(key,{"context":context,"units":Decimal(0)})
            entry["units"] += units
    uk = [entry for entry in orders.values() if entry["context"][0] == "united kingdom"]
    delivered = [entry for entry in uk if entry["context"][1] == "delivered"]
    return {"data_kind":"synthetic wholesale demonstration", "order_lines":lines,
            "unique_orders":len(orders),"uk_orders_all_statuses":len(uk),
            "uk_delivered_orders":len(delivered),"uk_delivered_units":str(sum((e["units"] for e in delivered),Decimal(0))),
            "note":"No monetary totals are combined across currencies; order counts are not conversion rates."}


def write_plan(product, orders, out):
    matcha = next((r for r in product["categories"] if r["category"]=="matcha set"),None)
    finding = (f"Matcha sets produce {matcha['revenue_per_unit_index']:.2f} times the portfolio-average net revenue per unit."
               if matcha and matcha["revenue_per_unit_index"] is not None else "No positive-unit matcha-set comparison is available.")
    (out/'sales_action_plan.md').write_text(f"""# Retail growth action plan — synthetic demonstration

## Decision
Choose which products and channels to investigate before increasing marketing spend.

## Product focus
{finding} Compare this with revenue share and unit share in categories.csv.
Use the finding to nominate a gift-bundle experiment; confirm stock availability,
costs and customer demand before giving it priority. Revenue per unit is not margin
or average order value. The finding does not by itself establish incremental sales.

## Channel focus
The fixture contains {orders['uk_delivered_orders']} delivered UK wholesale orders
and {orders['uk_delivered_units']} delivered units. Keep cancelled and shipped
orders outside fulfilled-sales counts. Assess suitable stockists separately from
the product export; the two files have no shared order/product key for a causal join.

## Purchase barriers and next actions
The consultancy framework examines product discovery and brand communication.
Review navigation, gift grouping and product-use content before paying for more traffic.
Treat selective wholesale as a separate acquisition route with operational capacity checks.

## Measurement plan for a future pilot
Define one hypothesis and intervention at a time. Capture orders, sessions, units,
net sales, contribution margin and channel acquisition costs over a pre-specified period.
Compare eligible control/treatment audiences if feasible and track guardrails such as
returns and stock-outs. No experiment has been run by this demonstration and no lift is claimed.
""")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--products",type=Path,default=BASE/'data/synthetic_products.csv')
    parser.add_argument("--orders",type=Path,default=BASE/'data/synthetic_orders.csv')
    parser.add_argument("--output",type=Path,default=BASE/'build')
    args=parser.parse_args()
    products,orders=analyze_products(args.products),analyze_orders(args.orders)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'results.json').write_text(json.dumps({"products":products,"orders":orders},indent=2)+'\n')
    with (args.output/'categories.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(products['categories'][0]))
        writer.writeheader();writer.writerows(products['categories'])
    write_plan(products,orders,args.output)
    print(json.dumps({"product_records":products['product_records'],"categories":products['normalized_categories'],"uk_delivered_orders":orders['uk_delivered_orders']},indent=2))


if __name__ == '__main__':
    main()
