import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes import job
from app.core.settings import get_settings
from app.scheduler import scheduler, setup_scheduler
from app.schemas.health import HealthOut
from app.wrappers.discord_bot import bot

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

    # Aplica migrations pendentes automaticamente no startup
    proc = await asyncio.create_subprocess_exec(
        'alembic',
        'upgrade',
        'head',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f'Falha ao aplicar migrations:\n{stderr.decode()}')

    # Inicia o bot do Discord
    asyncio.create_task(bot.start(settings.DISCORD_TOKEN))

    setup_scheduler()
    yield
    # Shutdown
    scheduler.shutdown(wait=False)


app = FastAPI(
    title='Vagas DEV - API',
    docs_url='/',
    description=description,
    version=__version__,
    lifespan=lifespan,
    terms_of_service='https://github.com/henriquesebastiao/vagas-dev/',
    contact={
        'name': 'Vagas Dev',
        'url': 'https://github.com/henriquesebastiao/vagas-dev/',
        'email': 'contato@henriquesebastiao.com',
    },
)
app.include_router(job.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health', response_model=HealthOut)
async def health():
    """Endpoint de saúde para verificar se a API está funcionando corretamente."""
    return {'status': 'ok'}
