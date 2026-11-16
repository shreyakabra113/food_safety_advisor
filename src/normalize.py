import re

# Single-word spelling and OCR fixes, applied word by word
SPELLING = {
    "lodised": "iodised", "lodized": "iodised", "iodized": "iodised",
    "sucar": "sugar", "relined": "refined", "mik": "milk",
    "brand": "bran",                      # "rice brand oil" is an OCR slip for "rice bran oil"
}

# canonical name -> every other name that means the same thing.
# Aliases must be lowercase letters, digits and spaces only (clean_name has already
# removed punctuation and percentages, and flattened brackets).
GROUPS = {
    # --- salts (all are sodium sources) ---
    "salt": ["iodised salt", "edible salt", "common salt", "edible common salt",
             "edible iodised salt", "table salt", "iodised common salt", "salt iodised",
             "black salt", "rock salt", "sea salt", "pink salt", "himalayan salt",
             "sendha namak", "kala namak"],

    # --- sugars ---
    "sugar": ["sugars", "cane sugar", "white sugar", "refined sugar", "sucrose",
              "powdered sugar", "icing sugar", "castor sugar", "caster sugar",
              "brown sugar", "raw sugar", "sugar syrup"],
    "invert sugar": ["invert sugar syrup", "invert syrup", "inverted sugar", "inverted sugar syrup"],
    "glucose syrup": ["liquid glucose", "glucose syrup solids", "dried glucose syrup",
                      "corn syrup", "glucose solids", "glucose"],
    "high fructose corn syrup": ["hfcs", "glucose fructose syrup", "fructose syrup", "high fructose syrup"],
    "jaggery": ["gur", "jaggery powder", "cane jaggery"],
    "dextrose": ["dextrose monohydrate", "dextrose anhydrous"],
    "maltodextrin": ["maltodextrins"],

    # --- flours and starches ---
    "refined wheat flour": ["maida", "refined wheat flour maida", "wheat flour maida",
                            "maida refined wheat flour", "refined flour", "white flour",
                            "all purpose flour", "enriched wheat flour", "wheat flour refined"],
    "whole wheat flour": ["atta", "whole wheat atta", "wheat atta", "wholemeal flour",
                          "wholemeal wheat flour", "wheat flour atta"],
    "starch": ["maize starch", "corn starch", "cornstarch", "corn flour", "cornflour",
               "tapioca starch", "potato starch", "wheat starch", "modified starch"],
    "gram flour": ["besan", "chickpea flour"],
    "oats": ["rolled oats", "oat flakes", "quick oats", "oatmeal"],
    "wheat gluten": ["gluten", "vital wheat gluten"],

    # --- oils and fats (palm kernel oil and coconut oil are deliberately NOT merged into palm oil) ---
    "palm oil": ["refined palm oil", "palm oil refined", "edible vegetable oil palm oil",
                 "palmolein", "palm olein", "refined palmolein oil", "refined palm olein",
                 "palmolein oil", "palm olein oil", "rbd palmolein", "rbd palm olein",
                 "palm oil palmolein"],
    "vegetable oil": ["edible vegetable oil", "refined vegetable oil", "edible oil",
                      "refined edible oil", "refined oil", "vegetable oil edible"],
    "sunflower oil": ["refined sunflower oil", "edible sunflower oil", "sunflower refined oil"],
    "soybean oil": ["soyabean oil", "soya bean oil", "refined soybean oil",
                    "refined soyabean oil", "soya oil"],
    "rice bran oil": ["refined rice bran oil", "edible rice bran oil"],
    "groundnut oil": ["peanut oil", "refined groundnut oil"],
    "coconut oil": ["refined coconut oil", "edible coconut oil"],
    "mustard oil": ["refined mustard oil"],
    "cottonseed oil": ["refined cottonseed oil"],
    "ghee": ["pure ghee", "desi ghee", "clarified butter"],
    "hydrogenated vegetable fat": ["hydrogenated vegetable oil", "hydrogenated oil",
                                   "hydrogenated fat", "vanaspati", "hydrogenated edible fat"],
    "partially hydrogenated oil": ["partially hydrogenated vegetable oil",
                                   "partially hydrogenated vegetable fat",
                                   "partially hydrogenated fat"],

    # --- dairy ---
    "milk solids": ["milk solid", "skimmed milk powder", "skim milk powder", "skimmed milk solids",
                    "whole milk powder", "full cream milk powder", "milk powder",
                    "dried milk solids", "non fat milk solids", "nonfat milk solids"],
    "milk": ["toned milk", "pasteurised toned milk", "pasteurised milk", "fresh milk",
             "cow milk", "full cream milk", "skimmed milk", "double toned milk"],

    # --- cocoa, nuts, legumes, grains ---
    "cocoa solids": ["cocoa mass", "cocoa liquor", "cocoa"],
    "peanuts": ["peanut", "groundnut", "groundnuts", "roasted peanuts"],
    "chickpea": ["gram dal", "chana kabuli", "chana dal", "bengal gram"],
    "soy": ["soya", "soybean", "soya bean", "soyabean"],
    "yeast": ["baker s yeast", "active dry yeast", "active yeast", "instant yeast"],
    "water": ["drinking water", "potable water", "filtered water", "mineral water"],

    # --- spices and vegetables ---
    "turmeric": ["haldi", "turmeric powder"],
    "cumin": ["jeera", "cumin seeds", "cumin powder"],
    "coriander": ["dhania", "coriander powder", "coriander seeds"],
    "red chilli": ["chilli powder", "red chilli powder", "red chili", "red chili powder", "chili powder"],
    "black pepper": ["black pepper powder", "pepper powder", "kali mirch"],
    "cinnamon": ["dalchini", "cassia", "cassia dalchini"],
    "garlic": ["garlic powder", "dried garlic", "garlic flakes"],
    "onion": ["onion powder", "dried onion", "onion flakes"],
    "ginger": ["ginger powder", "dry ginger", "dried ginger"],

    # --- additives: chemical names mapped to the INS code row in the knowledge base ---
    "ins 621": ["monosodium glutamate", "msg"],
    "ins 631": ["disodium inosinate"],
    "ins 627": ["disodium guanylate"],
    "ins 211": ["sodium benzoate"],
    "ins 202": ["potassium sorbate"],
    "ins 282": ["calcium propionate"],
    "ins 330": ["citric acid"],
    "ins 260": ["acetic acid"],
    "ins 300": ["ascorbic acid", "vitamin c"],
    "ins 322": ["lecithin", "lecithins", "soy lecithin", "soya lecithin", "sunflower lecithin"],
    "ins 471": ["mono and diglycerides", "mono and diglycerides of fatty acids", "mono diglycerides"],
    "ins 415": ["xanthan gum"],
    "ins 412": ["guar gum"],
    "ins 407": ["carrageenan"],
    "ins 466": ["cellulose gum", "carboxymethyl cellulose"],
    "ins 500": ["sodium bicarbonate", "baking soda", "sodium carbonate"],
    "ins 503": ["ammonium bicarbonate", "ammonium carbonate"],
    "ins 551": ["silicon dioxide"],
    "ins 102": ["tartrazine"],
    "ins 110": ["sunset yellow", "sunset yellow fcf"],
    "raising agent": ["baking powder"],
}

# Build the lookup and catch mistakes immediately
SYNONYMS, _seen = {}, {}
for _canon, _aliases in GROUPS.items():
    for _a in _aliases:
        assert re.fullmatch(r"[a-z0-9 ]+", _a), f"bad alias (use lowercase letters/digits/spaces): {_a!r}"
        assert _a not in _seen, f"{_a!r} is listed under both {_seen[_a]!r} and {_canon!r}"
        _seen[_a] = _canon
        SYNONYMS[_a] = _canon


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