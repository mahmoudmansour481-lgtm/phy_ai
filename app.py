import streamlit as st
import google.generativeai as genai
import telebot
from threading import Thread

# 1. إعدادات الواجهة والجيمناي
st.set_page_config(page_title="مساعد الفيزياء الذكي", page_icon="⚛️")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفتاح الوحيد من الـ Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # توكن التليجرام الخاص بك
    TELEGRAM_TOKEN = "8755768203:AAG0lBy3IkNb67JDNR-18F7ZEXTfGlsUo-A"
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
except Exception as e:
    st.error("تأكد من وجود مفتاح GOOGLE_API_KEY في الـ Secrets")

# 2. وظيفة التليجرام
def run_bot():
    @bot.message_handler(func=lambda message: True)
    def handle_telegram_message(message):
        try:
            response = model.generate_content(message.text)
            bot.reply_to(message, response.text)
        except Exception as e:
            if "429" in str(e):
                bot.reply_to(message, "خلصت حصة النهاردة يا بطل، نتقابل بكرة!")
            else:
                bot.reply_to(message, "لحظة فيه مشكلة فنية بسيطة.")
    
    bot.remove_webhook()
    bot.infinity_polling()

# تشغيل البوت في الخلفية
if "bot_started" not in st.session_state:
    thread = Thread(target=run_bot, daemon=True)
    thread.start()
    st.session_state.bot_started = True

# 3. واجهة الدردشة على الموقع
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل مستر جيمي في الفيزياء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.error("عذراً، انتهت حدود الأسئلة المجانية لهذا اليوم.")
            else:
                st.error("حدث خطأ ما، جرب لاحقاً.")
