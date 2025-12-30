import pytest
from src.data_loader import load_data

def test_required_columns_exist():
    df = load_data()
    required = {"dataset", "gender", "total_bilirubin", "alamine_aminotransferase", "albumin"}
    assert required.issubset(set(df.columns)), f"Missing required columns: {required - set(df.columns)}"

def test_no_negative_values_for_bilirubin():
    df = load_data()
    if "total_bilirubin" in df.columns:
        assert (df["total_bilirubin"].dropna() >= 0).all(), "Negative total_bilirubin values found"