PRAGMA foreign_keys = ON;
CREATE TABLE programmes (
  programme_id INTEGER PRIMARY KEY,
  programme_name TEXT NOT NULL,
  domain TEXT NOT NULL CHECK(domain IN ('education','employment'))
);
CREATE TABLE beneficiaries (
  beneficiary_id INTEGER PRIMARY KEY,
  active_education INTEGER NOT NULL CHECK(active_education IN (0,1)),
  education_before TEXT,
  education_after TEXT
);
CREATE TABLE participation (
  beneficiary_id INTEGER NOT NULL REFERENCES beneficiaries,
  programme_id INTEGER NOT NULL REFERENCES programmes,
  hours_per_week REAL CHECK(hours_per_week IS NULL OR hours_per_week >= 0),
  PRIMARY KEY(beneficiary_id, programme_id)
);
CREATE TABLE education_outcomes (
  beneficiary_id INTEGER NOT NULL,
  programme_id INTEGER NOT NULL,
  education_stage TEXT NOT NULL,
  math_proficient INTEGER CHECK(math_proficient IN (0,1)),
  reading_proficient INTEGER CHECK(reading_proficient IN (0,1)),
  PRIMARY KEY(beneficiary_id,programme_id),
  FOREIGN KEY(beneficiary_id,programme_id) REFERENCES participation
);
CREATE TABLE employment_outcomes (
  beneficiary_id INTEGER NOT NULL,
  programme_id INTEGER NOT NULL,
  employed_after INTEGER NOT NULL CHECK(employed_after IN (0,1)),
  weekly_income_before REAL NOT NULL CHECK(weekly_income_before >= 0),
  weekly_income_after REAL NOT NULL CHECK(weekly_income_after >= 0),
  PRIMARY KEY(beneficiary_id,programme_id),
  FOREIGN KEY(beneficiary_id,programme_id) REFERENCES participation
);
CREATE TABLE funding (
  funding_id INTEGER PRIMARY KEY,
  programme_id INTEGER NOT NULL REFERENCES programmes,
  funding_year INTEGER NOT NULL,
  amount_gbp REAL NOT NULL CHECK(amount_gbp >= 0)
);
