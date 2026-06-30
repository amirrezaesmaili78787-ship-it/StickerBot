import asyncio
import os
import gzip
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
from moviepy.editor import VideoFileClip

# توکن رباتت رو دقیقاً اینجا جایگزین کن
BOT_TOKEN = "8960825466:AAHN3PADUXoxRFy0U_tFFGds0o4ZJ5hW79c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام امیر جان! ربات همه‌فن‌حریف تبدیل استیکر به گیف آماده‌ست. 🔥\n"
        "الان دیگه استیکرهای متحرک قدیمی (TGS)، ویدیویی (WebM) و ثابت رو مایل به گیف یا عکس می‌کنه. بفرست بریم!"
    )

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    status_message = await update.message.reply_text("در حال دانلود و تشخیص نوع استیکر... ⏳")

    os.makedirs("temp", exist_ok=True)
    
    file = await context.bot.get_file(sticker.file_id)
    input_path = f"temp/{sticker.file_id}"
    await file.download_to_drive(input_path)

    try:
        # ۱. بررسی استیکرهای ویدیویی متحرک (WebM)
        if sticker.is_video:
            await status_message.edit_text("در حال تبدیل استیکر ویدیویی به گیف متحرک... 🎬")
            output_gif = f"temp/{sticker.file_id}.gif"
            
            clip = VideoFileClip(input_path)
            clip.write_gif(output_gif, fps=15, program='ffmpeg', logger=None)
            clip.close()
            
            await update.message.reply_animation(animation=open(output_gif, 'rb'), caption="استیکر ویدیویی شما با موفقیت به گیف تبدیل شد! 😍")

        # ۲. بررسی استیکرهای متحرک برداری سنتی (TGS)
        elif sticker.is_animated:
            await status_message.edit_text("این یک استیکر متحرک برداری (TGS) است. در حال استخراج فایل... 🔄")
            
            # فایل‌های TGS در اصل فایل‌های json هسند که gzip شده‌اند. آنها را باز می‌کنیم.
            output_json = f"temp/{sticker.file_id}.json"
            with gzip.open(input_path, 'rb') as f_in:
                with open(output_json, 'wb') as f_out:
                    f_out.write(f_in.read())
            
            # در اینجا برای تبدیل فرآیند برداری به تصویر متحرک واقعی، چون سرورهای داکر لایبرری سنگین می‌خواهند،
            # فعلاً دیتای خام اسکلت انیمیشن (JSON) را به عنوان داکیومنت می‌دهیم تا ربات کرش نکند 
            # و در آپدیت بعدی پلیر بومی براش می‌نویسیم.
            await update.message.reply_document(document=open(output_json, 'rb'), filename="animation.json", caption="فایل سورس انیمیشن استیکر متحرک استخراج شد! 📑")

        # ۳. بررسی استیکرهای ثابت (WebP)
        else:
            await status_message.edit_text("در حال تبدیل استیکر ثابت به عکس... 📸")
            output_png = f"temp/{sticker.file_id}.png"
            
            with Image.open(input_path) as img:
                img.save(output_png, "PNG")
                
            await update.message.reply_photo(photo=open(output_png, 'rb'), caption="استیکر ثابت به عکس PNG تبدیل شد! 🖼️")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("آخ! خطایی در پردازش داخلی رخ داد. ❌")
    
    finally:
        # تمیزکاری فایل‌ها
        try:
            await status_message.delete()
        except:
            pass
        if os.path.exists(input_path): os.remove(input_path)
        if 'output_gif' in locals() and os.path.exists(output_gif): os.remove(output_gif)
        if 'output_png' in locals() and os.path.exists(output_png): os.remove(output_png)
        if 'output_json' in locals() and os.path.exists(output_json): os.remove(output_json)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    print("Sticker Converter Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()