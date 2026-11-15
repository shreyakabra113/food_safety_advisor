import pandas as pd

# order matters: the first matching rule wins
RULES = [
    (("hydrogenated", "shortening", "margarine", "vanaspati"), "any hydrogenated fat"),
    (("syrup", "dextrose", "fructose", "sucrose", "molasses"), "any added sugar"),
    (("maida", "semolina", "rava"),                           "any refined starch"),
    (("sweetener", "aspartame", "sucralose", "acesulfame",
      "saccharin", "stevia"),                                  "any artificial sweetener"),
    (("sodium", "soda"),                                       "any sodium additive"),
    (("flavour", "flavor"),                                    "any flavour"),
]

def load_kb(path="../data/knowledgebase/ingredient.csv"):
    return pd.read_csv(path).set_index("ingredient")

def lookup(name, kb):
    """Return (row, how). how is 'exact', 'fallback:<row name>' or 'unrecognized'."""
    if name in kb.index:
        return kb.loc[name], "exact"
    for words, fallback in RULES:
        if any(w in name for w in words):
            return kb.loc[fallback], f"fallback:{fallback}"
    return None, "unrecognized"