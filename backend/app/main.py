import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import job
from app.scheduler import scheduler, setup_scheduler

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_scheduler()
    yield
    # Shutdown
    scheduler.shutdown(wait=False)


app = FastAPI(title='Vagas DEV - API', lifespan=lifespan)
app.include_router(job.router)


@app.get('/health')
async def health():
    return {'status': 'ok'}
