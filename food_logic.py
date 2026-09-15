from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
import random

BASE_PEOPLE = 4

MEALS = [
    {
        "id": "adas-polo", "name": "عدس‌پلو", "emoji": "🍚", "minutes": 55, "cost": 2,
        "tags": ["legume", "rice", "vegetarian"],
        "ingredients": [("برنج", 3, "پیمانه"), ("عدس", 1.5, "پیمانه"), ("پیاز", 2, "عدد"), ("کشمش", 120, "گرم"), ("دارچین", 1, "قاشق چای‌خوری")],
        "recipe": ["عدس را جداگانه نیم‌پز کن.", "برنج را آبکش کن و عدس را لابه‌لای آن بریز.", "پیاز را طلایی کن و کشمش را کوتاه تفت بده.", "برنج را دم کن و با پیاز، کشمش و دارچین سرو کن."],
    },
    {
        "id": "ghormeh-sabzi", "name": "قورمه‌سبزی", "emoji": "🥘", "minutes": 150, "cost": 4,
        "tags": ["red_meat", "rice", "vegetable"],
        "ingredients": [("گوشت خورشتی", 400, "گرم"), ("سبزی قورمه", 500, "گرم"), ("لوبیا قرمز", 1, "پیمانه"), ("لیموعمانی", 4, "عدد"), ("پیاز", 1, "عدد"), ("برنج", 3, "پیمانه")],
        "recipe": ["پیاز و گوشت را تفت بده.", "سبزی سرخ‌شده و لوبیا را اضافه کن.", "آب و لیموعمانی را اضافه کن و با حرارت کم بپز.", "با برنج سرو کن."],
    },
    {
        "id": "zereshk-polo-chicken", "name": "زرشک‌پلو با مرغ", "emoji": "🍗", "minutes": 80, "cost": 4,
        "tags": ["chicken", "rice"],
        "ingredients": [("مرغ", 4, "تکه"), ("برنج", 3, "پیمانه"), ("زرشک", 100, "گرم"), ("پیاز", 1, "عدد"), ("زعفران دم‌کرده", 3, "قاشق غذاخوری")],
        "recipe": ["مرغ را با پیاز و ادویه کمی تفت بده.", "رب و آب را اضافه کن و مرغ را بپز.", "برنج را جدا دم کن.", "زرشک را کوتاه تفت بده و همراه زعفران روی برنج بریز."],
    },
    {
        "id": "kuku-sabzi", "name": "کوکو سبزی", "emoji": "🌿", "minutes": 35, "cost": 2,
        "tags": ["egg", "vegetable", "quick", "vegetarian", "no_rice"],
        "ingredients": [("سبزی کوکو", 500, "گرم"), ("تخم‌مرغ", 5, "عدد"), ("گردو", 60, "گرم"), ("زرشک", 40, "گرم")],
        "recipe": ["سبزی، تخم‌مرغ و ادویه را مخلوط کن.", "گردو و زرشک را اضافه کن.", "مایه را در تابه بریز و دو طرف را با حرارت ملایم بپز."],
    },
    {
        "id": "lentil-soup", "name": "عدسی", "emoji": "🥣", "minutes": 45, "cost": 1,
        "tags": ["legume", "vegetarian", "budget", "no_rice", "healthy"],
        "ingredients": [("عدس", 2, "پیمانه"), ("پیاز", 1, "عدد"), ("سیب‌زمینی", 1, "عدد"), ("رب گوجه", 1, "قاشق غذاخوری"), ("آب‌لیمو", 2, "قاشق غذاخوری")],
        "recipe": ["پیاز را سبک کن.", "عدس، سیب‌زمینی و آب را اضافه کن.", "پس از پخت، رب و ادویه را اضافه کن.", "با آب‌لیمو سرو کن."],
    },
    {
        "id": "fish-herb-rice", "name": "ماهی با سبزی‌پلو", "emoji": "🐟", "minutes": 65, "cost": 5,
        "tags": ["fish", "rice", "healthy"],
        "ingredients": [("فیله ماهی", 600, "گرم"), ("برنج", 3, "پیمانه"), ("سبزی پلویی", 300, "گرم"), ("لیموترش", 2, "عدد"), ("سیر", 2, "حبه")],
        "recipe": ["ماهی را با لیمو، سیر و ادویه مزه‌دار کن.", "برنج را با سبزی پلویی دم کن.", "ماهی را در فر، گریل یا تابه بپز.", "همراه سبزی‌پلو سرو کن."],
    },
    {
        "id": "chicken-vegetable-pan", "name": "مرغ و سبزیجات تابه‌ای", "emoji": "🥦", "minutes": 35, "cost": 3,
        "tags": ["chicken", "vegetable", "quick", "healthy", "no_rice"],
        "ingredients": [("سینه مرغ", 500, "گرم"), ("فلفل دلمه", 2, "عدد"), ("کدو", 2, "عدد"), ("هویج", 2, "عدد"), ("پیاز", 1, "عدد"), ("لیمو", 1, "عدد")],
        "recipe": ["مرغ را نواری خرد و تفت بده.", "سبزیجات را اضافه کن و روی حرارت بالا بپز.", "ادویه و آب‌لیمو را اضافه کن و گرم سرو کن."],
    },
    {
        "id": "omelette", "name": "املت گوجه", "emoji": "🍳", "minutes": 20, "cost": 1,
        "tags": ["egg", "quick", "budget", "no_rice"],
        "ingredients": [("تخم‌مرغ", 5, "عدد"), ("گوجه", 5, "عدد"), ("پیاز", 1, "عدد")],
        "recipe": ["پیاز و گوجه را تفت بده تا آب گوجه کم شود.", "نمک و ادویه اضافه کن.", "تخم‌مرغ‌ها را اضافه کن و تا حد دلخواه بپز."],
    },
    {
        "id": "makaroni", "name": "ماکارونی", "emoji": "🍝", "minutes": 60, "cost": 3,
        "tags": ["red_meat", "pasta"],
        "ingredients": [("ماکارونی", 500, "گرم"), ("گوشت چرخ‌کرده", 300, "گرم"), ("پیاز", 1, "عدد"), ("رب گوجه", 2, "قاشق غذاخوری"), ("سیب‌زمینی", 1, "عدد")],
        "recipe": ["مایه گوشت، پیاز و رب را آماده کن.", "ماکارونی را کمی کمتر از حد معمول بجوشان و آبکش کن.", "با مایه لایه‌لایه در قابلمه بریز و دم کن."],
    },
    {
        "id": "ash-reshteh", "name": "آش رشته", "emoji": "🍲", "minutes": 110, "cost": 2,
        "tags": ["legume", "vegetable", "vegetarian", "no_rice"],
        "ingredients": [("نخود و لوبیا", 1.5, "پیمانه"), ("عدس", 1, "پیمانه"), ("سبزی آش", 700, "گرم"), ("رشته آش", 300, "گرم"), ("کشک", 250, "گرم")],
        "recipe": ["حبوبات خیس‌خورده را بپز.", "سبزی و سپس رشته را اضافه کن.", "غلظت آش را تنظیم کن و با کشک و پیازداغ سرو کن."],
    },
    {
        "id": "kotlet", "name": "کتلت", "emoji": "🥔", "minutes": 50, "cost": 3,
        "tags": ["red_meat", "no_rice"],
        "ingredients": [("گوشت چرخ‌کرده", 350, "گرم"), ("سیب‌زمینی", 4, "عدد"), ("پیاز", 1, "عدد"), ("تخم‌مرغ", 2, "عدد")],
        "recipe": ["سیب‌زمینی و پیاز را رنده کن و آب اضافه را بگیر.", "با گوشت، تخم‌مرغ و ادویه مخلوط کن.", "کتلت‌ها را شکل بده و دو طرف را سرخ کن."],
    },
    {
        "id": "mirza-ghasemi", "name": "میرزا قاسمی", "emoji": "🍆", "minutes": 50, "cost": 2,
        "tags": ["egg", "vegetable", "vegetarian", "no_rice", "healthy"],
        "ingredients": [("بادمجان", 5, "عدد"), ("گوجه", 4, "عدد"), ("تخم‌مرغ", 3, "عدد"), ("سیر", 5, "حبه")],
        "recipe": ["بادمجان‌ها را کباب و پوست بگیر.", "سیر و گوجه را تفت بده.", "بادمجان را اضافه کن و در پایان تخم‌مرغ را داخل مواد بپز."],
    },
    {
        "id": "bean-rice", "name": "لوبیاپلو", "emoji": "🍛", "minutes": 80, "cost": 3,
        "tags": ["red_meat", "rice", "vegetable"],
        "ingredients": [("برنج", 3, "پیمانه"), ("لوبیا سبز", 400, "گرم"), ("گوشت چرخ‌کرده", 300, "گرم"), ("پیاز", 1, "عدد")],
        "recipe": ["مایه گوشت و لوبیا سبز را آماده کن.", "برنج را آبکش کن.", "برنج و مایه را لایه‌لایه بریز و دم کن."],
    },
    {
        "id": "falafel", "name": "فلافل خانگی", "emoji": "🧆", "minutes": 40, "cost": 1,
        "tags": ["legume", "vegetarian", "budget", "quick", "no_rice"],
        "ingredients": [("نخود خیس‌خورده", 3, "پیمانه"), ("پیاز", 1, "عدد"), ("سیر", 3, "حبه"), ("جعفری", 0.5, "پیمانه"), ("نان", 4, "عدد")],
        "recipe": ["نخود، پیاز، سیر و ادویه را چرخ کن.", "مایه را استراحت بده.", "شکل بده و با روغن کم یا در هواپز بپز."],
    },
    {
        "id": "vegetable-soup", "name": "سوپ جو و سبزیجات", "emoji": "🥕", "minutes": 55, "cost": 1,
        "tags": ["vegetable", "vegetarian", "budget", "healthy", "no_rice"],
        "ingredients": [("جو پرک", 1.5, "پیمانه"), ("هویج", 3, "عدد"), ("قارچ", 250, "گرم"), ("کرفس", 2, "ساقه"), ("پیاز", 1, "عدد")],
        "recipe": ["پیاز و سبزیجات را کمی تفت بده.", "جو و آب را اضافه کن.", "با حرارت ملایم تا جا افتادن بپز و در پایان لیمو اضافه کن."],
    },
]


