import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
import asyncio
from handlers.start import dp

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"),default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())