import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from education import create_demo, results


class EducationTests(unittest.TestCase):
    def setUp(self):
        self.con = create_demo()
        self.addCleanup(self.con.close)

    def test_cohort_is_not_multiplied_and_rates_reproduce(self):
        result = results(self.con)
        self.assertEqual(result["cohort_checks"], {"rows":9,"unique_learners":9})
        rates = {r["exposure"]:r["math_proficiency_pct"] for r in result["exposure_summary"]}
        self.assertEqual(rates, {"High":60.0,"Low":50.0,"Medium":100.0})
        self.assertEqual(len(self.con.execute("PRAGMA foreign_key_check").fetchall()), 0)

    def test_duplicate_profile_and_orphan_are_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.con.execute("INSERT INTO beneficiaries VALUES (1,1,'a','b')")
        with self.assertRaises(sqlite3.IntegrityError):
            self.con.execute("INSERT INTO participation VALUES (999,1,4)")

    def test_cross_programme_participation_does_not_amplify_education(self):
        self.con.execute("INSERT INTO participation VALUES (1,2,5)")
        self.assertEqual(results(self.con)["cohort_checks"]["rows"], 9)

    def test_unknown_hours_do_not_become_high_attendance(self):
        self.con.execute("UPDATE participation SET hours_per_week=NULL WHERE beneficiary_id=1")
        row = self.con.execute("SELECT exposure FROM education_cohort WHERE beneficiary_id=1").fetchone()
        self.assertEqual(row[0], "Unknown")

    def test_missing_scores_are_not_counted_as_failures(self):
        self.con.execute("UPDATE education_outcomes SET math_proficient=NULL WHERE beneficiary_id=1")
        row = self.con.execute("SELECT * FROM stage_summary WHERE education_stage='Lower secondary'").fetchone()
        self.assertEqual((row["learners"],row["math_observed"],row["math_proficiency_pct"]), (5,4,25.0))

    def test_stage_and_attendance_lack_overlap(self):
        result = results(self.con)
        medium = [r for r in result["stage_exposure"] if r["exposure"]=="Medium"]
        self.assertEqual(medium, [{"education_stage":"Upper secondary","exposure":"Medium","learners":2}])

    def test_funding_totals_are_not_multiplied_by_participant_count(self):
        raw = self.con.execute("SELECT SUM(amount_gbp) FROM funding").fetchone()[0]
        summary = self.con.execute("SELECT SUM(funding_gbp) FROM programme_funding").fetchone()[0]
        self.assertEqual(raw, summary)


if __name__ == "__main__":
    unittest.main()
