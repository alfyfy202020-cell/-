import streamlit as st
import google.generativeai as genai

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="فاحص قصص سيرفر ريسبكت | Respect RP", 
    page_icon="🛡️", 
    layout="wide"
)

# --- تنسيق وتصميم الواجهة (Custom CSS) ---
st.markdown("""
<style>
    /* خلفية التطبيق العامة */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* تصميم الهيدر / العنوان */
    .main-title {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-title h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.2rem;
    }
    
    .main-title p {
        color: #93c5fd !important;
        margin-top: 8px;
        font-size: 1rem;
    }

    /* مربع إدخال النص */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4) !important;
    }

    /* زر الفحص */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.5) !important;
    }

    /* شاشة تسجيل الدخول */
    .login-box {
        background-color: #1e293b;
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #334155;
        max-width: 450px;
        margin: 50px auto;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
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

# --- الهيدر والعنوان الرئيسية ---
st.markdown("""
<div class="main-title">
    <h1>🛡️ نظام فحص وتدقيق القصص (Respect RP)</h1>
    <p>أداة ذكية مخصصة لتقييم القصص بناءً على شروط وقوانين سيرفر ريسبكت وفحص الذكاء الاصطناعي</p>
</div>
""", unsafe_allow_html=True)

# --- منطقة إدخال النص ---
story = st.text_area("✍️ ألصق القصة المراد فحصها هنا:", height=250, placeholder="ضع نص القصة هنا...")

system_prompt = """قم بمراجعة القصة وتوفير التقييم بالتنسيق التالي. أنت مدقق مخصص لقصص سيرفر "ريسبكت (Respect RP)" ومستكشف للنصوص التوليدية (AI Detector):

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
"""

if st.button("🚀 فحص القصة الآن"):
    if not api_key:
        st.error("لم يتم العثور على مفتاح API في Secrets. يرجى إضافته من إعدادات التطبيق.")
    elif not story.strip():
        st.warning("الرجاء كتابة أو نسخ القصة أولاً.")
    else:
        with st.spinner("جاري تحليل القصة وفحص الشروط..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-3.6-flash")
                response = model.generate_content(f"{system_prompt}\n\nالقصة المراد فحصها:\n{story}")

                st.markdown("---")
                st.subheader("📋 نتيجة الفحص والتقرير:")
                st.info(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الفحص: {e}")
