# Customer lifecycle diagnostic — synthetic demonstration

The counts below are generated examples. They demonstrate methods used in the wider consultancy problem; they do not reproduce client tables or client performance.

## Channel and purchase funnel

| Channel | Sessions | Purchase sessions | Conversion |
|---|---:|---:|---:|
| Search | 5000 | 70 | 1.40% |
| Social | 4000 | 12 | 0.30% |
| Direct | 1000 | 18 | 1.80% |

Overall conversion: 1.00%. Cart-to-purchase loss: 81.82% (450 cart sessions without purchase).

Channel traffic volume and purchase intent differ. Investigate stage loss before assuming more visits will produce proportionate sales. The loss count is not a forecast of recoverable orders.

## Repeat-purchase cohorts

| Month after first purchase | Mature cohorts | Eligible customers | Returning customers | Rate |
|---|---:|---:|---:|---:|
| 1 | 2 | 300 | 22 | 7.33% |
| 2 | 1 | 100 | 4 | 4.00% |

The rate measures a repeat purchase during that month, not lifetime retention. Later horizons exclude cohorts without enough follow-up; they are not filled with zero. Changing cohort composition limits direct horizon comparisons.

## Decision use

Use the findings to formulate checkout and post-purchase hypotheses, then assess interventions with compatible session/cohort definitions, an observation window and commercial guardrails. The complete project strategy is documented in PROJECT_REPORT.md and ACTION_PLAN.md.
