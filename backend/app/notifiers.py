import logging
from dataclasses import asdict

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.settings import get_settings
from app.models import Job
from app.wrappers.telegram import BotTelegram

logger = logging.getLogger(__name__)


async def notify_new_jobs():
    """Notifica os usuários sobre novas vagas.

    Envia uma mensagem formatada para os canais
    configurados com as informações das vagas.
    """
    async with AsyncSessionLocal() as session:
        jobs_for_telegram = await session.scalars(
            select(Job).where(Job.telegram_notified == False)
        )
        jobs_for_telegram = jobs_for_telegram.all()

        telegram_jobs = [asdict(job) for job in jobs_for_telegram]

        n_jobs = len(telegram_jobs)

        logger.info(f'Notificando sobre {n_jobs} novas vagas')
        settings = get_settings()

        telegram = BotTelegram(token=settings.TELEGRAM_BOT_TOKEN)

        # Envia notificações com novas vagas para os canais
        await telegram.send_notification_jobs(
            jobs=telegram_jobs,
            chat_id=settings.TELEGRAM_CHAT_ID,
            session=session,
        )
