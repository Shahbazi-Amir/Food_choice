from __future__ import annotations

import random

COST_ORDER=["اقتصادی","معمولی","گران"]
WEIGHT_ORDER=["سبک","متوسط","سنگین"]
TIME_LIMITS={"تا ۳۰ دقیقه":30,"تا ۱ ساعت":60,"تا ۱ ساعت و نیم":90,"تا ۲ ساعت":120}

def total_minutes(food:dict)->int:return int(food.get("prep",0))+int(food.get("cook",0))
def format_minutes(minutes:int)->str:
    minutes=int(minutes)
    if minutes<60:return f"{minutes} دقیقه"
    h,m=divmod(minutes,60)
    return f"{h} ساعت" if m==0 else f"{h} ساعت و {m} دقیقه"

def matches_time(food,time_filter):return time_filter=="مهم نیست" or total_minutes(food)<=TIME_LIMITS[time_filter]
def matches_cost(food,selected):return not selected or food["cost"] in selected
def matches_weight(food,selected):return not selected or food["weight"] in selected
def matches_categories(food,selected):return not selected or food.get("family",food.get("category")) in selected

def filter_foods(foods,*,time_filter="مهم نیست",selected_costs=None,selected_weights=None,selected_categories=None):
    selected_costs=selected_costs or [];selected_weights=selected_weights or [];selected_categories=selected_categories or []
    return [f for f in foods if matches_time(f,time_filter) and matches_cost(f,selected_costs) and matches_weight(f,selected_weights) and matches_categories(f,selected_categories)]

def _distance(value,selected,order):
    if not selected:return 0
    i=order.index(value);return min(abs(i-order.index(x)) for x in selected)

def build_candidate_pool(foods,usual_names,try_names,*,allow_new=True):
    result=[]
    for food in foods:
        if food["name"] in usual_names:result.append({**food,"_source":"usual"})
        elif allow_new and food["name"] in try_names:result.append({**food,"_source":"try"})
    return result

def _semantic(food,families,methods):
    family_ok=not families or food.get("family") in families
    method_ok=not methods or any(m in food.get("methods",[]) for m in methods)
    return family_ok,method_ok

def _semantic_candidates(foods,families,methods,priority):
    exact=[f for f in foods if all(_semantic(f,families,methods))]
    if exact:return exact,[]
    if families and methods:
        if priority=="category":
            family_only=[f for f in foods if _semantic(f,families,[])[0]]
            if family_only:return family_only,["روش پخت"]
        method_only=[f for f in foods if _semantic(f,[],methods)[1]]
        if method_only:return method_only,["نوع غذا"]
        family_only=[f for f in foods if _semantic(f,families,[])[0]]
        if family_only:return family_only,["روش پخت"]
    if methods:
        method_only=[f for f in foods if _semantic(f,[],methods)[1]]
        if method_only:return method_only,[]
    if families:
        family_only=[f for f in foods if _semantic(f,families,[])[0]]
        if family_only:return family_only,[]
    return [],[]

def score_food(food,*,time_filter="مهم نیست",selected_costs=None,selected_weights=None,priority="balanced",history=None):
    selected_costs=selected_costs or [];selected_weights=selected_weights or [];history=history or []
    mult=lambda key:4.0 if priority==key else 1.0
    score=70 if food.get("_source")=="usual" else 30 if food.get("_source")=="try" else 18 if food.get("_source")=="catalog-fallback" else 0
    misses=[];matches=[]
    limit=TIME_LIMITS.get(time_filter)
    if limit is not None:
        over=total_minutes(food)-limit
        if over<=0:score+=24*mult("time");matches.append("زمان")
        else:score-=min(70,8+(over/10)*5)*mult("time");misses.append(f"{format_minutes(over)} بیشتر از زمان دلخواه")
    if selected_costs:
        if food["cost"] in selected_costs:score+=20*mult("cost");matches.append("هزینه")
        else:score-=(10+10*_distance(food["cost"],selected_costs,COST_ORDER))*mult("cost");misses.append(f"هزینه {food['cost']}")
    if selected_weights:
        if food["weight"] in selected_weights:score+=20*mult("weight");matches.append("سبکی/سنگینی")
        else:score-=(8+9*_distance(food["weight"],selected_weights,WEIGHT_ORDER))*mult("weight");misses.append(f"{food['weight']} است")
    recent=[x if isinstance(x,str) else x.get("name") for x in history[:6]]
    if food["name"] in recent:
        pos=recent.index(food["name"]);score-=60 if pos==0 else 32 if pos<3 else 12
    return {**food,"_score":score,"_misses":misses,"_matches":matches,"_exact":not misses}

