import csv
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pipeline import build_snapshot, top_issues, borough_totals
from app import handler_for


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.csv = self.base / "requests.csv"
        self.db = self.base / "snapshot.sqlite"
        self.rows = [
            ["1", "2025-03-01T00:00:00", "Manhattan", "Heat/Hot Water"],
            ["2", "2025-03-02T00:00:00", "MANHATTAN", "Heat/Hot Water"],
            ["3", "2025-03-03T00:00:00", "MANHATTAN", "Noise"],
            ["4", "2025-03-03T00:00:00", "UNSPECIFIED", "Noise"],
            ["1", "2025-03-01T00:00:00", "Manhattan", "Heat/Hot Water"],
            ["5", "bad-date", "QUEENS", "Noise"],
            ["6", "2025-03-03T00:00:00", "BROOKLYN", "Parking"],
        ]
        self.write_rows()

    def write_rows(self):
        with self.csv.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["unique_key", "created_date", "borough", "complaint_type"])
            writer.writerows(self.rows)

    def test_quality_buckets_and_summary_reconcile(self):
        report = build_snapshot([self.csv], self.db)
        self.assertEqual((report["raw_rows"], report["accepted_rows"], report["duplicate_rows"], report["rejected_rows"]), (7, 5, 1, 1))
        self.assertEqual(report["unspecified_borough_rows"], 1)
        with sqlite3.connect(self.db) as c:
            self.assertEqual(c.execute("SELECT SUM(requests) FROM monthly_summary").fetchone()[0], 5)
        self.assertEqual(sum(x["requests"] for x in borough_totals(self.db, "2025-03")), 4)

    def test_rerun_does_not_double_count(self):
        build_snapshot([self.csv], self.db)
        build_snapshot([self.csv], self.db)
        self.assertEqual(top_issues(self.db, "2025-03", "MANHATTAN")["total_requests"], 3)

    def test_top_one_share_uses_all_categories(self):
        build_snapshot([self.csv], self.db)
        result = top_issues(self.db, "2025-03", "MANHATTAN", 1)
        self.assertEqual(result["total_requests"], 3)
        self.assertAlmostEqual(result["issues"][0]["share_pct"], 66.6667)
        self.assertAlmostEqual(result["issues"][0]["daily_average"], 2/31, places=4)

    def test_invalid_input_does_not_replace_existing_snapshot(self):
        build_snapshot([self.csv], self.db)
        self.csv.write_text("wrong,columns\n1,2\n")
        with self.assertRaises(ValueError):
            build_snapshot([self.csv], self.db)
        self.assertEqual(top_issues(self.db, "2025-03", "MANHATTAN")["total_requests"], 3)

    def test_missing_month_and_injection_are_rejected(self):
        build_snapshot([self.csv], self.db)
        for month in ["", "2025-99", "2025-03' OR 1=1"]:
            with self.assertRaises(ValueError):
                borough_totals(self.db, month)
        with self.assertRaises(ValueError):
            top_issues(self.db, "2025-03", "MANHATTAN' OR 1=1")
        self.assertEqual(top_issues(self.db, "2025-04", "MANHATTAN")["issues"], [])

    def route(self, path):
        handler = object.__new__(handler_for(self.db))
        handler.path = path
        handler.wfile = io.BytesIO()
        status = []
        handler.send_response = status.append
        handler.send_header = lambda *args: None
        handler.end_headers = lambda: None
        handler.do_GET()
        return status[0], handler.wfile.getvalue()

    def test_api_routes_and_validation(self):
        build_snapshot([self.csv], self.db)
        status, body = self.route("/api/top-issues?month=2025-03&borough=MANHATTAN")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["total_requests"], 3)
        self.assertEqual(self.route("/api/boroughs?month=bad")[0], 400)
        self.assertEqual(self.route("/missing")[0], 404)
        self.assertEqual(self.route("/")[0], 200)


if __name__ == "__main__":
    unittest.main()
