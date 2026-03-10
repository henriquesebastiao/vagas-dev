from dataclasses import asdict
from typing import Any

from loguru import logger
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.settings import get_settings
from app.models import Job
from app.wrappers.discord_bot import send_notification_jobs
from app.wrappers.telegram import BotTelegram


async def get_jobs_for_selector(selector) -> dict[str, Any]:
    async with AsyncSessionLocal() as session:
        jobs = await session.scalars(select(Job).where(selector == False))
        jobs = jobs.all()

        jobs = [asdict(job) for job in jobs]

        return {'jobs': jobs, 'session': session}


async def notify_new_jobs():
    """Notifica os usuários sobre novas vagas.

    Envia uma mensagem formatada para os canais
    configurados com as informações das vagas.
    """
    settings = get_settings()

    # TELEGRAM
    result = await get_jobs_for_selector(Job.telegram_notified)
    telegram_jobs = result['jobs']
    n_jobs = len(telegram_jobs)

    logger.info(f'[Telegram] Notificando sobre {n_jobs} novas vagas')

    telegram = BotTelegram(token=settings.TELEGRAM_BOT_TOKEN)

    # Envia notificações com novas vagas para os canais
    await telegram.send_notification_jobs(
        jobs=telegram_jobs,
        chat_id=settings.TELEGRAM_CHAT_ID,
        session=result['session'],
    )

    # DISCORD
    result = await get_jobs_for_selector(Job.discord_notified)
    discord_jobs = result['jobs']
    n_jobs = len(discord_jobs)

    logger.info(f'[Discord] Notificando sobre {n_jobs} novas vagas')

    # Envia notificações com novas vagas para os canais
    await send_notification_jobs(
        jobs=discord_jobs,
        session=result['session'],
    )
