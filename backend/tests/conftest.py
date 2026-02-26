import pytest
from app.core.database import get_session
from app.main import app
from app.models import table_registry
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer


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
