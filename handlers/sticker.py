import os
from telegram import Update
from telegram.ext import ContextTypes

async def sticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker

    file = await context.bot.get_file(sticker.file_id)

    os.makedirs("temp", exist_ok=True)

    path = f"temp/{sticker.file_id}.webp"
    await file.download_to_drive(path)

    await update.message.reply_text("استیکر دریافت شد و ذخیره شد.")