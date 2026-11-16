from src.kb import load_kb
from src.profile import Profile
from src.verdict import analyse, ORDER

kb = load_kb()

def test_plain_water_is_safe():
    assert analyse("water", kb)["general"]["verdict"] == "Safe"

def test_personal_never_better_than_general():
    r = analyse("sugar, palm oil, salt, maltodextrin", kb, Profile(diabetes=True))
    assert ORDER[r["personal"]["verdict"]] >= ORDER[r["general"]["verdict"]]

def test_unknown_ingredient_is_reported_not_scored():
    r = analyse("water, zzzxxyy", kb)
    assert "zzzxxyy" in r["unrecognized_ingredients"]

def test_trans_fat_forces_at_least_limit():
    r = analyse("water, hydrogenated vegetable fat", kb)
    assert r["general"]["verdict"] in ("Limit", "Avoid")