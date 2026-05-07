import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="مساعد الفيزياء", layout="centered")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# تعريف الموديل بأبسط طريقة
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدمنا الاسم ده لأنه الأكثر توافقاً حالياً
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"فشل في إعداد الجيمناي: {e}")

# واجهة الشات
if prompt := st.chat_input("اسأل مستر جيمي..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"خطأ: {e}")
