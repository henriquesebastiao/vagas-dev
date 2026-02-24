import pytest
from app.main import app
from httpx import ASGITransport, AsyncClient


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='https://test'
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
