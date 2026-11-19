"""Compare reported financial metrics, retaining source and accounting basis."""
import argparse
import csv
import json
import sqlite3
from pathlib import Path

BASE=Path(__file__).resolve().parent


def analyze(rows):
    keys=set()
    for row in rows:
        key=(row['company'],row['fiscal_year'])
        if key in keys:raise ValueError('duplicate company/year')
        keys.add(key)
        if row['net_revenue_usd_m'] <= 0:raise ValueError('revenue must be positive')
        if not row['source'].startswith('https://www.sec.gov/Archives/edgar/'):
            raise ValueError('each observation needs an SEC filing source')
    with sqlite3.connect(':memory:') as con:
        con.execute('CREATE TABLE financials (company TEXT, fiscal_year INTEGER, year_end TEXT, revenue REAL, operating_income REAL, adjusted_opex REAL, source TEXT, PRIMARY KEY(company,fiscal_year))')
        con.executemany('INSERT INTO financials VALUES(?,?,?,?,?,?,?)',[(r['company'],r['fiscal_year'],r['year_end'],r['net_revenue_usd_m'],r['gaap_operating_income_usd_m'],r['disclosed_adjusted_operating_expenses_usd_m'],r['source']) for r in rows])
        cur=con.execute((BASE/'analysis.sql').read_text())
        columns=[d[0] for d in cur.description]
        result=[dict(zip(columns,row)) for row in cur.fetchall()]
    # LAG must refer to a consecutive fiscal year, not an arbitrary earlier observation.
    previous={}
    for r in result:
        if r['company'] not in previous or r['fiscal_year'] != previous[r['company']]+1:
            for key in ['revenue_growth_pct','gaap_margin_change_pp','adjusted_margin_change_pp']:r[key]=None
        previous[r['company']]=r['fiscal_year']
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=BASE/'build');args=p.parse_args()
    source=json.loads((BASE/'data/financials.json').read_text())
    result=analyze(source);args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'metrics.json').write_text(json.dumps(result,indent=2)+'\n')
    with (args.output/'metrics.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
    lines=['# Payment-network financial comparison','', 'USD millions. Fiscal years differ between companies. Derived adjusted margins are calculated from disclosed adjusted operating expenses and are not a harmonized accounting standard.','', '| Company | FY | Revenue growth | GAAP margin | GAAP change | Derived adjusted change |','|---|---:|---:|---:|---:|---:|']
    for r in result:
        if r['fiscal_year']==2025:
            lines.append(f"| {r['company']} | 2025 | {r['revenue_growth_pct']:.2f}% | {r['gaap_margin_pct']:.2f}% | {r['gaap_margin_change_pp']:.2f} pp | {r['adjusted_margin_change_pp']:.2f} pp |")
    lines+=['','Interpretation: compare reported and adjusted bases before treating changes in profitability as operational deterioration or improvement. Review litigation and other excluded items in each filing. This comparison alone does not establish valuation or investment suitability.']
    (args.output/'comparison.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'company_year_observations':len(result),'companies':len({r['company'] for r in result})},indent=2))


if __name__=='__main__':main()
