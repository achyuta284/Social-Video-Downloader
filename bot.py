import os
import logging
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ✅ Telegram Bot Token
TOKEN = "7626158271:AAHe5D_izzvL8ACRKaxP9Uj1tFkvL19jCCY"

# ✅ Initialize bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ✅ Logging setup
logging.basicConfig(level=logging.INFO)

# 📌 Start Command
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("📹 YouTube Video", callback_data="youtube"),
        InlineKeyboardButton("📷 Instagram Video", callback_data="instagram"),
        InlineKeyboardButton("📘 Facebook Video", callback_data="facebook"),
        InlineKeyboardButton("🟢 WhatsApp Status", callback_data="whatsapp"),
        InlineKeyboardButton("📸 Instagram Stories", callback_data="stories"),
        InlineKeyboardButton("🖼️ Images", callback_data="images")
    ]
    keyboard.add(*buttons)
    
    await message.answer("👋 Welcome! Please select the platform from which you want to download videos/images:", reply_markup=keyboard)

# 📌 Callback Query Handler
@dp.callback_query_handler(lambda call: True)
async def callback_handler(call: types.CallbackQuery):
    platform = call.data
    await bot.send_message(call.message.chat.id, f"🔗 Please send the {platform} video link:")
    
    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def download_video(message: types.Message):
        link = message.text
        await message.answer(f"✅ Downloading from: {link}\n🔄 Please wait...")

        # 📌 Using yt-dlp to download the video
        download_path = f"downloads/video.mp4"
        cmd = f"yt-dlp -o {download_path} {link}"
        try:
            subprocess.run(cmd, shell=True, check=True)
            await message.answer_document(open(download_path, "rb"), caption="✅ Here is your downloaded video!")
        except Exception as e:
            await message.answer(f"❌ Download failed! Error: {str(e)}")

        # 📌 Show Thank You Message & Ask Again
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("Download Another Video 🎥", callback_data="restart"),
            InlineKeyboardButton("Join Our Channel 🔔", url="https://t.me/YOUR_CHANNEL")
        )
        await message.answer("🎉 Thank You for using this bot! Want to download another video?", reply_markup=keyboard)

# 📌 Restart Download Process
@dp.callback_query_handler(lambda call: call.data == "restart")
async def restart_download(call: types.CallbackQuery):
    await start_cmd(call.message)

# ✅ Run Bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
