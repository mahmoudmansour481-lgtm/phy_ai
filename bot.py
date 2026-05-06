import telebot
import google.generativeai as genai
import os

# التوكن بتاع التليجرام اللي إنت جبته
TOKEN = "8755768203:AAG0lBy3IkNb67JDNR-18F7ZEXTfGlsUo-A"
bot = telebot.TeleBot(TOKEN)

# إعداد جيمي (هيقرأ المفتاح من إعدادات السيرفر)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت مستر محمود للفيزياء! أنا جاهز للرد على أسئلتك.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # بنبعت السؤال لجيميناي
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "لحظة واحدة يا بطل، جيمي بياخد نفسه.. جرب تسأل تاني.")

bot.infinity_polling()
