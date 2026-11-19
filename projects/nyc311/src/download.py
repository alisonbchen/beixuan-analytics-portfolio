"""Download only four non-identifying NYC Open Data fields. No API key required."""
import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from pipeline import validate_month

ENDPOINT = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
FIELDS = ["unique_key", "created_date", "borough", "complaint_type"]


def download(month, output, max_rows=5000):
    validate_month(month)
    if max_rows < 0:
        raise ValueError("max_rows must be nonnegative")
    year, number = map(int, month.split("-"))
    following = f"{year+1}-01" if number == 12 else f"{year}-{number+1:02}"
    where = f"created_date >= '{month}-01T00:00:00' AND created_date < '{following}-01T00:00:00'"
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".partial")
    count = 0
    exhausted = False
    try:
        with temporary.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            while not max_rows or count < max_rows:
                size = min(10000, max_rows-count) if max_rows else 10000
                params = {"$select": ",".join(FIELDS), "$where": where, "$order": "unique_key ASC", "$limit": size, "$offset": count}
                request = Request(ENDPOINT + "?" + urlencode(params), headers={"User-Agent": "nyc311-portfolio-reproduction/1.0"})
                with urlopen(request, timeout=60) as response:
                    rows = json.load(response)
                if not isinstance(rows, list):
                    raise ValueError("unexpected API response")
                for row in rows:
                    writer.writerow({field: row.get(field, "") for field in FIELDS})
                count += len(rows)
                if len(rows) < size:
                    exhausted = True
                    break
        temporary.replace(output)
    finally:
        if temporary.exists():
            temporary.unlink()
    manifest = {"endpoint": ENDPOINT, "fields": FIELDS, "month": month, "rows": count,
                "requested_cap": max_rows, "full_month_exhausted": exhausted,
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "note": "API data can change during pagination; validate duplicates and reconcile the saved snapshot. A capped extract is not representative of the month."}
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", required=True)
    parser.add_argument("--output", default="build/public_requests.csv")
    parser.add_argument("--max-rows", type=int, default=5000, help="0 requests a complete month; default is a partial extract")
    args = parser.parse_args()
    print(json.dumps(download(args.month, args.output, args.max_rows), indent=2))
