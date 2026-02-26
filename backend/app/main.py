import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import job
from app.core.settings import get_settings
from app.scheduler import scheduler, setup_scheduler
from app.schemas.health import HealthOut

logging.basicConfig(level=logging.INFO)
settings = get_settings()

description = f"""
Esta API fornece acesso a vagas de emprego para desenvolvedores, coletadas de diversas fontes.

Inicialmente, as vagas são coletadas da plataforma Gupy, mas a arquitetura é modular para permitir a adição de outras fontes no futuro.

#### Documentação alternativa: [Redoc]({settings.APP_URL}/redoc)
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_scheduler()
    yield
    # Shutdown
    scheduler.shutdown(wait=False)


app = FastAPI(
    title='Vagas DEV - API',
    docs_url='/',
    description=description,
    version=settings.VERSION,
    lifespan=lifespan,
    terms_of_service='https://github.com/henriquesebastiao/vagas-dev/',
    contact={
        'name': 'Vagas Dev',
        'url': 'https://github.com/henriquesebastiao/vagas-dev/',
        'email': 'contato@henriquesebastiao.com',
    },
)
app.include_router(job.router)


@app.get('/health', response_model=HealthOut)
async def health():
    """Endpoint de saúde para verificar se a API está funcionando corretamente."""
    return {'status': 'ok'}
