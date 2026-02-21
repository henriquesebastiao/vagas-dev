from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from database import AsyncSessionLocal
from scrapers.gupy import GupyScraper
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

async def run_gupy_sync():
    logger.info("Iniciando sync Gupy...")
    scraper = GupyScraper(keywords=["python", "fastapi", "django", "backend"])
    async with AsyncSessionLocal() as db:
        count = await scraper.sync(db)
    logger.info(f"Sync Gupy finalizado. {count} novas vagas.")

def setup_scheduler():
    # Roda a cada 30 minutos
    scheduler.add_job(
        run_gupy_sync,
        trigger=IntervalTrigger(minutes=30),
        id="gupy_sync",
        name="Gupy Job Sync",
        replace_existing=True,
        max_instances=1,       # Evita execuções sobrepostas
        misfire_grace_time=60, # Tolera até 60s de atraso
    )

    # Exemplo com cron: todo dia às 8h e 18h
    # scheduler.add_job(
    #     run_gupy_sync,
    #     trigger=CronTrigger(hour="8,18", minute=0),
    #     id="gupy_sync_cron",
    # )

    scheduler.start()
    logger.info("Scheduler iniciado.")