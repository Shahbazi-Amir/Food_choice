import streamlit as st

from streamlit_foods import FAMILIES, METHODS, FOODS
from streamlit_logic import fit_message, format_minutes, rank_nearest, suggested_new_foods, total_minutes
from streamlit_recipe import recipe_for

st.set_page_config(page_title="چی بپزم؟", page_icon="🍲", layout="centered")
st.markdown("""
<style>
html, body, [class*="css"] { direction: rtl; text-align: right; }
.stApp { background: #f8f5ee; }
.block-container { max-width: 820px; padding-top: 1.2rem; padding-bottom: 4rem; }
h1,h2,h3,p,label,div { font-family: Tahoma,Arial,sans-serif; }
[data-testid="stMetric"] { background:white;border:1px solid #eadfce;border-radius:18px;padding:12px; }
[data-testid="stForm"] { background:rgba(255,255,255,.72);border:1px solid #eadfce;border-radius:22px;padding:18px; }
.food-card { background:#fff;border:1px solid #e7ddcd;border-radius:24px;padding:22px;margin:12px 0;box-shadow:0 8px 30px rgba(67,52,30,.05); }
.badge { display:inline-block;background:#eef4ef;color:#285b43;padding:5px 10px;border-radius:999px;margin:2px;font-size:.85rem; }
.new-badge { display:inline-block;background:#fff0d7;color:#8a5713;padding:5px 10px;border-radius:999px;margin:2px;font-size:.85rem; }
div.stButton > button, div[data-testid="stFormSubmitButton"] > button { min-height:50px;border-radius:16px;font-weight:800; }
</style>
""", unsafe_allow_html=True)

DEFAULT_USUAL={"قورمه‌سبزی","قیمه","زرشک‌پلو با مرغ","عدس‌پلو","ماکارونی","کتلت","کوکو سبزی","املت گوجه","کباب تابه‌ای","لوبیاپلو","آش رشته","میرزا قاسمی"}
for key,value in {"profile_ready":False,"usual_foods":set(),"try_foods":set(),"suggested_food":None,"people":4,"ranked":[],"rank_index":0,"history":[]}.items():
    if key not in st.session_state: st.session_state[key]=value


def render_profile_setup():
    st.title("🍲 چی بپزم؟")
    st.subheader("اول برنامه را با غذاهای خودت آشنا کنیم")
    st.write(f"از کاتالوگ {len(FOODS)} غذایی، هر غذایی را که معمولاً در خانه می‌پزی انتخاب کن.")
    selections=set()
    with st.form("usual_foods_form"):
        for family in FAMILIES:
            names=[f["name"] for f in FOODS if f["family"]==family]
            defaults=[name for name in names if name in DEFAULT_USUAL]
            chosen=st.multiselect(family,names,default=defaults,key=f"usual_{family}")
            selections.update(chosen)
        people=st.number_input("معمولاً برای چند نفر غذا می‌پزی؟",min_value=1,max_value=12,value=4,step=1)
        saved=st.form_submit_button("ادامه",use_container_width=True,type="primary")
    if saved:
        if len(selections)<3: st.warning("حداقل ۳ غذا انتخاب کن.")
        else:
            st.session_state.usual_foods=selections;st.session_state.people=int(people);st.session_state.profile_ready=True;st.rerun()


def render_try_foods_setup():
    suggestions=suggested_new_foods(FOODS,st.session_state.usual_foods,limit=24)
    st.markdown("### دوست داری این‌ها را هم گاهی امتحان کنی؟")
    chosen=st.multiselect("غذاهای پیشنهادی برای امتحان",suggestions,default=list(st.session_state.try_foods))
    if st.button("ذخیره انتخاب‌های جدید",use_container_width=True):
        st.session_state.try_foods=set(chosen);st.success("ذخیره شد.")


def source_label(food):
    if food.get("_source")=="try": return '<span class="new-badge">✨ برای امتحان</span>'
    if food.get("_source")=="usual": return '<span class="badge">🏠 از غذاهای معمول خودت</span>'
    return '<span class="new-badge">✨ پیشنهاد جدید سازگار</span>'


