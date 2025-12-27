import pytest
from src.clinical_rules import get_warnings

def test_no_warnings_for_normal_values():
    patient = {
        "total_bilirubin": 0.8,
        "alamine_aminotransferase": 30,
        "albumin": 4.2,
        "aspartate_aminotransferase": 25
    }
    assert get_warnings(patient) == []

def test_jaundice_warning():
    patient = {"total_bilirubin": 2.5}
    ws = get_warnings(patient)
    assert any("Jaundice" in w or "Bilirubin" in w for w in ws)

def test_high_alt_warning():
    patient = {"alamine_aminotransferase": 200}
    ws = get_warnings(patient)
    assert any("ALT" in w for w in ws)

def test_low_albumin_warning():
    patient = {"albumin": 2.8}
    ws = get_warnings(patient)
    assert any("Low Albumin" in w for w in ws)

def test_ast_alt_ratio_warning():
    patient = {"aspartate_aminotransferase": 200, "alamine_aminotransferase": 50}
    ws = get_warnings(patient)
    assert any("AST/ALT ratio" in w for w in ws)