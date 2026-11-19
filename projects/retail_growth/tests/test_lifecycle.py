import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from lifecycle import BASE,read_csv,funnel,cohorts


class LifecycleTests(unittest.TestCase):
    def test_session_and_conditional_denominators_differ(self):
        r=funnel(read_csv(BASE/'data/synthetic_funnel.csv'))
        self.assertEqual(r['total_sessions'],10000)
        self.assertEqual(r['purchase_session_conversion_pct'],1)
        self.assertAlmostEqual(r['cart_to_checkout_pct'],310/550*100)
        self.assertAlmostEqual(r['cart_to_purchase_loss_pct'],450/550*100)

    def test_non_nested_counts_are_rejected(self):
        r=read_csv(BASE/'data/synthetic_funnel.csv');r[0]['purchase_sessions']='10000'
        with self.assertRaises(ValueError):funnel(r)

    def test_empty_channel_conversion_is_not_zero(self):
        r=funnel([{'channel':'Empty','sessions':'0','add_to_cart_sessions':'0','checkout_sessions':'0','purchase_sessions':'0'}])
        self.assertIsNone(r['purchase_session_conversion_pct'])

    def test_maturity_and_weighted_cohort_denominators(self):
        r=cohorts(read_csv(BASE/'data/synthetic_cohorts.csv'))
        self.assertEqual((r[0]['eligible_customers'],r[0]['returning_customers']),(300,22))
        self.assertAlmostEqual(r[0]['repeat_purchase_in_month_pct'],22/300*100)
        self.assertEqual((r[1]['eligible_customers'],r[1]['repeat_purchase_in_month_pct']),(100,4))

    def test_duplicate_cohorts_and_changed_denominators_are_rejected(self):
        rows=read_csv(BASE/'data/synthetic_cohorts.csv')
        with self.assertRaises(ValueError):cohorts(rows+[copy.deepcopy(rows[0])])
        rows[1]['initial_customers']='99'
        with self.assertRaises(ValueError):cohorts(rows)