def rank_nearest(foods,usual_names,try_names,*,allow_new=True,time_filter="مهم نیست",selected_costs=None,selected_weights=None,selected_categories=None,selected_families=None,selected_methods=None,priority="balanced",history=None):
    families=selected_families if selected_families is not None else (selected_categories or [])
    methods=selected_methods or []
    user_pool=build_candidate_pool(foods,usual_names,try_names,allow_new=allow_new)
    pool,relaxed=_semantic_candidates(user_pool,families,methods,priority)
    if not pool:
        catalog=[{**f,"_source":"catalog-fallback"} for f in foods]
        pool,relaxed=_semantic_candidates(catalog,families,methods,priority)
    if not pool:pool=user_pool or [{**f,"_source":"catalog-fallback"} for f in foods]
    ranked=[]
    for food in pool:
        scored=score_food(food,time_filter=time_filter,selected_costs=selected_costs,selected_weights=selected_weights,priority=priority,history=history)
        scored["_semantic_relaxations"]=relaxed
        ranked.append(scored)
    return sorted(ranked,key=lambda item:(-item["_score"],total_minutes(item),item["name"]))

def fit_message(food):
    if not food:return ""
    relaxed=food.get("_semantic_relaxations",[])
    if food.get("_exact") and not relaxed:
        return "✨ گزینه سازگار پیدا شد، ولی خارج از غذاهای معمول/انتخابی توست." if food.get("_source")=="catalog-fallback" else "✅ با انتخاب‌های امروزت جور است."
    text="🔎 نزدیک‌ترین پیشنهاد است"
    if food.get("_misses"):text+="؛ "+"، ".join(food["_misses"][:2])
    if relaxed:text+=f". برای پیدا کردن گزینه، {' و '.join(relaxed)} کمی آزاد شد"
    return text+"."

def rank_foods(foods,usual_names,try_names,*,allow_new=True,rng=None):
    rng=rng or random.Random();ranked=[]
    for f in foods:
        if f["name"] in usual_names:s,src=100,"usual"
        elif allow_new and f["name"] in try_names:s,src=72,"try"
        elif not usual_names and not try_names:s,src=50,"catalog"
        else:s,src=(12 if allow_new else -1000),"catalog"
        ranked.append({**f,"_score":s+rng.random()*14,"_source":src})
    return sorted(ranked,key=lambda x:x["_score"],reverse=True)

def recommend_food(foods,usual_names,try_names,*,allow_new=True,rng=None):
    if not foods:return None
    ranked=rank_foods(foods,usual_names,try_names,allow_new=allow_new,rng=rng);rng=rng or random.Random();return rng.choice(ranked[:min(3,len(ranked))])

def suggested_new_foods(foods,usual_names,limit=20):
    usual_families={f.get("family",f.get("category")) for f in foods if f["name"] in usual_names}
    candidates=[f for f in foods if f["name"] not in usual_names]
    candidates.sort(key=lambda f:(f.get("family",f.get("category")) in usual_families,total_minutes(f),0 if f["cost"]=="اقتصادی" else 1))
    picked=[]
    for family in dict.fromkeys(f.get("family",f.get("category")) for f in foods):
        for f in [x for x in candidates if x.get("family",x.get("category"))==family][:2]:
            if f["name"] not in picked:picked.append(f["name"])
    for f in candidates:
        if len(picked)>=limit:break
        if f["name"] not in picked:picked.append(f["name"])
    return picked[:limit]
