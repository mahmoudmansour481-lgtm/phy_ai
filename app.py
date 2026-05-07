import streamlit as st
import google.generativeai as genai
import telebot
from threading import Thread

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد الفيزياء - مستر محمود", page_icon="⚛️")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# 2. جلب المفتاح والتأكد منه
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("خطأ: مفتاح GOOGLE_API_KEY غير موجود في الـ Secrets على Streamlit!")
    st.stop()

API_KEY = st.secrets["GOOGLE_API_KEY"]
TELEGRAM_TOKEN = "8755768203:AAG0lBy3IkNb67JDNR-18F7ZEXTfGlsUo-A"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 3. وظيفة التليجرام
def run_bot():
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        try:
            response = model.generate_content(message.text)
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, f"خطأ في التليجرام: {str(e)}")
    
    bot.remove_webhook()
    bot.infinity_polling()

if "bot_active" not in st.session_state:
    Thread(target=run_bot, daemon=True).start()
    st.session_state.bot_active = True

# 4. واجهة الموقع
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("اسألني أي سؤال في الفيزياء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ فني: {str(e)}")
