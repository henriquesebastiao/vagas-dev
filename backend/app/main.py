import asyncio
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app import __version__
from app.api.routes import job
from app.core.settings import get_settings
from app.scheduler import scheduler, setup_scheduler
from app.schemas.health import HealthOut
from app.wrappers.discord_bot import bot

settings = get_settings()

log_level = 'INFO'
if settings.DEBUG:
    log_level = 'DEBUG'


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # Descobre o nível equivalente no loguru
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Sobe na call stack para achar o chamador real
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


description = f"""
Esta API fornece acesso a vagas de emprego para desenvolvedores, coletadas de diversas fontes.

Inicialmente, as vagas são coletadas da plataforma Gupy, mas a arquitetura é modular para permitir a adição de outras fontes no futuro.

#### Documentação alternativa: [Redoc]({settings.APP_URL}/redoc)
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup

    # Remove o handler padrão do loguru
    logger.remove()

    logger.add(
        sys.stdout,
        level=log_level,
        colorize=True,
    )

    # Opcional: salvar em arquivo com rotação
    logger.add(
        'logs/app.log',
        level=log_level,
        rotation='10 MB',
        retention='7 days',
        compression='zip',
    )

    # Intercepta todos os loggers do Python (uvicorn, sqlalchemy, etc.)
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = [InterceptHandler()]
        logging.getLogger(name).propagate = False

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
