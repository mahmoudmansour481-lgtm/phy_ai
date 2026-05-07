import streamlit as st
import requests
import json

st.set_page_config(page_title="مساعد الفيزياء - مستر محمود")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

def ask_gemini(prompt):
    # جربنا v1 بدل v1beta عشان نهرب من الـ 404
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # لو v1 منفعش، الكود هيجرب v1beta أوتوماتيكياً
            url_beta = url.replace("/v1/", "/v1beta/")
            response_beta = requests.post(url_beta, headers=headers, json=data, timeout=10)
            if response_beta.status_code == 200:
                return response_beta.json()['candidates'][0]['content']['parts'][0]['text']
            return f"عذراً يا مستر، جوجل مش مستجيب حالياً. الخطأ: {response_beta.status_code}"
    except Exception as e:
        return f"فيه مشكلة في الشبكة: {str(e)}"

if prompt := st.chat_input("اسألني أي سؤال..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        answer = ask_gemini(prompt)
        st.write(answer)