def scale_ingredients(ingredients, people: int, base_people: int = BASE_PEOPLE):
    factor = people / base_people
    return [(name, round(amount * factor, 2), unit) for name, amount, unit in ingredients]


def _recent_history(history, days: int = 7, now: datetime | None = None):
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    result = []
    for item in history:
        cooked_at = item.get("cooked_at")
        if isinstance(cooked_at, str):
            cooked_at = datetime.fromisoformat(cooked_at)
        if cooked_at and cooked_at.tzinfo is None:
            cooked_at = cooked_at.replace(tzinfo=timezone.utc)
        if cooked_at and cooked_at >= cutoff:
            result.append(item)
    return result


def weekly_counts(history):
    meal_map = {meal["id"]: meal for meal in MEALS}
    counts = Counter()
    for item in _recent_history(history):
        meal = meal_map.get(item.get("meal_id"))
        if meal:
            counts.update(meal["tags"])
    return counts


def score_meal(meal, history, mode: str = "balanced"):
    score = 50
    recent = history[:5]
    weekly = weekly_counts(history)

    if not any(item.get("meal_id") == meal["id"] for item in history):
        score += 20
    if any(item.get("meal_id") == meal["id"] for item in recent[:2]):
        score -= 35

    recent_tags = []
    meal_map = {m["id"]: m for m in MEALS}
    for item in recent[:3]:
        recent_meal = meal_map.get(item.get("meal_id"))
        if recent_meal:
            recent_tags.extend(recent_meal["tags"])

    for tag in ("rice", "red_meat", "chicken", "fish", "legume", "egg"):
        if tag in meal["tags"] and tag in recent_tags:
            score -= 7

    if weekly.get("fish", 0) == 0 and "fish" in meal["tags"]:
        score += 16
    if weekly.get("legume", 0) < 2 and "legume" in meal["tags"]:
        score += 9
    if weekly.get("vegetable", 0) < 2 and "vegetable" in meal["tags"]:
        score += 7
    if weekly.get("red_meat", 0) >= 2 and "red_meat" in meal["tags"]:
        score -= 14

    if mode == "quick":
        score += 24 if meal["minutes"] <= 40 else -18
    elif mode == "budget":
        score += 22 if meal["cost"] <= 2 else -10
    elif mode == "balanced":
        score += 14 if "healthy" in meal["tags"] else 0

    return score


