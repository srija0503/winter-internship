import sqlite3
import os
from typing import Dict, Any
from .config import DB_PATH

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "..", "db", "database_schema.sql")

def create_db(db_path: str = None):
    db_path = db_path or DB_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    schema_path = os.path.abspath(SCHEMA_FILE)
    with open(schema_path, "r") as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"Database created/verified at: {db_path}")
    return db_path

def insert_patient(record: Dict[str, Any], db_path: str = None) -> int:
    """
    Insert a patient record. record keys should be snake_case matching DB columns.
    Returns inserted row id.
    """
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Allowed columns (reduce risk)
    cols = ["name", "disease_prob", "risk_label", "age", "gender",
            "total_bilirubin", "direct_bilirubin", "alkaline_phosphotase",
            "alamine_aminotransferase", "aspartate_aminotransferase",
            "total_protiens", "albumin", "ag_ratio"]
    data = {k: record.get(k) for k in cols}

    keys = ", ".join([k for k, v in data.items() if v is not None])
    placeholders = ", ".join(["?" for k, v in data.items() if v is not None])
    values = [v for k, v in data.items() if v is not None]

    sql = f"INSERT INTO patients ({keys}) VALUES ({placeholders})"
    cur.execute(sql, values)
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid

def get_patient(patient_id: int, db_path: str = None) -> Dict[str, Any]:
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None