import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات روشن است")

async def sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.sticker.file_id)
    await file.download_to_drive(f"temp/{update.message.sticker.file_id}.webp")
    await update.message.reply_text("دریافت شد")

async def run():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, sticker))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("Bot is running...")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run())