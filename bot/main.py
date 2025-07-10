import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import start, forge
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from middlewares.db import DbSessionMiddleware
from database.models import CrowbarStats, Base

load_dotenv()

async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///crowbarbot.db", echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    await create_tables(engine)
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(sessionmaker))
    dp.include_routers(start.router, forge.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())