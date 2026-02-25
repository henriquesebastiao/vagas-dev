from httpx import AsyncClient, Response

from app.core.settings import get_settings
from app.keywords import (
    BACKEND_KEYWORDS,
    FRONTEND_KEYWORDS,
    GOLANG_KEYWORDS,
    JAVA_KEYWORDS,
    PYTHON_KEYWORDS,
)


class BotTelegram:
    def __init__(self, token: str):
        self._token = token

    async def send_message(
        self, chat_id: str, text: str, topic_id: str | None = None
    ) -> Response:
        async with AsyncClient(
            base_url=f'https://api.telegram.org/bot{self._token}', timeout=30
        ) as client:
            payload = {
                'chat_id': chat_id,
                'text': text,
            }

            if topic_id:
                payload['message_thread_id'] = topic_id  # pragma: no cover

            response = await client.post('/sendMessage', json=payload)

            return response

    async def send_notification_jobs(
        self, jobs: list[dict], chat_id: str
    ) -> bool:
        async with AsyncClient(
            base_url=f'https://api.telegram.org/bot{self._token}', timeout=30
        ) as client:
            for job in jobs:
                keyword = job['keyword']
                topic_id = None
                settings = get_settings()

                # Define qual o tópico correto para enviar
                # a vaga com base na sua palavra-chave
                if keyword in PYTHON_KEYWORDS:
                    topic_id = settings.TELEGRAM_PYTHON_TOPIC_ID
                elif keyword in JAVA_KEYWORDS:
                    topic_id = settings.TELEGRAM_JAVA_TOPIC_ID
                elif keyword in GOLANG_KEYWORDS:
                    topic_id = settings.TELEGRAM_GOLANG_TOPIC_ID
                elif keyword in FRONTEND_KEYWORDS:
                    topic_id = settings.TELEGRAM_FRONTEND_TOPIC_ID
                elif keyword in BACKEND_KEYWORDS:
                    topic_id = settings.TELEGRAM_BACKEND_TOPIC_ID

                message = f"""{job['title']}\nEmpresa: {job['company']}
\nLocal: {job['location']}\nModelo: {job['workplace_type']}
\n\n{job['description']}\n\nLink: {job['url']}"""

                payload = {
                    'chat_id': chat_id,
                    'text': message,
                }

                if topic_id:
                    # Adiciona o ID do tópico ao json da requisição POST
                    payload['message_thread_id'] = topic_id

                await client.post('/sendMessage', json=payload)
            return True
