import re
from src.normalize import canonical, clean_name

CATS = ["acidity regulator", "raising agent", "anticaking agent", "flavour enhancer",
        "firming agent", "antioxidant", "thickener", "sequestrant", "stabilizer",
        "stabiliser", "emulsifier", "preservative", "sweetener", "colour", "color",
        "flavouring", "flavoring", "flavour", "flavor"]
CAT_SPLIT = re.compile(r"\b(" + "|".join(CATS) + r")(?:s|es)?\b")
FLAV      = {"flavouring", "flavoring", "flavour", "flavor"}
CAT_FIX   = {"color": "colour", "stabiliser": "stabilizer"}

ADVISORY = re.compile(r"\b(may contain|contains|allergen|for allergens|please see|packed in)\b.*")
CODE     = re.compile(r"\b(?:ins|e)?\s*(\d{3,4}[a-z]?)\b")
ROMAN    = re.compile(r"\b(?:i|ii|iii|iv)\b")
NOISE    = re.compile(r"\b(permitted|class|natural|nature|identical|added|food)\b")


def tidy(t):
    t = ROMAN.sub(" ", NOISE.sub(" ", t))
    t = " ".join(t.split())
    return re.sub(r"^(?:and )+|(?: and)+$|^and$", "", t).strip()


def split_ingredients(text):
    return [part.strip() for part in text.split(",") if part.strip()]


def expand_item(item):
    """'emulsifier (soy lecithin, ins 322)' -> ['emulsifier', 'soy lecithin', 'ins 322'].
       A bracket with one plain word, like '(maida)', is a synonym and stays."""
    m = re.match(r"^(.*?)\((.*)\)\s*$", item.strip())
    if not m:
        return [item]
    parent, inside = m.group(1).strip(), m.group(2)
    if "," in inside or CODE.search(inside):
        return ([parent] if parent else []) + split_ingredients(inside)
    return [item]


def parse_piece(piece):
    s = clean_name(piece).replace("(", " ").replace(")", " ")
    s = " ".join(ADVISORY.sub("", s).split())
    if not s:
        return []
    m = re.fullmatch(r"(?:ins|e)?\s*(\d{3,4}[a-z]?)(?:\s+(?:i|ii|iii|iv))?", s)
    if m:                                   # a bare code like '503' or '500 i'
        return [f"ins {m.group(1)}"]
    parts = CAT_SPLIT.split(s)              # [before, cat1, text1, cat2, text2, ...]
    out = []
    pre = tidy(parts[0])
    if pre and (len(parts) == 1 or parts[1] not in FLAV):
        out.append(pre)
    for i in range(1, len(parts), 2):
        cat, text = parts[i], parts[i + 1]
        if cat in FLAV:                     # every flavour phrase becomes one item
            out.append("added flavour")
            continue
        out.append(CAT_FIX.get(cat, cat))
        out += [f"ins {c}" for c in CODE.findall(text)]
        left = tidy(CODE.sub(" ", text))
        if left:
            out.append(left)
    return out


def parse_ingredient(raw):
    out = []
    for piece in expand_item(raw):
        for q in parse_piece(piece):
            c = canonical(q)
            if c and c not in out:
                out.append(c)
    return out