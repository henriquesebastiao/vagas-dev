import httpx
from app.scrapers.gupy import GupyScraper
from app.wrappers.telegram import BotTelegram
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


async def test_telegram_bot_send_message_timeout(respx_mock: MockRouter):
    # Configura o mock para simular um timeout
    mocked = respx_mock.post(
        'https://api.telegram.org/botfake-token/sendMessage'
    ).mock(side_effect=httpx.ReadTimeout('timed out'))

    bot = BotTelegram(token='fake-token')

    # Executa o método e verifica se ele lida com o timeout
    response = await bot.send_message(chat_id='12345', text='Hello')

    assert mocked.called
    assert response is None  # O método deve retornar None em caso de timeout