def recommend_meal(history, mode: str = "balanced", excluded_ids=None, rng=None):
    excluded_ids = set(excluded_ids or [])
    candidates = [meal for meal in MEALS if meal["id"] not in excluded_ids] or MEALS[:]
    ranked = sorted(candidates, key=lambda meal: score_meal(meal, history, mode), reverse=True)
    top = ranked[: min(3, len(ranked))]
    rng = rng or random
    return rng.choice(top)


def recommendation_reason(meal, history, mode: str = "balanced"):
    if mode == "quick":
        return "سریع و کم‌دردسر"
    if mode == "budget":
        return "اقتصادی و ساده"
    weekly = weekly_counts(history)
    if weekly.get("fish", 0) == 0 and "fish" in meal["tags"]:
        return "برای تنوع این هفته، نوبت ماهی است"
    if weekly.get("legume", 0) < 2 and "legume" in meal["tags"]:
        return "حبوبات این هفته کم بوده"
    if "healthy" in meal["tags"]:
        return "انتخاب متعادل‌تر برای امروز"
    return "بر اساس غذاهای چند روز اخیر"


def balance_message(history):
    if not history:
        return "چند وعده ثبت کن تا پیشنهادها کم‌کم با برنامه غذاییت هماهنگ شوند."
    counts = weekly_counts(history)
    if counts.get("fish", 0) == 0:
        return "این هفته هنوز ماهی ثبت نشده؛ اگر دوست داری وعده بعدی را از غذاهای ماهی انتخاب می‌کنم."
    if counts.get("legume", 0) < 2:
        return "حبوبات این هفته کم بوده؛ عدسی، آش یا فلافل انتخاب خوبی است."
    if counts.get("vegetable", 0) < 2:
        return "سبزیجات این هفته کم بوده؛ یک غذای سبزیجات‌محور بد نیست."
    if counts.get("red_meat", 0) >= 3:
        return "گوشت قرمز چند بار تکرار شده؛ وعده بعدی بهتر است مرغ، ماهی یا حبوبات باشد."
    return "تنوع این هفته خوب است؛ همین روند را ادامه بده."
