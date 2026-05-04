import streamlit as st
import google.generativeai as genai

# إعداد الصفحة واللقب
st.set_page_config(page_title="مساعد الفيزياء الذكي", page_icon="⚛️")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح من الـ Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("خطأ: لم يتم العثور على مفتاح الـ API في إعدادات Secrets")

# الموديل الأساسي
model = genai.GenerativeModel('gemini-1.5-flash')

# سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة السؤال والجواب
if prompt := st.chat_input("اسألني أي سؤال في الفيزياء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # طلب الإجابة من جيمي
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بجيمي: {e}")
