import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="فاحص قصص سيرفر ريسبكت", page_icon="🛡️")

# --- نظام حماية التطبيق بكلمة مرور (خاص) ---
PASSWORD_SECRET = "Respect112833"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 نظام فحص قصص ريسبكت - تسجيل الدخول")
    input_pwd = st.text_input("أدخل كلمة المرور للدخول:", type="password")
    if st.button("تسجيل الدخول"):
        if input_pwd == PASSWORD_SECRET:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة!")
    st.stop()

# --- واجهة التطبيق الرئيسية بعد الدخول ---
st.title("🛡️ نظام فحص قصص ريسبكت (Respect RP)")
st.write("أدخل القصة الأساسية من المتطلبات المعتمده لقصص ريسبكت وفحص الذكاء الاصطناعي.")

api_key = st.sidebar.text_input("أدخل Gemini API:", type="password")

story = st.text_area("نص القصة:", height=250)

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

if st.button("فحص القصة الآن"):
    if not api_key:
        st.error("في الشريط الجانبي أولاً الرجاء إدخال مفتاح API.")
    elif not story:
        st.warning("الرجاء كتابة أو نسخ القصة أولاً.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(f"{system_prompt}\n\nالقصة المراد فحصها:\n{story}")

            st.markdown("---")
            st.subheader("نتيجة الفحص:")
            st.write(response.text)
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
