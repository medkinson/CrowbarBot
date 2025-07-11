import random
import time
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import CrowbarStats

router = Router()

@router.message(Command("top"))
async def handle_top(message: Message, session: AsyncSession):
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
    query = await session.execute(
        select(CrowbarStats).where(CrowbarStats.crowbars > 0).order_by(CrowbarStats.crowbars.desc()).limit(10)
    )
    top = query.scalars().all()
    if not top:
        await message.answer("Лудоманы еще не обзавелись монтировками.")
    medals = ["🥇", "🥈", "🥉"]
    top_list = []
    for idx, user in enumerate(top):
        position = medals[idx] if idx < 3 else f"{idx + 1}."
        top_list.append(f"{position} {user.first_name}{' ' + user.last_name if user.last_name else ''} — {user.crowbars} монтировок")
    response_text = "Монтировочные магнаты:\n\n" + "\n".join(top_list)
    await message.answer(response_text)

    