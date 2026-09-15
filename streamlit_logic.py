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
    limits = {"تا ۳۰ دقیقه": 30, "تا ۱ ساعت": 60, "تا ۱ ساعت و نیم": 90, "تا ۲ ساعت": 120}
    return time_filter == "مهم نیست" or total_minutes(food) <= limits[time_filter]


def matches_cost(food: dict, selected_costs: list[str]) -> bool:
    return not selected_costs or food["cost"] in selected_costs


def matches_weight(food: dict, selected_weights: list[str]) -> bool:
    return not selected_weights or food["weight"] in selected_weights


def matches_categories(food: dict, selected_categories: list[str]) -> bool:
    return not selected_categories or food["category"] in selected_categories


def filter_foods(foods: list[dict], *, time_filter: str = "مهم نیست", selected_costs: list[str] | None = None,
                 selected_weights: list[str] | None = None, selected_categories: list[str] | None = None) -> list[dict]:
    selected_costs = selected_costs or []
    selected_weights = selected_weights or []
    selected_categories = selected_categories or []
    return [food for food in foods if matches_time(food, time_filter) and matches_cost(food, selected_costs)
            and matches_weight(food, selected_weights) and matches_categories(food, selected_categories)]


COST_ORDER = ["اقتصادی", "معمولی", "گران"]
WEIGHT_ORDER = ["سبک", "متوسط", "سنگین"]
TIME_LIMITS = {"تا ۳۰ دقیقه": 30, "تا ۱ ساعت": 60, "تا ۱ ساعت و نیم": 90, "تا ۲ ساعت": 120}


def _distance(value: str, selected: list[str], order: list[str]) -> int:
    if not selected:
        return 0
    index = order.index(value)
    return min(abs(index - order.index(item)) for item in selected)


def build_candidate_pool(foods: list[dict], usual_names: set[str], try_names: set[str], *, allow_new: bool = True) -> list[dict]:
    pool = [food for food in foods if food["name"] in usual_names or (allow_new and food["name"] in try_names)]
    if not pool:
        pool = [food for food in foods if food["name"] in usual_names]
    if not pool:
        pool = list(foods)
    result = []
    for food in pool:
        source = "usual" if food["name"] in usual_names else "try" if food["name"] in try_names else "catalog"
        result.append({**food, "_source": source})
    return result


def score_food(food: dict, *, time_filter: str = "مهم نیست", selected_costs: list[str] | None = None,
               selected_weights: list[str] | None = None, selected_categories: list[str] | None = None,
               priority: str = "balanced", history: list | None = None) -> dict:
    selected_costs = selected_costs or []
    selected_weights = selected_weights or []
    selected_categories = selected_categories or []
    history = history or []
    mult = lambda key: 4.0 if priority == key else 1.0
    score = 70 if food.get("_source") == "usual" else 28 if food.get("_source") == "try" else 0
    misses, matches = [], []

    limit = TIME_LIMITS.get(time_filter)
    if limit is not None:
        over = total_minutes(food) - limit
        if over <= 0:
            score += 24 * mult("time"); matches.append("زمان")
        else:
            score -= min(54, 8 + (over / 10) * 5) * mult("time")
            misses.append(f"{format_minutes(over)} بیشتر از زمان دلخواه")

    if selected_costs:
        if food["cost"] in selected_costs:
            score += 20 * mult("cost"); matches.append("هزینه")
        else:
            score -= (10 + 10 * _distance(food["cost"], selected_costs, COST_ORDER)) * mult("cost")
            misses.append(f"هزینه {food['cost']}")

    if selected_weights:
        if food["weight"] in selected_weights:
            score += 20 * mult("weight"); matches.append("سبکی/سنگینی")
        else:
            score -= (8 + 9 * _distance(food["weight"], selected_weights, WEIGHT_ORDER)) * mult("weight")
            misses.append(f"{food['weight']} است")

    if selected_categories:
        if food["category"] in selected_categories:
            score += 22 * mult("category"); matches.append("دسته‌بندی")
        else:
            score -= 14 * mult("category")
            misses.append(f"از دسته «{food['category']}» است")

    recent = [item if isinstance(item, str) else item.get("name") for item in history[:6]]
    if food["name"] in recent:
        pos = recent.index(food["name"])
        score -= 60 if pos == 0 else 32 if pos < 3 else 12

    return {**food, "_score": score, "_misses": misses, "_matches": matches, "_exact": not misses}


def rank_nearest(foods: list[dict], usual_names: set[str], try_names: set[str], *, allow_new: bool = True,
                 time_filter: str = "مهم نیست", selected_costs: list[str] | None = None,
                 selected_weights: list[str] | None = None, selected_categories: list[str] | None = None,
                 priority: str = "balanced", history: list | None = None) -> list[dict]:
    pool = build_candidate_pool(foods, usual_names, try_names, allow_new=allow_new)
    ranked = [score_food(food, time_filter=time_filter, selected_costs=selected_costs,
                         selected_weights=selected_weights, selected_categories=selected_categories,
                         priority=priority, history=history) for food in pool]
    return sorted(ranked, key=lambda item: (-item["_score"], total_minutes(item), item["name"]))


def fit_message(food: dict | None) -> str:
    if not food:
        return ""
    if food.get("_exact"):
        return "✅ با همه انتخاب‌های امروزت جور است."
    return "🔎 نزدیک‌ترین پیشنهاد است؛ " + "، ".join(food.get("_misses", [])[:2]) + "."


def rank_foods(foods: list[dict], usual_names: set[str], try_names: set[str], *, allow_new: bool = True,
               rng: random.Random | None = None) -> list[dict]:
    rng = rng or random.Random()
    ranked = []
    for food in foods:
        name = food["name"]
        if name in usual_names:
            score, source = 100, "usual"
        elif allow_new and name in try_names:
            score, source = 72, "try"
        elif not usual_names and not try_names:
            score, source = 50, "catalog"
        else:
            score, source = (12 if allow_new else -1000), "catalog"
        ranked.append({**food, "_score": score + rng.random() * 14, "_source": source})
    return sorted(ranked, key=lambda item: item["_score"], reverse=True)


def recommend_food(foods: list[dict], usual_names: set[str], try_names: set[str], *, allow_new: bool = True,
                   rng: random.Random | None = None) -> dict | None:
    if not foods:
        return None
    ranked = rank_foods(foods, usual_names, try_names, allow_new=allow_new, rng=rng)
    top = ranked[: min(3, len(ranked))]
    rng = rng or random.Random()
    return rng.choice(top)


def suggested_new_foods(foods: list[dict], usual_names: set[str], limit: int = 20) -> list[str]:
    usual_categories = {f["category"] for f in foods if f["name"] in usual_names}
    candidates = [f for f in foods if f["name"] not in usual_names]
    candidates.sort(key=lambda f: (f["category"] in usual_categories, total_minutes(f), 0 if f["cost"] == "اقتصادی" else 1))
    picked = []
    for category in dict.fromkeys(f["category"] for f in foods):
        for food in [f for f in candidates if f["category"] == category][:2]:
            if food["name"] not in picked:
                picked.append(food["name"])
    for food in candidates:
        if len(picked) >= limit:
            break
        if food["name"] not in picked:
            picked.append(food["name"])
    return picked[:limit]
