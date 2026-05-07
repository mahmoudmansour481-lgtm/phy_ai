import streamlit as st
import google.generativeai as genai

st.title("⚛️ مساعد الفيزياء - مستر محمود")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح ناقص!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

if prompt := st.chat_input("اسألني أي سؤال..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
