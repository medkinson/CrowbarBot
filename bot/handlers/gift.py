import random
import time
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import CrowbarStats

router = Router()

GIFT_COOLDOWN = 86400

messages_success = [
    "{first_name}, Тяф-тяф! Из крота падает {n} монтировок.",
    "{first_name}, дарёному лису в зубы не смотрят - финское посольство дарит тебе {n} монтировок.",
    "{first_name}, из горшочка с перцем падает {n} монтировок!",
    "Hyvää työtä, {first_name}! Твой подарок - {n} монтировок."
]

messages_fail = [
    "Пока подарка не занесли, {first_name}. Следующий подарок будет доступен через {hours_left}ч и {minutes_left}мин.",
    "Нетерпеливый {first_name}! Следующий подарок будет доступен через {hours_left}ч и {minutes_left}мин.",
    "Слишком рано, {first_name}! Следующий подарок будет доступен через {hours_left}ч и {minutes_left}мин.",
    "Чеснок в лицо, {first_name}! Следующий подарок будет доступен через {hours_left}ч и {minutes_left}мин."
]

@router.message(Command("gift"))
async def handle_gift(message: Message, session: AsyncSession) -> None:
    stats = await session.get(CrowbarStats, message.from_user.id)
    current_time = int(time.time())

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
    if current_time - stats.last_gift >= GIFT_COOLDOWN:
        gift_amount = random.randint(1,10)
        stats.crowbars += gift_amount
        stats.last_gift = current_time
        await session.commit()
        msg = random.choice(messages_success).format(first_name = message.from_user.first_name, n = gift_amount)
        await message.answer(msg)
        
    elif current_time - stats.last_gift < GIFT_COOLDOWN:
        remaining_seconds = GIFT_COOLDOWN - (current_time - stats.last_gift)
        remaining_hours = remaining_seconds // 3600 
        remaining_minutes = (remaining_seconds % 3600) // 60 
        msg = random.choice(messages_fail).format(first_name = message.from_user.first_name, hours_left = remaining_hours, minutes_left = remaining_minutes)
        await message.answer(msg)