-- DATABASE SCHEMA DESIGN
-- Table: patients
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Patient Info
    name TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- AI Results
    disease_prob TEXT,    -- e.g. "85.2%"
    risk_label TEXT,      -- "High Risk" / "Low Risk"

    -- Vitals (Inputs) (snake_case names)
    age INTEGER,
    gender INTEGER,       -- 1=Male, 0=Female
    total_bilirubin REAL,
    direct_bilirubin REAL,
    alkaline_phosphotase INTEGER,
    alamine_aminotransferase INTEGER,
    aspartate_aminotransferase INTEGER,
    total_protiens REAL,
    albumin REAL,
    ag_ratio REAL
);