import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.set_page_config(page_title="مساعد الفيزياء")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح ناقص!")
    st.stop()

# الإعداد مع إجبار السيرفر على استخدام v1 المستقرة
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# هنا السر: بنحدد لـ جوجل إننا عاوزين النسخة المستقرة v1 حصراً
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash'
)

if prompt := st.chat_input("اسأل مستر جيمي..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        try:
            # استخدام RequestOptions لتحديد الإصدار يدوياً
            response = model.generate_content(
                prompt,
                request_options=RequestOptions(api_version='v1')
            )
            st.write(response.text)
        except Exception as e:
            # لو فشل، بنجرب آخر محاولة بالاسم القديم المستقر
            try:
                legacy_model = genai.GenerativeModel('gemini-pro')
                response = legacy_model.generate_content(prompt)
                st.write(response.text)
            except:
                st.error(f"عذراً يا بطل، لسه فيه مشكلة في السيرفر: {e}")
