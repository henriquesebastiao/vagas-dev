from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import get_settings

engine = create_async_engine(get_settings().DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
