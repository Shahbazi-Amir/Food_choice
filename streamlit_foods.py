import json
from pathlib import Path

BASE = Path(__file__).parent
CATALOG_PATH = BASE / "data" / "foods.json"
TAXONOMY_PATH = BASE / "data" / "taxonomy.json"
TAXONOMY = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
_raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

def _family(food):
    return TAXONOMY.get("family_overrides", {}).get(food["id"], TAXONOMY.get("family_by_legacy_category", {}).get(food["category"], food["category"]))

def _methods(food, family):
    return TAXONOMY.get("method_overrides", {}).get(food["id"], TAXONOMY.get("default_methods_by_family", {}).get(family, ["تابه‌ای"]))

FOODS = []
for item in _raw:
    family = _family(item)
    FOODS.append({**item, "family": family, "methods": _methods(item, family), "emoji": TAXONOMY.get("family_emoji", {}).get(family, "🍽️")})

FAMILIES = [name for name in TAXONOMY["families"] if any(f["family"] == name for f in FOODS)]
METHODS = list(TAXONOMY["methods"])
CATEGORIES = FAMILIES
FOOD_NAMES = [food["name"] for food in FOODS]
