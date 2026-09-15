import streamlit as st

from streamlit_foods import CATEGORIES, FOODS
from streamlit_logic import (
    filter_foods,
    format_minutes,
    recommend_food,
    suggested_new_foods,
    total_minutes,
)

st.set_page_config(page_title="چی بپزم؟", page_icon="🍲", layout="centered")

st.markdown(
    """
    <style>
    html, body, [class*="css"] { direction: rtl; text-align: right; }
    .stApp { background: #f8f5ee; }
    .block-container { max-width: 760px; padding-top: 1.2rem; padding-bottom: 4rem; }
    h1, h2, h3, p, label, div { font-family: Tahoma, Arial, sans-serif; }
    h1 { font-size: 2.3rem !important; }
    [data-testid="stMetric"] { background: white; border: 1px solid #eadfce; border-radius: 18px; padding: 12px; }
    [data-testid="stForm"] { background: rgba(255,255,255,.72); border: 1px solid #eadfce; border-radius: 22px; padding: 18px; }
    .food-card { background: #fff; border: 1px solid #e7ddcd; border-radius: 24px; padding: 22px; margin: 12px 0; box-shadow: 0 8px 30px rgba(67,52,30,.05); }
    .badge { display: inline-block; background: #eef4ef; color: #285b43; padding: 5px 10px; border-radius: 999px; margin: 2px; font-size: .85rem; }
    .new-badge { display: inline-block; background: #fff0d7; color: #8a5713; padding: 5px 10px; border-radius: 999px; margin: 2px; font-size: .85rem; }
    .muted { color: #756f66; }
    .center { text-align: center; }
    .big-question { font-size: 1.1rem; font-weight: 700; margin-top: .5rem; }
    div.stButton > button, div[data-testid="stFormSubmitButton"] > button { min-height: 50px; border-radius: 16px; font-weight: 800; }
    </style>
    """,
    unsafe_allow_html=True,
)

DEFAULT_USUAL = {
    "قورمه‌سبزی",
    "قیمه",
    "زرشک‌پلو با مرغ",
    "عدس‌پلو",
    "ماکارونی",
    "کتلت",
    "کوکو سبزی",
    "املت گوجه",
}

