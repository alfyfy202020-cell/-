import streamlit as st
from google import genai

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="فاحص قصص سيرفر ريسبكت | Respect RP", 
    page_icon="🛡️", 
    layout="wide"
)

# --- تنسيق وتصميم الواجهة (Purple Dark Theme) ---
st.markdown("""
<style>
    /* خلفية التطبيق العامة */
    .stApp {
        background-color: #0d0914;
        color: #f3f0ff;
    }
    
    /* تصميم الهيدر / العنوان */
    .main-title {
        background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%);
        padding: 28px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 30px -5px rgba(109, 40, 217, 0.5);
        margin-bottom: 25px;
        border: 1px solid rgba(167, 139, 250, 0.3);
    }
    
    .main-title h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.3rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .main-title p {
        color: #ddd6fe !important;
        margin-top: 10px;
        font-size: 1.1rem;
    }

    /* عناوين ومسميات الحقول */
    label {
        color: #c4b5fd !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    /* مربع إدخال النص */
    .stTextArea textarea {
        background-color: #181024 !important;
        color: #ffffff !important;
        border: 1.5px solid #5b21b6 !important;
        border-radius: 12px !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    .stTextArea textarea:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.4) !important;
    }

    /* زر الفحص */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #7c3aed 0%, #6d28d9 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        padding: 14px 24px !important;
        border-radius: 12px !important;
        border: 1px solid #a78bfa !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px 0 rgba(124, 58, 237, 0.4) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px 0 rgba(168, 85, 247, 0.6) !important;
        background: linear-gradient(90deg, #8b5cf6 0%, #7c3aed 100%) !important;
    }

    /* شاشة تسجيل الدخول */
    .login-box {
        background-color: #181024;
        padding: 40px;
        border-radius: 18px;
        border: 1px solid #5b21b6;
        max-width: 450px;
        margin: 50px auto;
        box-shadow: 0 20px 30px -5px rgba(0, 0, 0, 0.8);
    }

    /* تنسيق مربع النتيجة والرسائل */
    .stAlert {
        background-color: #1e1333 !important;
        border: 1px solid #7c3aed !important;
        color: #f3f0ff !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- نظام كلمة المرور للحماية ---
PASSWORD_SECRET = "Respect112833"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("🔒 تسجيل الدخول")
    st.write("نظام فحص وتقييم القصص الخاص بإدارة ريسبكت")
    input_pwd = st.text_input("أدخل كلمة المرور:", type="password")
    if st.button("تسجيل الدخول"):
        if input_pwd == PASSWORD_SECRET:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة!")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- جلب API Key تلقائياً من Secrets ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

# --- الهيدر والعنوان الرئيسي ---
st.markdown("""
<div class="main-title">
    <h1>👾 نظام فحص وتقييم القصص (Respect RP)</h1>
    <p>أداة ذكية مخصصة لتقييم قصص السيرفر وتدقيق الشروط وفحص الذكاء الاصطناعي</p>
</div>
""", unsafe_allow_html=True)

# --- منطقة إدخال النص ---
story = st.text_area("📝 ألصق القصة المراد فحصها هنا:", height=250, placeholder="ضع نص القصة هنا...")

system_prompt = """قم بمراجعة القصة وتوفير التقييم بالتنسيق المحدد أسفله. أنت مدقق مخصص لقصص سيرفر "ريسبكت (Respect RP)" ومستكشف للنصوص التوليدية (AI Detector):

1. **كشف الذكاء الاصطناعي (AI Detection):**
   - حدد نسبة احتمال أن تكون القصة مكتوبة بواسطة الذكاء الاصطناعي (منخفض جداً، متوسط، عالي جداً).
   - اذكر السبب اختصاراً (مثل: أسلوب وتراكيب رسمية جداً، تكرار أنماط الذكاء الاصطناعي، أو أسلوب بشري طبيعي).

2. **النتيجة النهائية:**
   - حدد بوضوح: (مقبولة) أو (مرفوضة).

3. **تفصيل شروط سيرفر ريسبكت:**
   - [مستوفى / غير مستوفى] : (الاسم الثلاثي وسنة الميلاد والمنشأ)
   - [مستوفى / غير مستوفى] : (الواقعية والتسلسل العمري والأحداث)
   - [مستوفى / غير مستوفى] : (حدث محوري/مؤلم في الطفولة أثر على الشخصية)
   - [مستوفى / غير مستوفى] : (الاهتمامات، الطموحات، السلبيات والإيجابيات)
   - [مستوفى / غير مستوفى] : (عدم تحديد الوظيفة أو المسار المباشر والاكتفاء بالتلميح)
   - [مستوفى / غير مستوفى] : (خلو القصة من أحداث داخل السيرفر)

4. **أسباب الرفض والملاحظات (إن وجدت):**
   - وضح النقاط المفقودة والتوجيهات للتعديل بأسلوب مباشر ومختصر.

5. **رسالة الرفض الموجهة للشخص (رسالة إدارية مرتبة وجاهزة للنسخ):**
   - قم بكتابة رسالة ديسكورد محترمة ومرتبة بالنيابة عن إدارة "ريسبكت RP" موجهة للشخص صاحب القصة، تشرح له الرفض بلباقة وتوضح له الأسباب بالتفصيل مع توجيهه لكيفية التعديل ليتمكن من إعادة التقديم. (إذا كانت القصة مقبولة، اكتب رسالة قبول وترحيب به في السيرفر).
"""

if st.button("🔮 فحص القصة الآن"):
    if not api_key:
        st.error("لم يتم العثور على مفتاح API في Secrets. يرجى إضافته من إعدادات التطبيق.")
    elif not story.strip():
        st.warning("الرجاء كتابة أو نسخ القصة أولاً.")
    else:
        with st.spinner("جاري تحليل القصة وفحص الشروط..."):
            try:
                # التهيئة الجديدة للمكتبة
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\n\nالقصة المراد فحصها:\n{story}",
                )

                st.markdown("---")
                st.subheader("📊 نتيجة الفحص والتقرير الإداري:")
                st.info(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الفحص: {e}")
