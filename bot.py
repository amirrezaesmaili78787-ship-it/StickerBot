import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
from moviepy.editor import VideoFileClip

# توکن رباتت رو دقیقاً اینجا جایگزین کن
BOT_TOKEN = "8960825466:AAHN3PADUXoxRFy0U_tFFGds0o4ZJ5hW79c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام امیر جان! ربات پیشرفته تبدیل استیکر به گیف و عکس آماده‌ست. 🔥\n"
        "هر استیکری بفرستی، برات تبدیلش می‌کنم!"
    )

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    status_message = await update.message.reply_text("در حال دریافت استیکر و شروع پردازش... ⏳")

    # ساخت پوشه موقت
    os.makedirs("temp", exist_ok=True)
    
    # دانلود فایل اصلی استیکر از تلگرام
    file = await context.bot.get_file(sticker.file_id)
    input_path = f"temp/{sticker.file_id}"
    await file.download_to_drive(input_path)

    try:
        # ۱. بررسی استیکرهای ویدیویی (فرمت WebM که معمولاً متحرک‌های جدید هستند)
        if sticker.is_video:
            await status_message.edit_text("در حال تبدیل استیکر ویدیویی به گیف متحرک... 🎬")
            output_gif = f"temp/{sticker.file_id}.gif"
            
            # تبدیل WebM به GIF با استفاده از moviepy
            clip = VideoFileClip(input_path)
            clip.write_gif(output_gif, fps=15, program='ffmpeg', logger=None)
            clip.close()
            
            # ارسال به صورت گیف واقعی در تلگرام
            await update.message.reply_animation(animation=open(output_gif, 'rb'), caption="خدمت شما، استیکر شما به گیف تبدیل شد! 😍")
            
        # ۲. بررسی استیکرهای ثابت (فرمت WebP)
        else:
            await status_message.edit_text("در حال تبدیل استیکر ثابت به عکس PNG... 📸")
            output_png = f"temp/{sticker.file_id}.png"
            
            # تبدیل WebP به PNG با استفاده از Pillow
            with Image.open(input_path) as img:
                img.save(output_png, "PNG")
                
            # ارسال به صورت عکس معمولی
            await update.message.reply_photo(photo=open(output_png, 'rb'), caption="خدمت شما، استیکر به عکس تبدیل شد! 🖼️")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("آخ! موقع تبدیل یه مشکلی پیش آمد. مطمئن شو استیکرت ویدیویی یا عکس ثابته. ❌")
    
    finally:
        # پاک‌سازی فایل‌های موقت برای پر نشدن حافظه سرور
        await status_message.delete()
        if os.path.exists(input_path): os.remove(input_path)
        if 'output_gif' in locals() and os.path.exists(output_gif): os.remove(output_gif)
        if 'output_png' in locals() and os.path.exists(output_png): os.remove(output_png)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    print("Sticker Converter Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()