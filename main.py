from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
from yt_dlp import YoutubeDL
import os
import asyncio

# Создаём папку для загрузок
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Ютубтан видео жонот родной, музыка кылып берем.")

# Функция для скачивания и конвертации аудио
async def download_audio(update: Update, context: CallbackContext):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("Кутуп тур, родной!")
        try:
            options = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            # Используем run_in_executor для выполнения yt-dlp в отдельном потоке
            loop = asyncio.get_event_loop()
            with YoutubeDL(options) as ydl:
                info = await loop.run_in_executor(None, ydl.extract_info, url, True)
                audio_filename = ydl.prepare_filename(info).replace('.webm', '.mp3')

            if os.path.exists(audio_filename):
                with open(audio_filename, "rb") as audio_file:
                    await update.message.reply_audio(audio_file)
                os.remove(audio_filename)
            else:
                await update.message.reply_text("Файл не найден после загрузки!")
        except Exception as e:
            await update.message.reply_text(f"Ошибка болуп калды родной: {e}")
    else:
        await update.message.reply_text("Нормальный ссылка жонот родной")

# Главная функция для запуска бота
def main():
    TOKEN = "7807136622:AAEETbYuxHEhF4SgZt2WshF1ycj1aKjjps0"
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    
    application.run_polling()

if __name__ == "__main__":
    main()