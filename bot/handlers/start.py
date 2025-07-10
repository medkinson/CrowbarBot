import random
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import CrowbarStats

router = Router()

messages = [
    "Баклажаны содержат соланин. Это яд.",
    "От бурых медведей падают сети!",
    "Добро пожаловать в симулятор бесконечного таскания монтировок!",
    "В отличие от первой версии, я написан не говнокодом!"
]

@router.message(Command("start"))
async def handle_message(message: Message, session: AsyncSession) -> None:
    stats = await session.get(CrowbarStats, message.from_user.id)
    
    if not stats:
        stats = CrowbarStats(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            crowbars=0,
            last_gift=0,
            last_forging=0
        )
        session.add(stats)
        await session.commit()
    await message.answer(random.choice(messages))