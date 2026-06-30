import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# توکن رباتت رو مستقیم بذار بین دو تا کوتیشن زیر
BOT_TOKEN = 8960825466: "AAHN3PADUXoxRFy0U_tFFGds0o4ZJ5hW79c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات روشن است")

async def sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.sticker.file_id)
    await file.download_to_drive(f"temp/{update.message.sticker.file_id}.webp")
    await update.message.reply_text("دریافت شد")

def main():
    """راه‌اندازی و اجرای استاندارد ربات"""
    # ساخت اپلیکیشن با توکن مستقیم
    app = Application.builder().token(BOT_TOKEN).build()

    # افزودن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, sticker))

    print("Bot is running...")
    
    # اجرای پولینگ ربات
    app.run_polling()

if __name__ == "__main__":
    main()