import streamlit as st
import requests

st.set_page_config(page_title="مساعد الفيزياء - مستر محمود")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح
api_key = st.secrets.get("GOOGLE_API_KEY")

if prompt := st.chat_input("اسألني أي سؤال في الفيزياء..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        # الرابط المباشر للنسخة المستقرة
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.write(answer)
            else:
                st.error(f"جوجل بيقول فيه خطأ 404، ده معناه إن السيرفر في منطقة غير مدعومة.")
        except Exception as e:
            st.error(f"مشكلة في الاتصال: {e}")