def render_food(food):
    recipe=recipe_for(food)
    methods=" / ".join(food.get("methods",[]))
    st.markdown(f"<div class='food-card'>{source_label(food)}<h2 style='margin-top:12px'>{food.get('emoji','🍽️')} {food['name']}</h2><span class='badge'>{food['family']}</span><span class='badge'>{methods}</span><span class='badge'>{food['weight']}</span><span class='badge'>{food['cost']}</span></div>",unsafe_allow_html=True)
    st.info(fit_message(food))
    a,b,c=st.columns(3)
    a.metric("آماده‌سازی",format_minutes(food["prep"]));b.metric("پخت",format_minutes(food["cook"]));c.metric("زمان کل",format_minutes(total_minutes(food)))
    st.markdown(f"#### 🧺 مواد اصلی برای حدود {st.session_state.people} نفر")
    for item in food["ingredients"]: st.write(f"• {item}")
    st.markdown("#### 👩‍🍳 مراحل پخت")
    for i,step in enumerate(recipe["steps"],1): st.write(f"{i}. {step}")
    st.markdown("#### 🔥 روش‌های قابل پخت")
    for variant in recipe["variants"]: st.write(f"• {'روش اصلی' if variant['primary'] else 'روش جایگزین'}: **{variant['method']}**")
    st.markdown("#### 💡 نکته‌ها")
    for note in recipe["notes"]: st.write(f"• {note}")
    st.caption("🖼️ جای تصویر واقعی/تولیدشده هر غذا در UI در نظر گرفته شده و فعلاً نشان تصویری دسته نمایش داده می‌شود.")


def render_main():
    st.title("🍲 چی بپزم؟")
    st.caption(f"از {len(st.session_state.usual_foods)} غذای معمول و {len(st.session_state.try_foods)} غذای انتخاب‌شده برای امتحان پیشنهاد می‌دهم.")
    with st.expander("⚙️ ویرایش پروفایل غذایی"):
        render_try_foods_setup()
        if st.button("غذاهای معمول را از نو انتخاب کن"):
            st.session_state.profile_ready=False;st.session_state.suggested_food=None;st.rerun()

    with st.form("recommend_form"):
        priority_label=st.radio("⭐ مهم‌ترین معیار امروز",["تعادل همه","زمان","هزینه","سبک بودن","نوع غذا"],horizontal=True)
        priority={"تعادل همه":"balanced","زمان":"time","هزینه":"cost","سبک بودن":"weight","نوع غذا":"category"}[priority_label]
        time_filter=st.radio("⏱ چقدر وقت داری؟",["مهم نیست","تا ۳۰ دقیقه","تا ۱ ساعت","تا ۱ ساعت و نیم","تا ۲ ساعت"],horizontal=True)
        costs=st.multiselect("💰 هزینه",["اقتصادی","معمولی","گران"])
        weights=st.multiselect("🥗 سبک یا سنگین؟",["سبک","متوسط","سنگین"])
        families=st.multiselect("🍽️ نوع غذا",FAMILIES,help="نوع غذا با روش پخت فرق دارد.")
        methods=st.multiselect("🔥 روش پخت",METHODS,help="مثلاً اگر گریل/منقل انتخاب شود، غذای تابه‌ای ناسازگار پیشنهاد نمی‌شود.")
        allow_new=st.checkbox("✨ از غذاهای جدیدی که خودم انتخاب کرده‌ام هم استفاده کن",value=True)
        submitted=st.form_submit_button("🎲 بگو چی بپزم",use_container_width=True,type="primary")

    if submitted:
        ranked=rank_nearest(FOODS,set(st.session_state.usual_foods),set(st.session_state.try_foods),allow_new=allow_new,time_filter=time_filter,selected_costs=costs,selected_weights=weights,selected_families=families,selected_methods=methods,priority=priority,history=st.session_state.history)
        st.session_state.ranked=ranked;st.session_state.rank_index=0;st.session_state.suggested_food=ranked[0] if ranked else None

    if st.session_state.suggested_food:
        render_food(st.session_state.suggested_food)
        col1,col2=st.columns(2)
        with col1:
            if st.button("✅ همینو می‌پزم",use_container_width=True):
                name=st.session_state.suggested_food["name"];st.session_state.history=[name]+[x for x in st.session_state.history if x!=name];st.success("ثبت شد؛ نوش جان 🌿")
        with col2:
            if st.button("🔄 یکی دیگه",use_container_width=True):
                ranked=st.session_state.ranked
                if ranked:
                    st.session_state.rank_index=(st.session_state.rank_index+1)%len(ranked);st.session_state.suggested_food=ranked[st.session_state.rank_index];st.rerun()

if not st.session_state.profile_ready:render_profile_setup()
else:render_main()
