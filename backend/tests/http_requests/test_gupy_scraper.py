import httpx
from app.scrapers.gupy import GupyScraper
from respx import MockRouter


async def test_gupy_scraper_fetch_jobs_timeout(respx_mock: MockRouter):
    # Configura o mock para simular um timeout
    mocked = respx_mock.get(
        'https://employability-portal.gupy.io/api/v1/jobs'
    ).mock(side_effect=httpx.ReadTimeout('timed out'))

    scraper = GupyScraper(keywords=['python'], limit=10)

    # Executa o método e verifica se ele lida com o timeout
    jobs = await scraper.fetch_jobs()

    assert mocked.called
    assert isinstance(jobs, list)
