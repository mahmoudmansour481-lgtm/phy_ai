import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="مساعد الفيزياء")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح من الـ Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# محاولة ذكية لتعريف الموديل تهرب من خطأ 404
try:
    # الطريقة الأولى (للنسخ الجديدة)
    model = genai.GenerativeModel('gemini-1.5-flash')
    # اختبار سريع عشان نتأكد إنه مش 404
    model.generate_content("hi") 
except:
    try:
        # الطريقة الثانية (لبعض سيرفرات Streamlit اللي لسه قديمة)
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except:
        # الطريقة الثالثة (لو مفيش فايدة في Flash، نستخدم Pro المستقر جداً)
        model = genai.GenerativeModel('gemini-pro')

# واجهة الشات
if prompt := st.chat_input("اسأل مستر جيمي..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"عذراً، فيه مشكلة في الاتصال: {e}")
