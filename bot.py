import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
from moviepy.editor import VideoFileClip
# استفاده از کتابخانه خالص tgs برای رندر انیمیشن‌های برداری تلگرام
from tgs.utils import ffmpeg as tgs_ffmpeg

BOT_TOKEN = "AAHN3PADUXoxRFy0U_tFFGds0o4ZJ5hW79c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام امیر جان! ربات آماده‌ست و بدون مشکل لایبرری‌ها بالا اومد. هر ۳ مدل استیکر رو بفرست تست کنیم! 🔥")

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    status_message = await update.message.reply_text("در حال پردازش استیکر... ⏳")
    os.makedirs("temp", exist_ok=True)
    
    file = await context.bot.get_file(sticker.file_id)
    input_path = f"temp/{sticker.file_id}"
    await file.download_to_drive(input_path)

    try:
        # ۱. استیکرهای متحرک قدیمی برداری (TGS)
        if sticker.is_animated:
            await status_message.edit_text("در حال رندر کردن استیکر متحرک سنتی به گیف... 🎨")
            output_gif = f"temp/{sticker.file_id}.gif"
            
            # تبدیل مستقیم فایل برداری TGS به انیمیشن متحرک با ابزار tgs و ffmpeg
            tgs_ffmpeg.to_gif(input_path, output_gif)
            
            await update.message.reply_animation(animation=open(output_gif, 'rb'), caption="استیکر متحرک برداری شما با موفقیت به گیف تبدیل شد! 😍")

        # ۲. استیکرهای ویدیویی جدید (WebM)
        elif sticker.is_video:
            await status_message.edit_text("در حال تبدیل ویدیو استیکر به گیف... 🎬")
            output_gif = f"temp/{sticker.file_id}.gif"
            
            clip = VideoFileClip(input_path)
            clip.write_gif(output_gif, fps=15, program='ffmpeg', logger=None)
            clip.close()
            
            await update.message.reply_animation(animation=open(output_gif, 'rb'), caption="استیکر ویدیویی به گیف تبدیل شد! ⚡")

        # ۳. استیکرهای ثابت معمولی (WebP)
        else:
            await status_message.edit_text("در حال تبدیل استیکر به عکس... 📸")
            output_png = f"temp/{sticker.file_id}.png"
            
            with Image.open(input_path) as img:
                img.save(output_png, "PNG")
                
            await update.message.reply_photo(photo=open(output_png, 'rb'), caption="استیکر ثابت به عکس تبدیل شد! 🖼️")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("خطایی در رندر یا تبدیل فایل رخ داد. دوباره تلاش کن. ❌")
    
    finally:
        try: await status_message.delete()
        except: pass
        if os.path.exists(input_path): os.remove(input_path)
        if 'output_gif' in locals() and os.path.exists(output_gif): os.remove(output_gif)
        if 'output_png' in locals() and os.path.exists(output_png): os.remove(output_png)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    app.run_polling()

if __name__ == "__main__":
    main()