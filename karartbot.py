import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 🔹 ضع التوكن الخاص بالبوت هنا
TOKEN = "7764577394:AAFOr0ONjSDZuozeYP0tcRiNysS1pygInaU"

# 🔹 دالة لجلب رابط تحميل فيديو تيك توك بدون علامة مائية باستخدام TikWM API
def get_tiktok_video(url):
    try:
        api_url = "https://www.tikwm.com/api/"
        params = {"url": url}
        response = requests.get(api_url, params=params)
        data = response.json()

        if data.get("data") and data["data"].get("play"):
            return data["data"]["play"]
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# 🔹 دالة لتنزيل الفيديو من الرابط
def download_video(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = "tiktok_video.mp4"

        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        return filename
    except Exception as e:
        print(f"Download Error: {e}")
        return None

# 🔹 دالة لمعالجة الرسائل المستلمة
async def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    chat_id = update.message.chat_id

    if "tiktok.com" in url:
        await update.message.reply_text("🔄 جارٍ جلب رابط الفيديو...")
        video_url = get_tiktok_video(url)

        if video_url:
            await update.message.reply_text("📥 جارٍ تنزيل الفيديو...")
            filename = download_video(video_url)

            if filename and os.path.exists(filename):
                with open(filename, "rb") as file:
                    await context.bot.send_video(chat_id=chat_id, video=file)
                os.remove(filename)
            else:
                await update.message.reply_text("❌ فشل التنزيل!")
        else:
            await update.message.reply_text("❌ لم أتمكن من الحصول على الفيديو!")
    else:
        await update.message.reply_text("❌ الرجاء إرسال رابط فيديو من TikTok فقط.")

# 🔹 دالة بدء البوت مع رسالة الترحيب المخصصة
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🎥 أرسل رابط فيديو تيك توك مطور البوت @u_u_nn")

# 🔹 تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()