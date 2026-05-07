import streamlit as st
import requests
import json

st.set_page_config(page_title="مساعد الفيزياء - مستر محمود")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("المفتاح ناقص في الـ Secrets!")
    st.stop()

# دالة إرسال السؤال لجوجل مباشرة بدون مكتبات وسيطة
def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"خطأ من جوجل: {response.text}"

# واجهة الشات
if prompt := st.chat_input("اسألني أي سؤال في الفيزياء..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("بفكر..."):
            answer = ask_gemini(prompt)
            st.write(answer)
