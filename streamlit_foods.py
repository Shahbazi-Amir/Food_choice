import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "data" / "foods.json"
FOODS = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
CATEGORIES = list(dict.fromkeys(food["category"] for food in FOODS))
FOOD_NAMES = [food["name"] for food in FOODS]
