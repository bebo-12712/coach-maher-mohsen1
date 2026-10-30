import streamlit as st
import base64
from datetime import datetime
from supabase import create_client

st.set_page_config(page_title="لوحة تحكم الكابتن", page_icon="🔒", layout="wide")

# ============================================================
# 🔥 إعدادات Supabase (غيرهم لبيانات المشروع الجديد)
# ============================================================
SUPABASE_URL = "https://yiassgywpdgdwlcavbch.supabase.co"  # 👈 غير ده للرابط الجديد
SUPABASE_KEY = "sb_publishable_UIGOw-9Q2Qg2S7Yb8MAgNg_VOGdntyl"  # 👈 غير ده للمفتاح الجديد
TABLE_NAME = "coach_data"
ADMIN_PASSWORD = "mohsen123"

LOGIN_BG_IMAGE = "https://i.postimg.cc/NMQ9rC6x/Screenshot-20261027-212455-Google.jpg"


# ============================================================
# الاتصال بـ Supabase
# ============================================================
@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


client = init_supabase()


# ============================================================
# دوال قاعدة البيانات
# ============================================================
def get_default_data():
    return {
        "coach": {"name": "كابتن محسن", "photo": ""},
        "trainer": {"name": "المدرب المساعد", "photo": ""},
        "schedule": [],
        "users": {},
        "last_update_msg": "",
        "last_update_time": "",
        "motivation_msg": "مجهود عظيم = تدريبات كتير! استمر ولا تتوقف. 💪"
    }


def load_data():
    try:
        response = client.table(TABLE_NAME).select("*").eq("id", 1).execute()
        if response.data:
            data = response.data[0]["content"]
            for s in data.get("schedule", []):
                if "booked_by" not in s: s["booked_by"] = []
                if "video_url" not in s: s["video_url"] = ""
                if "category" not in s: s["category"] = "Normal"
                if "type" not in s: s["type"] = "جروب"
                if "price" not in s: s["price"] = ""
            return data
        else:
            default_data = get_default_data()
            client.table(TABLE_NAME).insert({"id": 1, "content": default_data}).execute()
            return default_data
    except Exception as e:
        st.error(f"مشكلة في الاتصال بقاعدة البيانات: {e}")
        return get_default_data()


def save_data(data):
    try:
        client.table(TABLE_NAME).update({"content": data}).eq("id", 1).execute()
    except Exception as e:
        st.error(f"فشل حفظ البيانات: {e}")


if "data" not in st.session_state:
    st.session_state.data = load_data()

if "editing_index" not in st.session_state:
    st.session_state.editing_index = None

# ✅ حفظ تسجيل الدخول (عشان الريفريش)
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = True if "admin" in st.query_params else False


