import random
import time
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import CrowbarStats

router = Router()

FORGING_COOLDOWN = 7200

messages_success = [
    "{first_name}, Пшш-ш-ш-ш-ш! Успешно сковано {n} монтировок.",
    "{first_name}, сервер выдержал запрос - random даёт тебе {n} монтировок.",
    "{first_name}, ты сковал {n} монтировок!",
    "Hyvää työtä, {first_name}! Добавлено {n} монтировок на счёт."
]

messages_fail = [
    "Жмак, {first_name}. Следующая ковка будет доступна через {hours_left}ч и {minutes_left}мин.",
    "Либо время неправильно сохранилось, либо ты мешок, {first_name}! Следующая ковка будет доступна через {hours_left}ч и {minutes_left}мин.",
    "Слишком рано, {first_name}! Следующая ковка будет доступна через {hours_left}ч и {minutes_left}мин.",
    "Помидор в лицо, {first_name}! Следующая ковка будет доступна через {hours_left}ч и {minutes_left}мин."
]

@router.message(Command("forge"))
async def handle_forge(message: Message, session: AsyncSession) -> None:
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
    if current_time - stats.last_forging >= FORGING_COOLDOWN:
        crowbar_amount = random.randint(0,2)
        stats.crowbars += crowbar_amount
        stats.last_forging = current_time
        await session.commit()
        msg = random.choice(messages_success).format(first_name = message.from_user.first_name, n = crowbar_amount)
        await message.answer(msg)
        
    elif current_time - stats.last_forging < FORGING_COOLDOWN:
        remaining_seconds = FORGING_COOLDOWN - (current_time - stats.last_forging)
        remaining_hours = remaining_seconds // 3600 
        remaining_minutes = (remaining_seconds % 3600) // 60 
        msg = random.choice(messages_fail).format(first_name = message.from_user.first_name, hours_left = remaining_hours, minutes_left = remaining_minutes)
        await message.answer(msg)