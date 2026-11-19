"""Build an auditable local serving snapshot from four non-identifying 311 fields."""
import argparse
import calendar
import csv
import hashlib
import json
import re
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BOROUGHS = {"BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND"}


def validate_month(month):
    if not re.fullmatch(r"\d{4}-\d{2}", month):
        raise ValueError("month must be YYYY-MM")
    datetime.strptime(month, "%Y-%m")
    return month


def build_snapshot(paths, database):
    """Replace the ENTIRE local snapshot atomically; include all desired input months."""
    accepted, seen, reasons, sources = [], set(), Counter(), []
    raw = duplicates = 0
    for filename in paths:
        path = Path(filename)
        sources.append({"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            required = {"unique_key", "created_date", "borough", "complaint_type"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError("CSV must contain unique_key, created_date, borough, complaint_type")
            for row in reader:
                raw += 1
                key = (row["unique_key"] or "").strip()
                issue = (row["complaint_type"] or "").strip().upper()
                if not key or not issue:
                    reasons["missing_key_or_issue"] += 1
                    continue
                try:
                    created = datetime.fromisoformat(row["created_date"].strip().replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    reasons["invalid_created_date"] += 1
                    continue
                if key in seen:
                    duplicates += 1
                    continue
                seen.add(key)
                borough = (row["borough"] or "").strip().upper()
                if borough not in BOROUGHS:
                    borough = "UNSPECIFIED"
                accepted.append((key, created.strftime("%Y-%m"), borough, issue))
    database = Path(database)
    database.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "raw_rows": raw, "accepted_rows": len(accepted),
        "duplicate_rows": duplicates, "rejected_rows": sum(reasons.values()),
        "rejection_reasons": dict(reasons),
        "unspecified_borough_rows": sum(r[2] == "UNSPECIFIED" for r in accepted),
        "sources": sources, "built_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    assert raw == len(accepted) + duplicates + sum(reasons.values())
    with sqlite3.connect(database) as con:
        con.execute("CREATE TABLE IF NOT EXISTS requests (unique_key TEXT PRIMARY KEY, month TEXT NOT NULL, borough TEXT NOT NULL, issue TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS monthly_summary (month TEXT, borough TEXT, issue TEXT, requests INTEGER NOT NULL, PRIMARY KEY(month,borough,issue))")
        con.execute("CREATE TABLE IF NOT EXISTS run_metadata (report_json TEXT NOT NULL)")
        # These writes share one transaction. An insertion failure rolls back the replacement.
        con.execute("DELETE FROM requests")
        con.execute("DELETE FROM monthly_summary")
        con.execute("DELETE FROM run_metadata")
        con.executemany("INSERT INTO requests VALUES (?,?,?,?)", accepted)
        con.execute("INSERT INTO monthly_summary SELECT month,borough,issue,COUNT(*) FROM requests GROUP BY month,borough,issue")
        summary_count, summary_total = con.execute("SELECT COUNT(*), COALESCE(SUM(requests),0) FROM monthly_summary").fetchone()
        if summary_total != len(accepted):
            raise ValueError("summary reconciliation failed")
        report["summary_rows"] = summary_count
        report["summary_row_reduction_pct"] = round(100 * (1 - summary_count / len(accepted)), 4) if accepted else None
        con.execute("INSERT INTO run_metadata VALUES (?)", (json.dumps(report),))
    return report


def borough_totals(database, month):
    validate_month(month)
    with sqlite3.connect(database) as con:
        rows = con.execute("SELECT borough,SUM(requests) FROM monthly_summary WHERE month=? AND borough!='UNSPECIFIED' GROUP BY borough ORDER BY SUM(requests) DESC,borough", (month,)).fetchall()
    return [{"borough": b, "requests": n} for b, n in rows]


def top_issues(database, month, borough, limit=3):
    validate_month(month)
    borough = borough.strip().upper()
    if borough not in BOROUGHS or not 1 <= limit <= 20:
        raise ValueError("choose a NYC borough and limit between 1 and 20")
    with sqlite3.connect(database) as con:
        total = con.execute("SELECT COALESCE(SUM(requests),0) FROM monthly_summary WHERE month=? AND borough=?", (month, borough)).fetchone()[0]
        rows = con.execute("SELECT issue,requests FROM monthly_summary WHERE month=? AND borough=? ORDER BY requests DESC,issue LIMIT ?", (month, borough, limit)).fetchall()
    year, month_number = map(int, month.split("-"))
    days = calendar.monthrange(year, month_number)[1]
    return {"month": month, "borough": borough, "total_requests": total, "issues": [
        {"issue": issue, "requests": count, "share_pct": round(100 * count / total, 4), "daily_average": round(count / days, 4)}
        for issue, count in rows
    ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", nargs="+", required=True)
    parser.add_argument("--db", default="build/nyc311.sqlite")
    parser.add_argument("--report", default="build/quality_report.json")
    args = parser.parse_args()
    report = build_snapshot(args.input, args.db)
    path = Path(args.report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
