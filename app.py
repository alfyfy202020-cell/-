import streamlit as st
from google import genai

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="فاحص قصص سيرفر ريسبكت | Respect RP", 
    page_icon="🔮", 
    layout="wide"
)

# رابط الشعار
LOGO_URL = "logo.png"

# --- تنسيق وتصميم الواجهة وشعار Respect RP ---
st.markdown("""
<style>
    .stApp {
        background-color: #0d0914;
        background-image: radial-gradient(circle at 50% 10%, rgba(109, 40, 217, 0.25) 0%, transparent 60%);
        color: #f3f0ff;
    }
    
    .logo-header {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .logo-header img {
        width: 130px;
        height: auto;
        filter: drop-shadow(0 0 15px rgba(168, 85, 247, 0.8));
    }
    
    .main-title {
        background: linear-gradient(135deg, #4c1d95 0%, #2e1065 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px -5px rgba(124, 58, 237, 0.4);
        margin-bottom: 25px;
        border: 2px solid #7c3aed;
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
        font-size: 2.3rem;
    }
    
    .main-title p {
        color: #ddd6fe !important;
        margin-top: 5px;
        font-size: 1rem;
    }

    label {
        color: #a78bfa !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

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

    .login-box {
        background-color: #140d21;
        padding: 35px;
        border-radius: 20px;
        border: 2px solid #7c3aed;
        max-width: 420px;
        margin: 40px auto;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.9);
    }

    .footer-brand {
        text-align: center;
        margin-top: 35px;
        color: #6b7280;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- نظام كلمة المرور للحماية ---
PASSWORD_SECRET = "Respect112833"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown(f'''
    <div class="login-box">
        <div class="logo-header">
            <img src="{LOGO_URL}" onerror="this.onerror=null; this.src='https://i.imgur.com/vHq0FZX.png';" />
        </div>
        <div class="brand-badge">RESPECT ROLEPLAY</div>
        <h2 style="color: #fff; margin-bottom: 5px;">بوابة الإدارة</h2>
        <p style="color: #a78bfa; margin-bottom: 20px;">نظام الفحص والتدقيق الذكي للقصص</p>
    </div>
    ''', unsafe_allow_html=True)
    
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

# --- عرض الشعار والعنوان الرئيسية ---
st.markdown(f'''
<div class="logo-header">
    <img src="{LOGO_URL}" onerror="this.onerror=null; this.src='https://i.imgur.com/vHq0FZX.png';" />
</div>
<div class="main-title">
    <div class="brand-badge">RESPECT RP OFFICIAL TOOL</div>
    <h1>نظام فحص وتدقيق القصص</h1>
    <p>فحص الكتابة البشرية، مطابقة الشروط، وتقييم سيناريو الرول بلاي</p>
</div>
''', unsafe_allow_html=True)

# --- حقول الإدخال المقسمة ---
col_story, col_pros_cons = st.columns(2)

with col_story:
    story = st.text_area("📝 الخانة الأولى: نص القصة المراد فحصها", height=230, placeholder="ألصق نص القصة هنا...")

with col_pros_cons:
    pros_cons = st.text_area("💡 الخانة الثانية: إيجابيات وسلبيات الشخصية", height=230, placeholder="ألصق إيجابيات وسلبيات الشخصية هنا...")

system_prompt = """أنت المدقق الرسمي المخصص لقصص سيرفر "ريسبكت RP" (Respect Roleplay). قم بتحليل القصة وإيجابيات/سلبيات الشخصية بدقة عالية جداً وتقديم التقرير بالتنسيق المحدد أسفله:

1. 🔍 **فحص أسلوب الكتابة (ذكاء اصطناعي أم بشري؟):**
   - افحص الأسلوب بعناية فائقة (الكتابة البشرية تتميز بالأسلوب السردي المباشر، وجود أخطاء إملائية/لغوية خفيفة، والتطرق لتفاصيل عامية أو بسيطة. بينما الذكاء الاصطناعي يميل للمصطلحات الرسمية المعقدة والترتيب التوليدي المتناسق بزيادة).
   - التقييم: (كتابة بشرية طبيعية / مكتوبة بالذكاء الاصطناعي).
   - السبب: (في سطر واحد فقط).

2. 🎮 **ملائمة الرول بلاي (Roleplay Viability):**
   - هل الأحداث قابلة للتمثيل والتطبيق الفعلي داخل الجيم بلاي بدون الاعتماد على اللوقات (Logs) أو أشياء غير واقعية برمجياً؟
   - النتيجة: (مقبولة للرول بلاي / غير قابلة للتمثيل).

3. 📌 **النتيجة النهائية:**
   - (مقبولة) أو (مرفوضة).

4. 📋 **تفصيل شروط سيرفر ريسبكت:**
   - [مستوفى / غير مستوفى] : (الاسم، سنة الميلاد، والمنشأ - يكتفى بذكر اسم واحد فقط)
   - [مستوفى / غير مستوفى] : (الواقعية والتسلسل العمري والأحداث)
   - [مستوفى / غير مستوفى] : (حدث محوري/مؤلم في الطفولة أثر على الشخصية)
   - [مستوفى / غير مستوفى] : (الاهتمامات، الطموحات، السلبيات والإيجابيات ومدى توافقها مع النص)
   - [مستوفى / غير مستوفى] : (خلو القصة من أحداث داخل السيرفر)

5. 💡 **تقييم ومطابقة الإيجابيات والسلبيات المدخلة:**
   - مدى توافق الإيجابيات والسلبيات المدخلة في الخانة الثانية مع أحداث القصة وواقعية التمثيل.

6. 🎙️ **كلام مختصر للرفض (لقراءته للشخص صوتاً فوراً):**
   - اكتب جملتين فقط مختصرة ومباشرة يمكن قراءتها للشخص في روم الصوت لتوضيح سبب رفض القصة وما يحتاج تعديله بدون إطالة.
"""

if st.button("🔮 فحص القصة والتقييم"):
    if not api_key:
        st.error("لم يتم العثور على مفتاح API في Secrets. يرجى إضافته من إعدادات التطبيق.")
    elif not story.strip():
        st.warning("الرجاء كتابة أو نسخ القصة في الخانة الأولى أولاً.")
    else:
        with st.spinner("جاري تدقيق القصة والإيجابيات والسلبيات..."):
            try:
                client = genai.Client(api_key=api_key)
                combined_content = f"{system_prompt}\n\n--- نص القصة ---\n{story}\n\n--- إيجابيات وسلبيات الشخصية ---\n{pros_cons if pros_cons.strip() else 'لم يتم كتابة إيجابيات وسلبيات'}"
                
                # استخدام نموذج gemini-2.5-flash كنموذج رئيسي
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=combined_content,
                    )
                except Exception:
                    # الاحتياطي في حال طلب النظام الاصدار المحدث
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-latest",
                        contents=combined_content,
                    )

                st.markdown("---")
                st.markdown("### 📊 تقرير إدارة Respect RP:")
                st.info(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الفحص: {e}")

st.markdown("""
<div class="footer-brand">
    Respect RP - Administration Management System
</div>
""", unsafe_allow_html=True)
