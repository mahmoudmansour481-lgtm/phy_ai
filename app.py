import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="مساعد الفيزياء - مستر محمود")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# التأكد من وجود المفتاح في Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح غير موجود في الإعدادات (Secrets)")
    st.stop()

# إعداد الجيمناي
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# تعريف الموديل بأبسط صورة ممكنة
model = genai.GenerativeModel('gemini-1.5-flash-001')

# نظام الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني أي سؤال في الفيزياء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # مناداة الموديل مباشرة بدون أي إضافات معقدة
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.error("خلصت حصة النهاردة يا بطل، نتقابل بكرة!")
            else:
                st.error(f"حدث خطأ: {e}")
