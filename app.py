import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مساعد الفيزياء الذكي", page_icon="⚛️")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح من الـ Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("تأكد من وضع GOOGLE_API_KEY في إعدادات Secrets على Streamlit Cloud")

# استخدام الموديل المستقر
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
      system_instruction="أنت 'مستر جيمي'، خبير في مادة الفيزياء للمرحلة الثانوية بمصر. أسلوبك تعليمي، مشجع، ومبسط. استخدم اللهجة المصرية البيضاء المحببة للطلاب، وقدم حلولاً نموذجية للمسائل مع شرح الخطوات بوضوح."
)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني أي سؤال في الفيزياء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # تحديد الموديل هنا مباشرة يحل مشاكل الـ NotFound
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"عذراً، حدث خطأ: {e}")
