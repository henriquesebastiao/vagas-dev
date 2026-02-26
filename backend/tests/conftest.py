import os

import pytest
from app.core.database import get_session
from app.core.settings import get_settings
from app.main import app
from app.models import table_registry
from app.wrappers.telegram import BotTelegram
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer


@pytest.fixture(autouse=True, scope='session')
def load_env():
    load_dotenv()
    get_settings.cache_clear()

    os.environ['TELEGRAM_PYTHON_TOPIC_ID'] = '3'
    os.environ['TELEGRAM_JAVA_TOPIC_ID'] = '4'
    os.environ['TELEGRAM_GOLANG_TOPIC_ID'] = '5'
    os.environ['TELEGRAM_FRONTEND_TOPIC_ID'] = '6'
    os.environ['TELEGRAM_BACKEND_TOPIC_ID'] = '7'


@pytest.fixture
def get_chat_id():
    return '-1003737014042'


@pytest.fixture
def bot_telegram():
    settings = get_settings()
    print(
        f'TOKEN: {settings.TELEGRAM_BOT_TOKEN[:10]}...'
    )  # primeiros 10 chars
    return BotTelegram(token=get_settings().TELEGRAM_BOT_TOKEN)


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:18-alpine', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest.fixture
async def session(engine: AsyncEngine):
    async with engine.begin() as connection:
        await connection.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as _session:
        yield _session

    async with engine.begin() as connection:
        await connection.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
async def client(session: AsyncSession):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='https://test'
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