for key, value in {
    "profile_ready": False,
    "usual_foods": set(),
    "try_foods": set(),
    "suggested_food": None,
    "people": 4,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


def render_profile_setup():
    st.title("🍲 چی بپزم؟")
    st.subheader("اول برنامه را با غذاهای خودت آشنا کنیم")
    st.write("از لیست زیر فقط غذاهایی را انتخاب کن که معمولاً در خانه می‌پزی. لازم نیست همه را انتخاب کنی.")

    selections = set()
    with st.form("usual_foods_form"):
        for category in CATEGORIES:
            names = [f["name"] for f in FOODS if f["category"] == category]
            defaults = [name for name in names if name in DEFAULT_USUAL]
            chosen = st.multiselect(category, names, default=defaults, key=f"usual_{category}")
            selections.update(chosen)

        people = st.number_input("معمولاً برای چند نفر غذا می‌پزی؟", min_value=1, max_value=12, value=4, step=1)
        saved = st.form_submit_button("ذخیره و ادامه", use_container_width=True, type="primary")

    if saved:
        if len(selections) < 3:
            st.warning("حداقل ۳ غذایی که معمولاً می‌پزی انتخاب کن تا پیشنهادها معنی‌دارتر شوند.")
        else:
            st.session_state.usual_foods = selections
            st.session_state.people = int(people)
            st.session_state.profile_ready = True
            st.rerun()


def render_try_foods_setup():
    usual = st.session_state.usual_foods
    suggestions = suggested_new_foods(FOODS, usual, limit=10)
    st.markdown("### دوست داری گاهی چه غذاهای دیگری را هم امتحان کنی؟")
    st.caption("این‌ها غذای اصلی برنامه نمی‌شوند؛ فقط گاهی، مثلاً هفته‌ای یکی دو بار، می‌توانند وارد پیشنهاد شوند.")
    chosen = st.multiselect("غذاهای پیشنهادی برای امتحان", suggestions, default=list(st.session_state.try_foods))
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ذخیره این انتخاب‌ها", use_container_width=True):
            st.session_state.try_foods = set(chosen)
            st.success("ذخیره شد.")
    with col2:
        if st.button("فعلاً نمی‌خوام", use_container_width=True):
            st.session_state.try_foods = set()
            st.success("باشه؛ فعلاً فقط از غذاهای معمولت پیشنهاد می‌دهم.")


def source_label(food):
    if food.get("_source") == "try":
        return '<span class="new-badge">✨ برای امتحان</span>'
    if food.get("_source") == "usual":
        return '<span class="badge">🏠 از غذاهای معمول خودت</span>'
    return '<span class="badge">🍽️ از فهرست غذاها</span>'


def render_food(food):
    total = total_minutes(food)
    st.markdown(
        f"""
        <div class="food-card">
          {source_label(food)}
          <h2 style="margin-top:12px">{food['name']}</h2>
          <span class="badge">{food['category']}</span>
          <span class="badge">{food['weight']}</span>
          <span class="badge">{food['cost']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    a, b, c = st.columns(3)
    a.metric("آماده‌سازی", format_minutes(food["prep"]))
    b.metric("پخت", format_minutes(food["cook"]))
    c.metric("زمان کل", format_minutes(total))

    st.markdown(f"#### مواد اصلی برای حدود {st.session_state.people} نفر")
    scale = st.session_state.people / 4
    st.caption("در این نسخه مقدار دقیق مواد بعداً کامل می‌شود؛ فعلاً مواد اصلی را برای تصمیم‌گیری نشان می‌دهیم.")
    for item in food["ingredients"]:
        st.write(f"• {item}")

    st.info("🛒 تشخیص دقیق «نیاز به خرید دارد یا نه» در مرحله بعد با ثبت مواد موجود در خانه فعال می‌شود.")


def render_main():
    st.title("🍲 چی بپزم؟")
    st.caption(f"بر اساس {len(st.session_state.usual_foods)} غذای معمول تو انتخاب می‌کنم.")

    with st.expander("⚙️ ویرایش غذاهای معمول و غذاهای جدید"):
        st.write("غذاهای معمول:", "، ".join(sorted(st.session_state.usual_foods)))
        if st.session_state.try_foods:
            st.write("برای امتحان:", "، ".join(sorted(st.session_state.try_foods)))
        render_try_foods_setup()
        if st.button("انتخاب غذاهای معمول را از نو انجام بده"):
            st.session_state.profile_ready = False
            st.session_state.suggested_food = None
            st.rerun()

    st.markdown('<div class="big-question">امروز چه شرایطی داری؟</div>', unsafe_allow_html=True)
    with st.form("recommend_form"):
        time_filter = st.radio(
            "⏱ چقدر وقت داری؟",
            ["تا ۳۰ دقیقه", "تا ۱ ساعت", "تا ۱ ساعت و نیم", "تا ۲ ساعت", "مهم نیست"],
            horizontal=True,
            index=4,
        )
        costs = st.multiselect("💰 هزینه", ["اقتصادی", "معمولی", "گران"], placeholder="هرکدام که مناسب است")
        weights = st.multiselect("🥗 سبک یا سنگین؟", ["سبک", "متوسط", "سنگین"], placeholder="می‌توانی چند مورد را هم‌زمان انتخاب کنی")
        categories = st.multiselect("🍽️ چه نوع غذایی؟", CATEGORIES, placeholder="اگر مهم نیست، خالی بگذار")
        allow_new = st.checkbox("✨ گاهی از غذاهایی که برای امتحان انتخاب کرده‌ام هم پیشنهاد بده", value=True)
        submitted = st.form_submit_button("🎲 بگو چی بپزم", use_container_width=True, type="primary")

    if submitted:
        candidates = filter_foods(
            FOODS,
            time_filter=time_filter,
            selected_costs=costs,
            selected_weights=weights,
            selected_categories=categories,
        )
        food = recommend_food(
            candidates,
            set(st.session_state.usual_foods),
            set(st.session_state.try_foods),
            allow_new=allow_new,
        )
        st.session_state.suggested_food = food
        if food is None:
            st.warning("با این ترکیب شرط‌ها غذایی پیدا نکردم. یکی از فیلترها را کمی بازتر کن.")

    if st.session_state.suggested_food:
        render_food(st.session_state.suggested_food)
        if st.button("🔄 یکی دیگه پیشنهاد بده", use_container_width=True):
            # Reuse broad preference pools; exact form state remains visible for the next submit.
            pool = [f for f in FOODS if f["name"] != st.session_state.suggested_food["name"]]
            st.session_state.suggested_food = recommend_food(
                pool,
                set(st.session_state.usual_foods),
                set(st.session_state.try_foods),
                allow_new=True,
            )
            st.rerun()


if not st.session_state.profile_ready:
    render_profile_setup()
else:
    render_main()
