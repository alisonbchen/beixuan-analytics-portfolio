import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from retail import BASE,analyze_products,analyze_orders


class RetailTests(unittest.TestCase):
    def mutate(self, source, change):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        with source.open() as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
        change(rows)
        target=Path(temp.name)/'input.csv'
        with target.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
        return target

    def test_labels_merge_without_dropping_repeated_titles(self):
        r=analyze_products(BASE/'data/synthetic_products.csv')
        matcha=next(x for x in r['categories'] if x['category']=='matcha set')
        cups=next(x for x in r['categories'] if x['category']=='tea cup')
        self.assertEqual((r['product_records'],matcha['records'],cups['records']),(9,2,2))
        self.assertAlmostEqual(sum(x['net_sales_share_pct'] for x in r['categories']),100)

    def test_zero_units_have_no_revenue_per_unit(self):
        r=analyze_products(BASE/'data/synthetic_products.csv')
        zero=next(x for x in r['categories'] if x['category']=='uncategorized')
        self.assertIsNone(zero['revenue_per_net_unit'])

    def test_inconsistent_money_and_mixed_currency_are_rejected(self):
        for edit in [lambda rows:rows[0].update(net_sales='99999'),lambda rows:rows[0].update(currency='EUR')]:
            path=self.mutate(BASE/'data/synthetic_products.csv',edit)
            with self.assertRaises(ValueError):analyze_products(path)

    def test_order_lines_do_not_inflate_order_counts(self):
        r=analyze_orders(BASE/'data/synthetic_orders.csv')
        self.assertEqual((r['order_lines'],r['unique_orders'],r['uk_delivered_orders'],r['uk_delivered_units']),(9,7,3,'23'))

    def test_conflicting_order_status_is_rejected(self):
        path=self.mutate(BASE/'data/synthetic_orders.csv',lambda rows:rows[1].update(status='Cancelled'))
        with self.assertRaises(ValueError):analyze_orders(path)
