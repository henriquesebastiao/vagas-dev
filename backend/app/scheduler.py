import logging
from dataclasses import asdict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models import Job
from app.notifiers import notify_new_jobs
from app.scrapers.gupy import GupyScraper

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def run_gupy_sync():
    logger.info('Iniciando sync Gupy...')

    # Os keywords aqui serão as vagas que irão ser buscadas automaticamente.
    scraper = GupyScraper(keywords=['python', 'fastapi', 'django'])

    async with AsyncSessionLocal() as session:
        count = await scraper.sync(session)

    logger.info(f'Sync Gupy finalizado. {count} novas vagas.')


async def run_notify_new_jobs():
    logger.info('Iniciando notificação de novas vagas...')

    async with AsyncSessionLocal() as session:
        jobs = await session.scalars(select(Job).where(Job.notified == False))
        jobs = jobs.all()

        for job in jobs:
            # Envia notificações para todos os canais
            notified = await notify_new_jobs(asdict(job))

            # Atualiza registro no banco de dados
            # registrando que as vagas foram envidas pera o canais
            if notified:
                job.notified = True
                session.add(job)
                await session.commit()


def setup_scheduler():
    # Roda a cada 30 minutos
    scheduler.add_job(
        run_gupy_sync,
        trigger=IntervalTrigger(minutes=30),
        id='gupy_sync',
        name='Gupy Job Sync',
        replace_existing=True,
        max_instances=1,  # Evita execuções sobrepostas
        misfire_grace_time=60,  # Tolera até 60s de atraso
    )

    scheduler.add_job(
        run_notify_new_jobs,
        trigger=IntervalTrigger(minutes=30),
        id='notify_new_jobs',
        name='Notifica sobre novas vagas',
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=60,
    )

    # Exemplo com cron: todo dia às 8h e 18h
    # scheduler.add_job(
    #     run_gupy_sync,
    #     trigger=CronTrigger(hour="8,18", minute=0),
    #     id="gupy_sync_cron",
    # )

    scheduler.start()
    logger.info('Scheduler iniciado.')
