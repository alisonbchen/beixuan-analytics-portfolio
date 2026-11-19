import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from download import download


class DownloadTests(unittest.TestCase):
    def test_only_four_fields_are_saved_and_cap_is_disclosed(self):
        source = [{"unique_key":"1", "created_date":"2025-03-01T00:00:00",
                   "borough":"MANHATTAN", "complaint_type":"NOISE", "incident_address":"must not be retained"}]
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "sample.csv"
            with patch("download.urlopen", return_value=io.BytesIO(json.dumps(source).encode())):
                manifest = download("2025-03", target, max_rows=1)
            with target.open() as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(set(rows[0]), {"unique_key","created_date","borough","complaint_type"})
            self.assertNotIn("must not be retained", target.read_text())
            self.assertFalse(manifest["full_month_exhausted"])
            self.assertTrue(target.with_suffix(".manifest.json").is_file())

    def test_invalid_month_is_rejected_before_network_request(self):
        with patch("download.urlopen") as fetch:
            with self.assertRaises(ValueError):
                download("2025-13", "unused.csv")
            fetch.assert_not_called()
