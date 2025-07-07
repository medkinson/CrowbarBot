from aiogram import Dispatcher, types
from aiogram.filters import Command

dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Test")