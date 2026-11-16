from pathlib import Path
import pandas as pd

# Works from any folder: the CSV is found relative to this file, not the notebook
DEFAULT_KB = Path(__file__).resolve().parent.parent / "data" / "knowledge_base" / "ingredients.csv"

QUALIFIERS = {"powder", "powdered", "dried", "fresh", "roasted", "crushed", "ground", "flakes", "paste"}

# Risky categories first, so a risky word is never hidden by a harmless one
RULES = [
    (("hydrogenated", "shortening", "margarine", "vanaspati"), "any hydrogenated fat"),
    (("syrup", "dextrose", "fructose", "sucrose", "molasses"), "any added sugar"),
    (("maida", "semolina", "rava"),                           "any refined starch"),
    (("sweetener", "aspartame", "sucralose", "acesulfame", "saccharin", "stevia"), "any artificial sweetener"),
    (("sodium", "soda"),                                       "any sodium additive"),
    (("flavour", "flavor"),                                    "any flavour"),
]

# Whole foods: matched on whole words only, and kept deliberately short
WHOLE = [
    ({"pepper", "chilli", "chili", "cardamom", "cinnamon", "clove", "cumin", "coriander",
      "turmeric", "mustard", "fenugreek", "asafoetida", "hing", "nutmeg", "fennel",
      "saffron", "spices", "masala"},                          "any spice"),
    ({"garlic", "onion", "ginger", "tomato", "potato", "carrot", "peas", "cabbage",
      "spinach", "capsicum", "beetroot"},                      "any vegetable"),
    ({"dal", "gram", "lentil", "chickpea", "moong", "masoor", "urad", "rajma", "chana"}, "any pulse"),
    ({"almond", "cashew", "peanut", "peanuts", "walnut", "pistachio", "hazelnut"}, "any nut"),
]

# If a name contains one of these and no earlier rule matched, never call it a harmless whole food
RISK_WORDS = {"salt", "sugar", "syrup", "oil", "fat", "butter", "ghee", "sodium",
              "honey", "jaggery", "sauce", "ketchup", "chocolate", "candy", "juice"}


def load_kb(path=DEFAULT_KB):
    return pd.read_csv(path).set_index("ingredient")


def lookup(name, kb):
    """Return (row, how). how: 'exact', 'stripped', 'fallback:<row>', 'whole:<row>' or 'unrecognized'."""
    if name in kb.index:
        return kb.loc[name], "exact"

    words = name.split()
    base = " ".join(w for w in words if w not in QUALIFIERS)
    if base and base != name and base in kb.index:
        return kb.loc[base], "stripped"

    for keys, row in RULES:
        if row in kb.index and any(k in name for k in keys):
            return kb.loc[row], f"fallback:{row}"

    tokens = set(words)
    if RISK_WORDS & tokens:
        return None, "unrecognized"          # cautious: report it instead of calling it harmless

    for keys, row in WHOLE:
        if row in kb.index and tokens & keys:
            return kb.loc[row], f"whole:{row}"

    return None, "unrecognized"
