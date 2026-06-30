import os
import gzip
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# توکن اختصاصی شما
BOT_TOKEN = "8960825466:AAHN3PADUXoxRFy0U_tFFGds0o4ZJ5hW79c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("""👋 به استوگیف خوش اومدی!
    
✨ هر استیکری برام بفرست تا فایل اصلی اون رو برات استخراج کنم.

📦 پشتیبانی از:
• استیکر ثابت (WEBP)
• استیکر متحرک (TGS)
• استیکر ویدیویی (WEBM)

📩 فقط استیکر رو ارسال کن.""")

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    status_message = await update.message.reply_text("در حال پردازش... ⏳")
    os.makedirs("temp", exist_ok=True)
    
    file = await context.bot.get_file(sticker.file_id)
    input_path = f"temp/{sticker.file_id}"
    await file.download_to_drive(input_path)

    try:
        if sticker.is_video:
            await status_message.edit_text("استیکر ویدیویی (WebM) است. ارسال ویدیو... 🎬")
            await update.message.reply_video(video=open(input_path, 'rb'), caption="آماده شد! ⚡")
        elif sticker.is_animated:
            await status_message.edit_text("استیکر متحرک (TGS) است. استخراج سورس انیمیشن... 🔄")
            output_json = f"temp/{sticker.file_id}.json"
            with gzip.open(input_path, 'rb') as f_in:
                with open(output_json, 'wb') as f_out:
                    f_out.write(f_in.read())
            await update.message.reply_document(document=open(output_json, 'rb'), filename="animation.json", caption="سورس متحرک استخراج شد! 📑")
            if os.path.exists(output_json): os.remove(output_json)
        else:
            await status_message.edit_text("ارسال استیکر ثابت... 📸")
            await update.message.reply_document(document=open(input_path, 'rb'), filename="sticker.webp", caption="تصویر استیکر شما! 🖼️")
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("خطایی رخ داد. ❌")
    finally:
        try: await status_message.delete()
        except: pass
        if os.path.exists(input_path): os.remove(input_path)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    print("Bot is running...")
    app.run_polling()

if name == "main":
    main()