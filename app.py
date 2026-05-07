import streamlit as st
import google.generativeai as genai
import telebot
from threading import Thread

# قائمة المفاتيح
keys = [st.secrets["KEY1"], st.secrets["KEY2"], st.secrets["KEY3"]]

def get_chat_response(prompt_text):
    for k in keys:
        try:
            genai.configure(api_key=k)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt_text)
            return response.text
        except Exception as e:
            if "429" in str(e): # لو المفتاح ده خلص حصته
                continue # جرب اللي بعده
            return "عذراً يا بطل، حاول كمان شوية."
    return "كل المفاتيح استهلكت حصتها النهاردة، نتقابل بكرة!"

# إعداد البوت للتليجرام
TELEGRAM_TOKEN = "8755768203:AAG0lBy3IkNb67JDNR-18F7ZEXTfGlsUo-A"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def run_bot():
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        res = get_chat_response(message.text)
        bot.reply_to(message, res)
    bot.infinity_polling()

if "bot_run" not in st.session_state:
    Thread(target=run_bot, daemon=True).start()
    st.session_state.bot_run = True

# واجهة الموقع
st.title("⚛️ مساعد الفيزياء - مستر محمود")
user_input = st.chat_input("اسأل مستر جيمي...")
if user_input:
    st.write(get_chat_response(user_input))
