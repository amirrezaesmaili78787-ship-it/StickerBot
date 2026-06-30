import asyncio
import os
import gzip
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
from moviepy.editor import VideoFileClip

BOT_TOKEN = "AAHN3PADUXoxRFy0U_tFFGds0o4ZJ5hW79c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام امیر جان! ربات با موفقیت و در پایداری کامل بالا آمد. 🚀\nاستیکرهای ثابت یا ویدیویی جدیدت رو بفرست تا سه‌سوته تبدیل به گیف و عکس کنم!")

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    status_message = await update.message.reply_text("در حال پردازش استیکر... ⏳")
    os.makedirs("temp", exist_ok=True)
    
    file = await context.bot.get_file(sticker.file_id)
    input_path = f"temp/{sticker.file_id}"
    await file.download_to_drive(input_path)

    try:
        # ۱. استیکرهای ویدیویی جدید (WebM) -> تبدیل به GIF متحرک واقعی
        if sticker.is_video:
            await status_message.edit_text("در حال تبدیل ویدیو استیکر به گیف متحرک... 🎬")
            output_gif = f"temp/{sticker.file_id}.gif"
            
            clip = VideoFileClip(input_path)
            clip.write_gif(output_gif, fps=15, program='ffmpeg', logger=None)
            clip.close()
            
            await update.message.reply_animation(animation=open(output_gif, 'rb'), caption="استیکر ویدیویی شما با موفقیت به گیف تبدیل شد! 😍")

        # ۲. استیکرهای ثابت معمولی (WebP) -> تبدیل به عکس باکیفیت PNG
        elif not sticker.is_animated:
            await status_message.edit_text("در حال تبدیل استیکر ثابت به عکس... 📸")
            output_png = f"temp/{sticker.file_id}.png"
            
            with Image.open(input_path) as img:
                img.save(output_png, "PNG")
                
            await update.message.reply_photo(photo=open(output_png, 'rb'), caption="استیکر ثابت شما به عکس تبدیل شد! 🖼️")

        # ۳. استیکرهای متحرک سنتی (TGS)
        else:
            await status_message.edit_text("این استیکر از نوع برداری متحرک (TGS) است. در حال استخراج فایل متنی انیمیشن... 🔄")
            output_json = f"temp/{sticker.file_id}.json"
            
            with gzip.open(input_path, 'rb') as f_in:
                with open(output_json, 'wb') as f_out:
                    f_out.write(f_in.read())
            
            await update.message.reply_document(document=open(output_json, 'rb'), filename="lottie_animation.json", caption="سورس متنی انیمیشن استیکر (Lottie JSON) استخراج شد! 📑")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("خطایی در تبدیل فایل رخ داد. دوباره تلاش کن. ❌")
    
    finally:
        try: await status_message.delete()
        except: pass
        if os.path.exists(input_path): os.remove(input_path)
        if 'output_gif' in locals() and os.path.exists(output_gif): os.remove(output_gif)
        if 'output_png' in locals() and os.path.exists(output_png): os.remove(output_png)
        if 'output_json' in locals() and os.path.exists(output_json): os.remove(output_json)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    app.run_polling()

if __name__ == "__main__":
    main()