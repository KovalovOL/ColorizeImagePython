import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from PIL import Image
import io

API_TOKEN = 'YOUR_API_TOKEN'


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне изображение, и я его заколоризую!")


@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    photo = message.photo[-1]  
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path

    # Загружаем фото
    file_info = await bot.download_file(file_path)
    image = Image.open(io.BytesIO(file_info))


    output = io.BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    await bot.send_photo(message.chat.id, photo=output)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
