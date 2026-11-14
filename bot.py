import os
import asyncio
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types

# التوكن الخاص ببوتك جاهز ومرتبط تلقائياً
TOKEN = "7752042125:AAHnE5W2wWb3fH4F8d8sK2g1lZ9xV7mN6pQ" # التوكن الخاص ببوتك

bot = Bot(token=TOKEN)
dp = Dispatcher()

# إعداد سيرفر Flask البسيط لتبقي المنصة متصلة 24/7 وبدون توقف
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# تشغيل البوت بالطريقة الحديثة المتوافقة مع الإصدار الثالث
async def main():
    # بدء تشغيل سيرفر الفلاسك في خلفية منفصلة
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # بدء تشغيل البوت واستقبال الرسائل
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
