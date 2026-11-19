"""Channel, funnel and cohort methods using generated public demonstration data."""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
STAGES = ['sessions','add_to_cart_sessions','checkout_sessions','purchase_sessions']


def percent(numerator, denominator):
    return 100*numerator/denominator if denominator else None


def funnel(rows):
    result=[]
    totals={key:0 for key in STAGES}
    channels=set()
    for row in rows:
        channel=row['channel'].strip()
        if not channel or channel in channels:
            raise ValueError('each channel must occur once in this fixed-window fixture')
        channels.add(channel)
        values=[int(row[k]) for k in STAGES]
        if any(v<0 for v in values) or values!=sorted(values,reverse=True):
            raise ValueError('demo stages must be nonnegative nested session counts')
        values=dict(zip(STAGES,values))
        for key in STAGES:totals[key]+=values[key]
        result.append({'channel':channel,**values,
            'purchase_session_conversion_pct':percent(values['purchase_sessions'],values['sessions'])})
    s,cart,checkout,purchase=[totals[k] for k in STAGES]
    return {'channels':result,'total_sessions':s,'add_to_cart_pct':percent(cart,s),
        'purchase_session_conversion_pct':percent(purchase,s),
        'cart_to_checkout_pct':percent(checkout,cart),
        'checkout_to_purchase_pct':percent(purchase,checkout),
        'cart_to_purchase_loss_pct':percent(cart-purchase,cart),
        'cart_sessions_without_purchase':cart-purchase}


def cohorts(rows):
    seen=set();sizes={};totals=defaultdict(lambda:{'eligible_cohorts':0,'eligible_customers':0,'returning_customers':0})
    for row in rows:
        key=(row['cohort'],int(row['months_since_first_purchase']))
        size=int(row['initial_customers'])
        if key in seen or key[1]<1 or size<=0:
            raise ValueError('invalid or duplicate cohort/horizon')
        seen.add(key)
        if row['cohort'] in sizes and sizes[row['cohort']]!=size:
            raise ValueError('cohort denominator must remain consistent')
        sizes[row['cohort']]=size
        if row['mature'] not in {'0','1'}:
            raise ValueError('mature must be 0 or 1')
        if row['mature']=='0':
            if row['returning_customers'].strip():raise ValueError('unobserved horizon must not contain a return count')
            continue
        returning=int(row['returning_customers'])
        if not 0<=returning<=size:raise ValueError('returning count outside cohort bounds')
        group=totals[key[1]]
        group['eligible_cohorts']+=1;group['eligible_customers']+=size;group['returning_customers']+=returning
    return [{'months_since_first_purchase':h,**g,
             'repeat_purchase_in_month_pct':percent(g['returning_customers'],g['eligible_customers'])}
            for h,g in sorted(totals.items())]


def read_csv(path):
    with Path(path).open(newline='') as f:return list(csv.DictReader(f))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=BASE/'build');args=p.parse_args()
    f=funnel(read_csv(BASE/'data/synthetic_funnel.csv'))
    c=cohorts(read_csv(BASE/'data/synthetic_cohorts.csv'))
    result={'data_kind':'new synthetic demonstration; not client metrics','funnel':f,'cohort_horizons':c}
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'lifecycle_results.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# Customer lifecycle diagnostic — synthetic demonstration','',
           'The counts below are generated examples. They demonstrate methods used in the wider consultancy problem; they do not reproduce client tables or client performance.','',
           '## Channel and purchase funnel','',
           '| Channel | Sessions | Purchase sessions | Conversion |','|---|---:|---:|---:|']
    for r in f['channels']:
        rate=f"{r['purchase_session_conversion_pct']:.2f}%" if r['purchase_session_conversion_pct'] is not None else 'N/A'
        lines.append(f"| {r['channel']} | {r['sessions']} | {r['purchase_sessions']} | {rate} |")
    lines += ['',f"Overall conversion: {f['purchase_session_conversion_pct']:.2f}%. Cart-to-purchase loss: {f['cart_to_purchase_loss_pct']:.2f}% ({f['cart_sessions_without_purchase']} cart sessions without purchase).",'',
              'Channel traffic volume and purchase intent differ. Investigate stage loss before assuming more visits will produce proportionate sales. The loss count is not a forecast of recoverable orders.','',
              '## Repeat-purchase cohorts','',
              '| Month after first purchase | Mature cohorts | Eligible customers | Returning customers | Rate |','|---|---:|---:|---:|---:|']
    for r in c:lines.append(f"| {r['months_since_first_purchase']} | {r['eligible_cohorts']} | {r['eligible_customers']} | {r['returning_customers']} | {r['repeat_purchase_in_month_pct']:.2f}% |")
    lines+=['','The rate measures a repeat purchase during that month, not lifetime retention. Later horizons exclude cohorts without enough follow-up; they are not filled with zero. Changing cohort composition limits direct horizon comparisons.','',
            '## Decision use','',
            'Use the findings to formulate checkout and post-purchase hypotheses, then assess interventions with compatible session/cohort definitions, an observation window and commercial guardrails. The complete project strategy is documented in PROJECT_REPORT.md and ACTION_PLAN.md.']
    (args.output/'customer_lifecycle_diagnostic.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'synthetic_sessions':f['total_sessions'],'observed_cohort_horizons':len(c)},indent=2))


if __name__=='__main__':main()
