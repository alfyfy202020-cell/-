import streamlit as st
import google.generativeai as genai

# إعداد واجهة Streamlit
st.set_page_config(page_title="فاحص القصص", layout="wide")

st.title("نظام فحص وتقييم القصص")

# الشريط الجانبي لإدخال API Key
st.sidebar.header("الإعدادات")
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

# إدخال القصة
story = st.text_area("أدخل القصة المراد فحصها هنا:", height=250)

# النص التوجيهي (System Prompt)
system_prompt = """أنت محكّم ومقيّم قصص محترف داخل سيرفر رول بلاي (Roleplay).
قم بفحص القصة التالية بدقة بناءً على الشروط والمعايير التالية واكتب تقريراً مفصلاً باللغة العربية:

1. **النتيجة النهائية**: (مقبول / مراجع للتعديل / مرفوض)
2. **التقييم العام للقصة**.
3. **تفاصيل شروط السيرفر ريسبكت**:
   - (الاسم الثلاثي وسنة الميلاد والمنشأ) : [مستوفي / غير مستوفي]
   - (الواقعية والتسلسل العمري والأحداث) : [مستوفي / غير مستوفي]
   - (حدث محوري/مؤلم في الطفولة أثر على الشخصية) : [مستوفي / غير مستوفي]
   - (الاهتمامات، الطموحات، السلبيات والإيجابيات) : [مستوفي / غير مستوفي]
   - (عدم تحديد الوظيفة أو المسار المباشر والاكتفاء بالتلميح) : [مستوفي / غير مستوفي]
   - (خلو القصة من أحداث داخل السيرفر) : [مستوفي / غير مستوفي]

4. **أسباب الرفض والملاحظات (إن وجدت)**:
   - وضح النقاط المفقودة والتوجيهات للتعديل بأسلوب مباشر ومختصر.
"""

if st.button("فحص القصة الآن"):
    if not api_key:
        st.error("الرجاء إدخال مفتاح API في الشريط الجانبي أولاً.")
    elif not story:
        st.warning("الرجاء كتابة أو نسخ القصة أولاً.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"{system_prompt}\n\nالقصة المراد فحصها:\n{story}")

            st.markdown("---")
            st.subheader("نتيجة الفحص:")
            st.write(response.text)
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
