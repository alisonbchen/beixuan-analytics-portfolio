-- Each person contributes at most one outcome to the selected programme.
-- Explicit programme joins prevent cross-programme amplification.
CREATE VIEW education_cohort AS
SELECT b.beneficiary_id, e.education_stage, e.math_proficient, e.reading_proficient,
       CASE WHEN p.hours_per_week IS NULL THEN 'Unknown'
            WHEN p.hours_per_week <= 3 THEN 'Low'
            WHEN p.hours_per_week <= 6 THEN 'Medium' ELSE 'High' END AS exposure
FROM beneficiaries b
JOIN participation p ON p.beneficiary_id=b.beneficiary_id
JOIN education_outcomes e ON e.beneficiary_id=p.beneficiary_id AND e.programme_id=p.programme_id
WHERE p.programme_id=1 AND b.active_education=1
  AND b.education_before IS NOT NULL AND b.education_after IS NOT NULL;

CREATE VIEW stage_summary AS
SELECT education_stage, COUNT(*) AS learners,
       COUNT(math_proficient) AS math_observed,
       ROUND(100.0*AVG(math_proficient),2) AS math_proficiency_pct,
       COUNT(reading_proficient) AS reading_observed,
       ROUND(100.0*AVG(reading_proficient),2) AS reading_proficiency_pct
FROM education_cohort GROUP BY education_stage;

CREATE VIEW exposure_summary AS
SELECT exposure,COUNT(*) AS learners,
       COUNT(math_proficient) AS math_observed,
       ROUND(100.0*AVG(math_proficient),2) AS math_proficiency_pct
FROM education_cohort GROUP BY exposure;

CREATE VIEW stage_exposure AS
SELECT education_stage,exposure,COUNT(*) AS learners
FROM education_cohort GROUP BY education_stage,exposure;

-- Aggregate funding separately; joining funding directly to participation would
-- multiply monetary amounts by the number of participants.
CREATE VIEW programme_funding AS
SELECT p.programme_name,COUNT(f.funding_id) AS funding_records,SUM(f.amount_gbp) AS funding_gbp
FROM programmes p LEFT JOIN funding f ON p.programme_id=f.programme_id
GROUP BY p.programme_id,p.programme_name;
