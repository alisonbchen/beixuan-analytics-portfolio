"""A new public implementation of the education-outcomes analysis using synthetic data."""
import argparse
import csv
import json
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent


def create_demo():
    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    con.executescript((BASE / "sql/schema.sql").read_text())
    con.executemany("INSERT INTO programmes VALUES (?,?,?)", [(1, "Education demonstration", "education"), (2, "Employment demonstration", "employment")])
    con.executemany("INSERT INTO beneficiaries VALUES (?,?,?,?)", [
        (i, int(i <= 10 and i != 8), "baseline" if i <= 10 else None, "follow-up" if i <= 10 else None)
        for i in range(1, 21)
    ])
    hours = [10,10,10,4,2,4,8,5,10,3]
    con.executemany("INSERT INTO participation VALUES (?,?,?)", [(i, 1 if i <= 10 else 2, hours[i-1] if i <= 10 else 5) for i in range(1, 21)])
    # Deliberately small, synthetic fixture preserving the illustrative cohort pattern.
    outcomes = [
        (1,1,"Lower secondary",1,1), (2,1,"Lower secondary",1,0),
        (3,1,"Lower secondary",0,1), (4,1,"Upper secondary",1,1),
        (5,1,"Upper secondary",1,1), (6,1,"Upper secondary",1,0),
        (7,1,"Lower secondary",0,0), (8,1,"Upper secondary",1,1),
        (9,1,"Primary",1,1), (10,1,"Lower secondary",0,1),
    ]
    con.executemany("INSERT INTO education_outcomes VALUES (?,?,?,?,?)", outcomes)
    con.executemany("INSERT INTO employment_outcomes VALUES (?,?,?,?,?)", [(i,2,int(i%3!=0),100+5*i,150+5*i) for i in range(11,21)])
    con.executemany("INSERT INTO funding VALUES (?,?,?,?)", [(i,1 if i <= 12 else 2,2020+(i-1)%4,1000+100*i) for i in range(1,25)])
    con.executescript((BASE / "sql/analysis.sql").read_text())
    return con


def results(con):
    result = {}
    for view in ["stage_summary", "exposure_summary", "stage_exposure", "programme_funding"]:
        result[view] = [dict(row) for row in con.execute(f"SELECT * FROM {view} ORDER BY 1,2")]
    count, unique = con.execute("SELECT COUNT(*),COUNT(DISTINCT beneficiary_id) FROM education_cohort").fetchone()
    if count != unique:
        raise ValueError("cohort join multiplied learner rows")
    result["cohort_checks"] = {"rows": count, "unique_learners": unique}
    result["data_kind"] = "synthetic demonstration; not real beneficiaries or programme performance"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="build")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with create_demo() as con:
        result = results(con)
        (out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
        for key, rows in result.items():
            if not isinstance(rows, list) or not rows:
                continue
            with (out / (key + ".csv")).open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
    (out / "findings.md").write_text("""# Education-outcomes demonstration findings

This is a synthetic example, not an assessment of a charity or a deployed intervention.

Nine eligible learners remain after active-education and baseline/follow-up filters.
Lower-secondary maths proficiency is 40% (2/5), versus 100% (3/3) in upper secondary.
High attendance has 60% proficiency (3/5), versus 100% (2/2) for medium attendance.

The cross-tab explains an important comparison problem: all five high-attendance
learners are primary/lower-secondary, while both medium-attendance learners are
upper-secondary. These data cannot isolate the effect of tutoring hours.

Before changing tutoring provision, compare appropriately defined cohorts at the
same education stage, collect baseline attainment and record missing outcomes.
The present sample is too small and lacks overlap for a reliable causal comparison.
No educational improvement or funding saving is claimed.
""")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
