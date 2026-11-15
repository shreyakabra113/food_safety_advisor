import re

# 1. Known OCR/spelling fixes, applied as whole-word replacements
SPELLING = {
    "lodised": "iodised", "lodized": "iodized",
    "iodized": "iodised",              # one spelling style
    "sucar": "sugar", "relined": "refined", "mik": "milk",
    "palmolein": "palm oil", "palmolien": "palm oil",
}

# 2. Synonyms -> canonical name (start small, grow from your data)
SYNONYMS = {
    "maida": "refined wheat flour",
    "refined wheat flour maida": "refined wheat flour",
    "iodised salt": "salt",
    "edible salt": "salt",
    "common salt": "salt",
    "refined palm oil": "palm oil",
    "palm oil": "palm oil",
    "edible vegetable oil": "vegetable oil",
    "invert sugar syrup": "invert sugar",
    "liquid glucose": "glucose syrup",
}

def clean_name(raw):
    s = raw.lower().strip()
    s = re.sub(r"\d+(\.\d+)?\s*%", "", s)            # remove percentages
    s = re.sub(r"[^a-z0-9 ()]", " ", s)               # drop punctuation
    s = " ".join(SPELLING.get(w, w) for w in s.split())
    s = re.sub(r"\s+", " ", s).strip()
    return s

def canonical(raw):
    s = clean_name(raw)
    s = re.sub(r"[()]", " ", s)                       # flatten brackets
    s = re.sub(r"\s+", " ", s).strip()
    return SYNONYMS.get(s, s)