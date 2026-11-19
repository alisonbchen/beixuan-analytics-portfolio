# Project process and review guide

## Business question before implementation

For each project, define the decision, unit of analysis and a result that can be verified. NYC 311 concerns concentrations of reported demand; the education project concerns whether cohort comparisons can support a provision decision. Neither substitutes an implementation count for a realized business impact.

## Build and validate

1. Define the minimum data fields and avoid publishing private source files.
2. Make data grain explicit: request key for NYC; beneficiary/programme for education.
3. Preserve exclusions and unknown values rather than silently dropping them.
4. Reconcile aggregates to eligible inputs and check join multiplication.
5. Separate measured findings, intended uses and untested extensions.
6. Provide one-command offline runs and targeted tests.

## Public release scope

The repository includes new implementation code, SQL, English documentation, synthetic fixtures and an offline test workflow. It excludes original team submissions, private source exports, credentials, personal contact information and resume drafts. 

Original group materials are not redistributed.

## Suggested interview walkthrough

- NYC: load the fixture, inspect the quality buckets, rerun the load, then show why the top-one issue's share still uses the full borough/month denominator.
- Education: explain why the high-attendance group's lower rate is initially surprising, show the stage cross-tab, then explain what additional data would be needed before changing tutoring provision.

## CI

The workflow runs the same offline scripts on Python 3.10 and 3.12. Local success does not imply a hosted workflow has already run.

Action references: [checkout](https://github.com/actions/checkout) and [setup-python](https://github.com/actions/setup-python).
