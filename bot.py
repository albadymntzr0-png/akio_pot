from flask import Flask
import threading
import os
import sys
import asyncio

# إصلاح حلقة الأحداث ليتوافق مع بايثون 3.15 على الويندوز
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ==========================================
# إعدادات البوت والتوكن الخاص بك
# ==========================================
TOKEN = "5501734670:AAHltZtiaOpyFMfWx4eBnALxAKeuFClpRGg"
OWNER_ID = 1157443411

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, loop=loop)

# ==========================================
# أوامر البوت
# ==========================================
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        "🤖 **مرحباً بك في بوت تحميل فيديوهات تيك توك**\n\n"
        "• دز لي رابط أي فيديو من تيك توك وسأقوم بتحميله لك فوراً وبدون علامة مائية! 📥\n"
        "• قناة البوت: https://t.me/IIII3G"
    )

@dp.message_handler(content_types=types.ContentType.TEXT)
async def download_tiktok(message: types.Message):
    url = message.text
    if "tiktok.com" in url or "vm.tiktok.com" in url:
        sent_msg = await message.reply("⏳ جاري جلب وتحميل الفيديو بدون علامة مائية...")
        
        # API مجاني لجلب فيديو تيك توك بدون علامة مائية
        api_url = f"https://tikwm.com/api/?url={url}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    data = await resp.json()
                    if data.get("code") == 0:
                        video_url = data["data"]["play"]
                        await message.reply_video(
                            video=video_url, 
                            caption="✅ تم تحميل الفيديو بنجاح بواسطة بوت تيك توك"
                        )
                        await sent_msg.delete()
                    else:
                        await sent_msg.edit_text("❌ عذراً، لم أستطع تحميل الفيديو. تأكد من صحة الرابط.")
        except Exception as e:
            logger.error(f"Error downloading TikTok: {e}")
            await sent_msg.edit_text("❌ حدث خطأ أثناء الاتصال بخادم التحميل.")
    else:
        await message.reply("⚠️ يرجى إرسال رابط تيك توك صحيح فقط.")

# تشغيل البوت
app = Flask('')

@app.route('/')
def home():
    return "Bot is active and running 24/7!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()
if __name__ == "__main__":
    print("🚀 Starting TikTok Downloader Bot...")
    print(f"👑 Owner ID: {OWNER_ID}")
    executor.start_polling(dp, skip_updates=True)
    keep_alive()
