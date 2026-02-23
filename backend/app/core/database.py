from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.settings import get_settings

engine = create_async_engine(get_settings().DATABASE_URL)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
