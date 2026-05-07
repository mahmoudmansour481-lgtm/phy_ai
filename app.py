import streamlit as st
import google.generativeai as genai

# إعداد الواجهة
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# التأكد من المفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح ناقص في الـ Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# محاولة تشغيل الموديل بأكثر من اسم لضمان التوافق
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

# شات بسيط للتجربة
if prompt := st.chat_input("اسألني سؤال في الفيزياء..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"عذراً، فيه مشكلة: {str(e)}")
