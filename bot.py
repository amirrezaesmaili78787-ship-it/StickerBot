import os
import sys
import subprocess

# --- ترفند جادویی تک‌فایل: نصب خودکار پیش‌نیازها روی سرور ریلوای ---
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
except ImportError:
    # اگر کتابخونه نصب نبود، خود کد اون رو روی سرور نصب میکنه
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==21.3"])
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

import gzip

# توکن شما با موفقیت جایگذاری شد
BOT_TOKEN = "8960825466:AAHN3PADUXoxRFy0U_tFFGds0o4ZJ5hW79c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام امیر جان! ربات تک‌فایله با توکن اختصاصی بالا اومد و روشن شد. 🔥\n"
        "الان هر استیکری برام بفرستی، پردازشش می‌کنم و خروجی رو برات می‌فرستم!"
    )

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    status_message = await update.message.reply_text("در حال دریافت و پردازش استیکر... ⏳")
    
    os.makedirs("temp", exist_ok=True)
    
    file = await context.bot.get_file(sticker.file_id)
    input_path = f"temp/{sticker.file_id}"
    await file.download_to_drive(input_path)

    try:
        if sticker.is_video:
            await status_message.edit_text("این یک استیکر ویدیویی متحرک (WebM) است. در حال ارسال... 🎬")
            await update.message.reply_video(video=open(input_path, 'rb'), caption="خدمت شما، نسخه ویدیویی استیکر متحرک! ⚡")
            
        elif sticker.is_animated:
            await status_message.edit_text("این یک استیکر متحرک سنتی (TGS) است. در حال استخراج سورس انیمیشن... 🔄")
            output_json = f"temp/{sticker.file_id}.json"
            with gzip.open(input_path, 'rb') as f_in:
                with open(output_json, 'wb') as f_out:
                    f_out.write(f_in.read())
            await update.message.reply_document(document=open(output_json, 'rb'), filename="animation.json", caption="سورس انیمیشن متحرک استخراج شد! 📑")
            if os.path.exists(output_json): os.remove(output_json)
            
        else:
            await status_message.edit_text("در حال ارسال فایل تصویر استیکر ثابت... 📸")
            await update.message.reply_document(document=open(input_path, 'rb'), filename="sticker.webp", caption="فایل تصویر استیکر ثابت شما! 🖼️")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("مشکلی در ارسال خروجی پیش آمد. ❌")
        
    finally:
        try: await status_message.delete()
        except: pass
        if os.path.exists(input_path): os.remove(input_path)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    print("Bot is successfully running with your token...")
    app.run_polling()

if __name__ == "__main__":
    main()