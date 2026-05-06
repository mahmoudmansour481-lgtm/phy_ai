import streamlit as st
import google.generativeai as genai
import telebot
from threading import Thread

# 1. إعدادات جيمي والتليجرام
st.set_page_config(page_title="مساعد الفيزياء الذكي", page_icon="⚛️")
st.title("⚛️ مساعد الفيزياء - مستر محمود")

# جلب المفاتيح من الـ Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    TELEGRAM_TOKEN = "8755768203:AAG0lBy3IkNb67JDNR-18F7ZEXTfGlsUo-A"
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
except Exception as e:
    st.error("تأكد من ضبط المفاتيح في الـ Secrets")

# 2. وظيفة ردود التليجرام (بتشتغل في الخلفية)
# وظيفة تشغيل البوت مع إعادة المحاولة التلقائية
def run_bot():
    try:
        @bot.message_handler(func=lambda message: True)
        def handle_telegram_message(message):
            try:
                # بنستخدم الموديل اللي عرفناه فوق
                response = model.generate_content(message.text)
                bot.reply_to(message, response.text)
            except Exception as e:
                bot.reply_to(message, "فيه ضغط حالياً يا بطل، جرب كمان ثواني.")
        
        bot.remove_webhook() # خطوة أمان عشان ميتداخلش مع محاولات قديمة
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Bot error: {e}")

# التأكد من تشغيل البوت مرة واحدة فقط
if "bot_started" not in st.session_state:
    thread = Thread(target=run_bot, daemon=True) # daemon=True عشان يتقفل مع الموقع
    thread.start()
    st.session_state.bot_started = True

# 3. تشغيل البوت في "خيط" منفصل عشان ميعطلش الموقع
if "bot_thread" not in st.session_state:
    thread = Thread(target=run_bot)
    thread.start()
    st.session_state.bot_thread = True

# 4. واجهة الموقع العادية (للي بيحب يستخدم المتصفح)
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
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
