import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research import BASE,analyze


class FinanceTests(unittest.TestCase):
    def setUp(self):self.rows=json.loads((BASE/'data/financials.json').read_text())

    def test_first_year_has_no_growth_baseline(self):
        first=[r for r in analyze(self.rows) if r['fiscal_year']==2023]
        self.assertTrue(all(r['revenue_growth_pct'] is None for r in first))

    def test_growth_and_percentage_point_change(self):
        visa=next(r for r in analyze(self.rows) if r['company']=='Visa' and r['fiscal_year']==2025)
        self.assertAlmostEqual(visa['revenue_growth_pct'],(40000/35926-1)*100)
        self.assertAlmostEqual(visa['gaap_margin_change_pp'],23994/40000*100-23595/35926*100)
        self.assertLess(visa['gaap_margin_change_pp'],-5)
        self.assertGreater(visa['adjusted_margin_change_pp'],0)

    def test_duplicate_source_key_is_rejected(self):
        with self.assertRaises(ValueError):analyze(self.rows+[copy.deepcopy(self.rows[0])])

    def test_nonconsecutive_year_is_not_year_on_year(self):
        rows=[r for r in self.rows if r['fiscal_year']!=2024]
        self.assertTrue(all(r['revenue_growth_pct'] is None for r in analyze(rows)))
