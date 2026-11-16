import pytest
from src.profile import Profile, active_conditions, compute_bmi, personal_risk

def test_bmi_from_height_weight():
    assert compute_bmi(Profile(height_cm=170, weight_kg=70)) == 24.2

def test_high_bmi_activates_obesity():
    assert "obesity" in active_conditions(Profile(height_cm=160, weight_kg=80))

def test_healthy_person_has_no_conditions():
    assert active_conditions(Profile(height_cm=175, weight_kg=60)) == []

def test_personal_never_below_general():
    row = {"risk_general": 2, "risk_diabetes": 0, "risk_hypertension": 0, "risk_obesity": 0}
    assert personal_risk(row, Profile(diabetes=True)) >= row["risk_general"]

def test_condition_raises_risk():
    row = {"risk_general": 1, "risk_diabetes": 3, "risk_hypertension": 0, "risk_obesity": 0}
    assert personal_risk(row, Profile(diabetes=True)) == 3
    assert personal_risk(row, Profile()) == 1

def test_impossible_age_rejected():
    with pytest.raises(ValueError):
        active_conditions(Profile(age=200))
        