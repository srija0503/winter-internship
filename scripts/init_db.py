"""
Simple script to create DB and insert a sample record.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from db import create_db, insert_patient

def main():
    db = create_db()
    sample = {
        "name": "Sample Patient",
        "disease_prob": "12.3%",
        "risk_label": "Low Risk",
        "age": 45,
        "gender": 1,
        "total_bilirubin": 0.8,
        "direct_bilirubin": 0.2,
        "alkaline_phosphotase": 80,
        "alamine_aminotransferase": 30,
        "aspartate_aminotransferase": 25,
        "total_protiens": 7.0,
        "albumin": 4.0,
        "ag_ratio": 1.2
    }
    rowid = insert_patient(sample, db_path=db)
    print("Inserted sample patient with id:", rowid)

if __name__ == "__main__":
    main()