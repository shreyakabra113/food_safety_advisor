import pytest
from src.kb import load_kb

RISK = ["risk_general", "risk_diabetes", "risk_hypertension", "risk_obesity"]

@pytest.fixture(scope="module")
def kb():
    return load_kb()

def test_no_empty_reasons_or_sources(kb):
    assert kb["reason"].notna().all(), kb[kb["reason"].isna()].index.tolist()
    assert kb["source"].notna().all()

def test_risks_are_0_to_3(kb):
    assert kb[RISK].isin([0, 1, 2, 3]).all().all()

def test_no_duplicate_ingredients(kb):
    assert kb.index.is_unique

def test_fallback_rows_exist(kb):
    for row in ["any added sugar", "any refined starch", "any sodium additive",
                "any artificial sweetener", "any synthetic colour", "any hydrogenated fat",
                "any flavour", "any spice", "any vegetable", "any pulse", "any nut"]:
        assert row in kb.index, row