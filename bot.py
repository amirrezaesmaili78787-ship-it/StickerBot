import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# توکن رباتت رو دقیقاً اینجا جایگزین کن
BOT_TOKEN = "8960825466:AAHN3PADUXoxRFy0U_tFFGds0o4ZJ5hW79c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام امیر جان! ربات تبدیل استیکر به گیف روشن و آماده‌ست. 🔥\n"
        "کافیه یک استیکر (متحرک یا معمولی) برام بفرستی تا برات تبدیلش کنم."
    )

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    
    # بررسی اینکه آیا استیکر متحرک (فایل‌های TGS یا ویدیویی) هست یا معمولی
    if sticker.is_animated or sticker.is_video:
        await update.message.reply_text("در حال پردازش استیکر متحرک و تبدیل به گیف... لطفاً کمی صبر کن. ⏳")
    else:
        await update.message.reply_text("در حال دریافت استیکر... 🔄")

    # ساخت پوشه موقت در صورت عدم وجود
    os.makedirs("temp", exist_ok=True)
    
    # دانلود فایل استیکر
    file = await context.bot.get_file(sticker.file_id)
    file_path = f"temp/{sticker.file_id}.webp"
    await file.download_to_drive(file_path)
    
    # ارسال فایل به عنوان پیش‌فرض (در گام‌های بعدی ابزار تبدیل کامل رو بهش اضافه می‌کنیم)
    await update.message.reply_document(document=open(file_path, 'rb'), filename="sticker.webp", caption="فایل استیکر دریافت شد!")

def main():
    """راه‌اندازی استاندارد چرخه‌ی حیات ربات"""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    print("Bot is running perfectly...")
    app.run_polling()

if __name__ == "__main__":
    main()