import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات روشن است")

async def sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.sticker.file_id)
    # مطمئن شوید که پوشه temp از قبل ساخته شده است
    await file.download_to_drive(f"temp/{update.message.sticker.file_id}.webp")
    await update.message.reply_text("دریافت شد")

def main():
    """راه‌اندازی و اجرای استاندارد ربات"""
    # ساخت اپلیکیشن
    app = Application.builder().token(BOT_TOKEN).build()

    # افزودن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, sticker))

    print("Bot is running...")
    
    # این متد تمام مراحل initialize، start و polling را خودش به صورت استاندارد هندل می‌کند
    app.run_polling()

if __name__ == "__main__":
    main()