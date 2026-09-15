from __future__ import annotations

import random


def total_minutes(food: dict) -> int:
    return int(food.get("prep", 0)) + int(food.get("cook", 0))


def format_minutes(minutes: int) -> str:
    minutes = int(minutes)
    if minutes < 60:
        return f"{minutes} دقیقه"
    hours, rest = divmod(minutes, 60)
    if rest == 0:
        return f"{hours} ساعت"
    return f"{hours} ساعت و {rest} دقیقه"


def matches_time(food: dict, time_filter: str) -> bool:
    total = total_minutes(food)
    limits = {
        "تا ۳۰ دقیقه": 30,
        "تا ۱ ساعت": 60,
        "تا ۱ ساعت و نیم": 90,
        "تا ۲ ساعت": 120,
    }
    if time_filter == "مهم نیست":
        return True
    return total <= limits[time_filter]


def matches_cost(food: dict, selected_costs: list[str]) -> bool:
    return not selected_costs or food["cost"] in selected_costs


def matches_weight(food: dict, selected_weights: list[str]) -> bool:
    return not selected_weights or food["weight"] in selected_weights


def matches_categories(food: dict, selected_categories: list[str]) -> bool:
    return not selected_categories or food["category"] in selected_categories


def filter_foods(
    foods: list[dict],
    *,
    time_filter: str = "مهم نیست",
    selected_costs: list[str] | None = None,
    selected_weights: list[str] | None = None,
    selected_categories: list[str] | None = None,
) -> list[dict]:
    selected_costs = selected_costs or []
    selected_weights = selected_weights or []
    selected_categories = selected_categories or []
    return [
        food
        for food in foods
        if matches_time(food, time_filter)
        and matches_cost(food, selected_costs)
        and matches_weight(food, selected_weights)
        and matches_categories(food, selected_categories)
    ]


def rank_foods(
    foods: list[dict],
    usual_names: set[str],
    try_names: set[str],
    *,
    allow_new: bool = True,
    rng: random.Random | None = None,
) -> list[dict]:
    """Prefer familiar foods, but keep selected experiment foods in rotation.

    Familiar foods get the strongest baseline score. Foods explicitly marked as
    "I'd like to try" can occasionally surface, while completely unknown foods
    remain last unless the user's own lists are empty.
    """
    rng = rng or random.Random()
    ranked = []
    for food in foods:
        name = food["name"]
        if name in usual_names:
            score = 100
            source = "usual"
        elif allow_new and name in try_names:
            score = 72
            source = "try"
        elif not usual_names and not try_names:
            score = 50
            source = "catalog"
        else:
            score = 12 if allow_new else -1000
            source = "catalog"
        score += rng.random() * 14
        ranked.append({**food, "_score": score, "_source": source})
    return sorted(ranked, key=lambda item: item["_score"], reverse=True)


def recommend_food(
    foods: list[dict],
    usual_names: set[str],
    try_names: set[str],
    *,
    allow_new: bool = True,
    rng: random.Random | None = None,
) -> dict | None:
    if not foods:
        return None
    ranked = rank_foods(foods, usual_names, try_names, allow_new=allow_new, rng=rng)
    # Pick from the best few to avoid feeling deterministic while keeping quality.
    top = ranked[: min(3, len(ranked))]
    rng = rng or random.Random()
    return rng.choice(top)


def suggested_new_foods(foods: list[dict], usual_names: set[str], limit: int = 8) -> list[str]:
    """Suggest approachable additions, favoring categories absent from the usual list."""
    usual_foods = [f for f in foods if f["name"] in usual_names]
    usual_categories = {f["category"] for f in usual_foods}
    candidates = [f for f in foods if f["name"] not in usual_names]
    candidates.sort(
        key=lambda f: (
            f["category"] in usual_categories,
            total_minutes(f),
            0 if f["cost"] == "اقتصادی" else 1,
        )
    )
    return [f["name"] for f in candidates[:limit]]
