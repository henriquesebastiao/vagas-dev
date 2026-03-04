import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.database import AsyncSessionLocal
from app.core.settings import get_settings
from app.keywords import KEYWORDS
from app.notifiers import notify_new_jobs
from app.scrapers import gupy, linkedin

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()
settings = get_settings()


async def run_gupy_sync():
    logger.info('Iniciando sync Gupy...')

    # Os keywords aqui serão as vagas que irão ser buscadas automaticamente.
    scraper = gupy.GupyScraper(keywords=KEYWORDS)

    async with AsyncSessionLocal() as session:
        count = await scraper.sync(session)

    logger.info(f'Sync Gupy finalizado. {count} novas vagas.')


async def run_linkedin_sync():
    logger.info('Iniciando sync LinkedIn...')

    # Os keywords aqui serão as vagas que irão ser buscadas automaticamente.
    scraper = linkedin.LinkedInScraper(keywords=KEYWORDS)

    async with AsyncSessionLocal() as session:
        count = await scraper.sync(session)

    logger.info(f'Sync LinkedIn finalizado. {count} novas vagas.')


async def run_notify_new_jobs():
    """Aciona o processo de notificação para novas vagas."""
    await notify_new_jobs()


def setup_scheduler():
    # Roda a cada 30 minutos
    scheduler.add_job(
        run_gupy_sync,
        trigger=IntervalTrigger(minutes=settings.INTERVAL_SYNC),
        id='gupy_sync',
        name='Gupy Job Sync',
        replace_existing=True,
        max_instances=1,  # Evita execuções sobrepostas
        misfire_grace_time=60,  # Tolera até 60s de atraso
    )

    scheduler.add_job(
        run_linkedin_sync,
        trigger=IntervalTrigger(minutes=settings.INTERVAL_SYNC),
        id='linkedin_sync',
        name='Linkedin Job Sync',
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=60,
    )

    scheduler.add_job(
        run_notify_new_jobs,
        trigger=IntervalTrigger(minutes=settings.INTERVAL_SYNC),
        id='notify_new_jobs',
        name='Notifica sobre novas vagas',
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=60,
    )

    scheduler.start()
    logger.info('Scheduler iniciado.')
