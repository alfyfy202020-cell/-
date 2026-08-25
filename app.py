import streamlit as st
from google import genai

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="فاحص قصص سيرفر ريسبكت | Respect RP", 
    page_icon="👑", 
    layout="wide"
)

# --- تنسيق وتصميم الواجهة وشعارات Respect RP ---
st.markdown("""
<style>
    /* خلفية التطبيق العامة مع شعار مائي خفيف */
    .stApp {
        background-color: #0d0914;
        background-image: radial-gradient(circle at 50% 10%, rgba(109, 40, 217, 0.15) 0%, transparent 60%);
        color: #f3f0ff;
    }
    
    /* تصميم الهيدر وشعار ريسبكت */
    .main-title {
        background: linear-gradient(135deg, #4c1d95 0%, #2e1065 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px -5px rgba(124, 58, 237, 0.4);
        margin-bottom: 30px;
        border: 2px solid #7c3aed;
        position: relative;
    }
    
    .brand-badge {
        background: #7c3aed;
        color: #fff;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 2px;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.6);
    }

    .main-title h1 {
        color: #ffffff !important;
        font-weight: 900;
        margin: 5px 0;
        font-size: 2.5rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.7);
    }
    
    .main-title p {
        color: #ddd6fe !important;
        margin-top: 8px;
        font-size: 1.1rem;
    }

    /* عناوين ومسميات الحقول */
    label {
        color: #a78bfa !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* مربع إدخال النص */
    .stTextArea textarea {
        background-color: #140d21 !important;
        color: #ffffff !important;
        border: 2px solid #5b21b6 !important;
        border-radius: 14px !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    .stTextArea textarea:focus {
        border-color: #c084fc !important;
        box-shadow: 0 0 15px rgba(192, 132, 252, 0.4) !important;
    }

    /* زر الفحص */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #7c3aed 0%, #5b21b6 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.25rem !important;
        padding: 16px 24px !important;
        border-radius: 14px !important;
        border: 1px solid #c084fc !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px 0 rgba(124, 58, 237, 0.5) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px 0 rgba(192, 132, 252, 0.7) !important;
        background: linear-gradient(90deg, #9333ea 0%, #7c3aed 100%) !important;
    }

    /* شاشة تسجيل الدخول */
    .login-box {
        background-color: #140d21;
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #7c3aed;
        max-width: 450px;
        margin: 50px auto;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.9);
    }

    /* الملاحظات والشعار السفلي */
    .footer-brand {
        text-align: center;
        margin-top: 40px;
        color: #6b7280;
        font-size: 0.9rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- نظام كلمة المرور للحماية ---
PASSWORD_SECRET = "Respect112833"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("""
    <div class="login-box">
        <div class="brand-badge">RESPECT ROLEPLAY</div>
        <h2 style="color: #fff; margin-bottom: 10px;">👑 بوابة الإدارة</h2>
        <p style="color: #a78bfa; margin-bottom: 25px;">نظام الفحص الذكي والتقييم المتقدم للقصص</p>
    </div>
    """, unsafe_allow_html=True)
    
    input_pwd = st.text_input("🔑 أدخل كلمة المرور:", type="password")
    if st.button("تسجيل الدخول"):
        if input_pwd == PASSWORD_SECRET:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة!")
    st.stop()

# --- جلب API Key تلقائياً من Secrets ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

# --- الهيدر وشعارات ريسبكت ---
st.markdown("""
<div class="main-title">
    <div class="brand-badge">👑 RESPECT RP OFFICIAL TOOL</div>
    <h1>✨ نظام فحص وتقييم القصص</h1>
    <p>تدقيق احترافي للشروط، كشف دقيق للذكاء الاصطناعي، وتقييم إمكانية تطبيق الرول بلاي</p>
</div>
""", unsafe_allow_html=True)

# --- منطقة إدخال النص ---
story = st.text_area("📝 ألصق القصة المراد فحصها هنا:", height=260, placeholder="ضع نص القصة هنا للتحليل والشروط...")

# Prompt محسن بالكامل لزيادة دقة الـ AI وفحص صلاحية الرول بلاي
system_prompt = """أنت المدقق الرسمي المخصص لقصص سيرفر "ريسبكت RP" (Respect Roleplay). قم بتحليل القصة بدقة عالية جداً وتقديم النتيجة بالشكل المباشر والمختصر الموضح أسفله:

1. 🔍 **كشف الذكاء الاصطناعي (AI Detector - دقة عالية):**
   - حلل القصة بعناية (افحص التناغم اللغوي، التكرار السطحي، الهيكلة التوليدية المعتادة، والمفردات الرسمية الفائقة).
   - الاحتمالية: (منخفض جداً "بشري" / متوسط / عالي جداً "مكتوبة بـ AI").
   - السبب: (سطر واحد فقط بذكر الأدلة مثل: مفردات توليدية، أسلوب بشري عاطفي، أو تراكيب جاهزة).

2. 🎮 **ملائمة الرول بلاي (Roleplay Viability):**
   - هل سيناريو القصة وأحداث الشخصية قابلة للتطبيق والتمثيل الفعلي داخل الجيم بلاي بالسيرفر بدون الاعتماد على اللوقات (Logs) أو أحداث وهمية لا تدعمها المودات؟
   - النتيجة: (مقبول رول بلاي / غير قابل للتمثيل - يعتمد على اللوقات أو سيناريو غير واقعي).

3. 📌 **النتيجة النهائية:**
   - (مقبولة) أو (مرفوضة).

4. 📋 **تفصيل شروط سيرفر ريسبكت:**
   - [مستوفى / غير مستوفى] : (الاسم، سنة الميلاد، والمنشأ - يكتفى بذكر اسم واحد فقط)
   - [مستوفى / غير مستوفى] : (الواقعية والتسلسل العمري والأحداث)
   - [مستوفى / غير مستوفى] : (حدث محوري/مؤلم في الطفولة أثر على الشخصية)
   - [مستوفى / غير مستوفى] : (الاهتمامات، الطموحات، السلبيات والإيجابيات)
   - [مستوفى / غير مستوفى] : (خلو القصة من أحداث داخل السيرفر)

5. 🎙️ **ملخص الرفض والملاحظات الصوتية (مختصر جداً):**
   - اكتب أسباب الرفض بأسلوب نقاط مختصر ومباشر جداً ليتم قراءتها للشخص صوتياً في الروم (بدون مقدمات).
"""

if st.button("👑 فحص القصة والتقييم"):
    if not api_key:
        st.error("لم يتم العثور على مفتاح API في Secrets. يرجى إضافته من إعدادات التطبيق.")
    elif not story.strip():
        st.warning("الرجاء كتابة أو نسخ القصة أولاً.")
    else:
        with st.spinner("👑 جاري تدقيق الشروط وفحص الذكاء الاصطناعي والرول بلاي..."):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"{system_prompt}\n\nالقصة المراد فحصها:\n{story}",
                )

                st.markdown("---")
                st.markdown("### 📊 تقرير إدارة Respect RP:")
                st.info(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الفحص: {e}")

# الفوتر السفلي
st.markdown("""
<div class="footer-brand">
    👑 Respect RP - Administration Management System
</div>
""", unsafe_allow_html=True)