# ============================================================
# التصميم
# ============================================================
def set_bg_image(src):
    if not src: return
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{src}");
        background-size: cover; 
        background-repeat: no-repeat;
        background-position: center top; 
        background-attachment: fixed;
        direction: rtl;
    }}
    [data-testid="stAppViewContainer"] {{
        background-color: rgba(15, 23, 42, 0.85); 
    }}
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
<style>
    [data-testid="stAppDeployButton"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }

    .stApp { background-color: #050505; direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    h1, h2, h3 { color: #00e5ff !important; font-weight: 800;}

    .big-title { font-size: 2.5rem; font-weight: 900; color: #00e5ff; text-shadow: 0px 0px 10px rgba(0, 229, 255, 0.5); }
    .sub { color: #ffffff; font-weight: 600;}
        p, span, div, label {
        color: #ffffff !important;
    }

    .stButton>button { background: linear-gradient(90deg, #00e5ff, #00ff88) !important; color: #000 !important; font-weight: 800 !important; border: none !important; border-radius: 10px !important; transition: 0.3s !important; }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);}

    .auth-box { background: rgba(17, 24, 39, 0.95); padding: 40px; border-radius: 20px; border: 2px solid #00e5ff; box-shadow: 0 0 30px rgba(0, 229, 255, 0.2); }

    /* تنسيق شريط الحجوزات الأخضر */
    .booked-bar { background-color: #10b981; color: #000; padding: 10px 15px; border-radius: 8px; font-weight: 800; font-size: 1.1rem; margin-top: 10px; display: inline-block; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# شاشة تسجيل دخول الأدمن
# ============================================================
def show_admin_login():
    set_bg_image(LOGIN_BG_IMAGE)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.markdown("<div class='big-title' style='text-align:center;'>🔒 لوحة تحكم الكابتن</div>",
                    unsafe_allow_html=True)
        st.markdown(
            "<div class='sub' style='text-align:center;'>أهلاً بك يا كابتن محسن، يرجى إدخال كلمة المرور</div><br>",
            unsafe_allow_html=True)

        pw = st.text_input("كلمة المرور", type="password", key="admin_pw")
        if st.button("دخول", type="primary", use_container_width=True):
            if pw == ADMIN_PASSWORD:
                st.session_state.admin_logged = True
                st.query_params["admin"] = "true"  # 👈 حفظ في الرابط
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة.")
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# لوحة تحكم الأدمن
# ============================================================
def show_admin_dashboard():
    data = st.session_state.data
    set_bg_image(LOGIN_BG_IMAGE)

    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown("<div class='big-title'>🔒 لوحة تحكم الكابتن</div>", unsafe_allow_html=True)
    with c2:
        if st.button("تسجيل خروج", use_container_width=True):
            st.session_state.admin_logged = False
            st.query_params.clear()  # 👈 مسح الحفظ عند الخروج
            st.rerun()

    st.markdown("---")

    tab_alerts, tab_add, tab_manage = st.tabs([
        "📢 التنبيهات والرسائل",
        "➕ إضافة تدريب",
        "📝 إدارة الحجوزات"
    ])

    # ================= تبويب 1: التنبيهات =================
    with tab_alerts:
        st.subheader("✍️ تعديل الرسالة التحفيزية")
        with st.form("motivation_form"):
            new_motivation = st.text_input("الجملة التحفيزية", value=data.get("motivation_msg", ""))
            if st.form_submit_button("حفظ الجملة", type="primary"):
                data["motivation_msg"] = new_motivation
                save_data(data)
                st.success("تم حفظ الرسالة!")
                st.rerun()

        st.divider()
        st.subheader("📢 إرسال تنبيه للاعبين")
        with st.form("alert_form"):
            alert_msg = st.text_input("نص التنبيه")
            if st.form_submit_button("إرسال التنبيه", type="primary"):
                data["last_update_msg"] = alert_msg
                data["last_update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                save_data(data)
                st.success("تم إرسال التنبيه!")
                st.rerun()

        if data.get("last_update_msg"):
            if st.button("🗑️ مسح التنبيه الحالي"):
                data["last_update_msg"] = ""
                data["last_update_time"] = ""
                save_data(data)
                st.rerun()

    # ================= تبويب 2: إضافة تدريب =================
    with tab_add:
        st.subheader("➕ إضافة خطة تدريب جديدة")
        c1, c2, c3 = st.columns(3)
        with c1:
            day = st.selectbox("اليوم", ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"])
        with c2:
            time = st.text_input("الوقت")
        with c3:
            place = st.text_input("المكان")

        col_cat, col_type, col_price = st.columns(3)
        with col_cat:
            category = st.selectbox("الفئة", ["Normal", "Elite"])
        with col_type:
            tr_type = st.selectbox("النوع", ["جروب", "برايفت"])
        with col_price:
            price = st.text_input("السعر (مثال: 200 جنيه)")

        video_url = st.text_input("رابط فيديو التمرين (اختياري)")

        if st.button("إضافة الخطة", type="primary"):
            if time.strip() and place.strip():
                data["schedule"].append(
                    {"day": day, "time": time.strip(), "place": place.strip(), "category": category, "type": tr_type,
                     "price": price.strip(), "booked_by": [], "video_url": video_url.strip()})
                save_data(data)
                st.success("تم إضافة الخطة بنجاح!")
                st.rerun()
            else:
                st.error("أدخل الوقت والمكان.")

    # ================= تبويب 3: إدارة الحجوزات =================
    with tab_manage:
        st.subheader("📝 إدارة الخطط والحجوزات")
        if not data["schedule"]:
            st.info("لا توجد خطط حالياً.")

        for i, s in enumerate(data["schedule"]):
            if st.session_state.editing_index == i:
                st.markdown(f"**تعديل: {s['day']}**")
                ec1, ec2, ec3 = st.columns(3)
                days_list = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
                try:
                    day_idx = days_list.index(s["day"])
                except:
                    day_idx = 0
                with ec1:
                    new_day = st.selectbox("اليوم", days_list, index=day_idx, key=f"edit_day_{i}")
                with ec2:
                    new_time = st.text_input("الوقت", value=s["time"], key=f"edit_time_{i}")
                with ec3:
                    new_place = st.text_input("المكان", value=s["place"], key=f"edit_place_{i}")

                col_ecat, col_etype, col_eprice = st.columns(3)
                cat_list = ["Normal", "Elite"]
                try:
                    cat_idx = cat_list.index(s.get("category", "Normal"))
                except:
                    cat_idx = 0
                with col_ecat:
                    new_cat = st.selectbox("الفئة", cat_list, index=cat_idx, key=f"edit_cat_{i}")

                type_list = ["جروب", "برايفت"]
                try:
                    type_idx = type_list.index(s.get("type", "جروب"))
                except:
                    type_idx = 0
                with col_etype:
                    new_tr_type = st.selectbox("النوع", type_list, index=type_idx, key=f"edit_type_{i}")

                with col_eprice:
                    new_price = st.text_input("السعر", value=s.get("price", ""), key=f"edit_price_{i}")

                new_video = st.text_input("رابط الفيديو", value=s.get("video_url", ""), key=f"edit_vid_{i}")

                if st.button("حفظ", key=f"save_edit_{i}"):
                    data["schedule"][i].update(
                        {"day": new_day, "time": new_time.strip(), "place": new_place.strip(), "category": new_cat,
                         "type": new_tr_type, "price": new_price.strip(), "video_url": new_video.strip()})
                    save_data(data)
                    st.session_state.editing_index = None
                    st.rerun()
                if st.button("إلغاء", key=f"cancel_edit_{i}"):
                    st.session_state.editing_index = None
                    st.rerun()
                st.divider()
            else:
                cc1, cc2, cc3 = st.columns([4, 1, 1])
                with cc1:
                    st.markdown(f"**{s['day']}** — {s['time']} — {s['place']}")
                    st.markdown(
                        f"<span style='color:#ffcc00; font-weight:bold;'>📌 {s.get('category')} ({s.get('type')}) - 💰 {s.get('price', 'غير محدد')}</span>",
                        unsafe_allow_html=True)

                    # 👇 عرض الحجوزات بشكل بارز جداً
                    booked_names = s.get("booked_by", [])
                    if booked_names:
                        st.markdown(f"<div class='booked-bar'>👥 اللاعبين اللي حجزوا: {' - '.join(booked_names)}</div>",
                                    unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='sub' style='margin-top: 10px;'>لا يوجد حجوزات حتى الآن.</div>",
                                    unsafe_allow_html=True)

                with cc2:
                    if st.button("تعديل ✏️", key=f"edit_btn_{i}"):
                        st.session_state.editing_index = i
                        st.rerun()
                with cc3:
                    if st.button("حذف 🗑️", key=f"del_{i}"):
                        data["schedule"].pop(i)
                        save_data(data)
                        st.session_state.editing_index = None
                        st.rerun()


# ============================================================
# الراوتر (Router)
# ============================================================
if st.session_state.admin_logged:
    show_admin_dashboard()
else:
    show_admin_login()