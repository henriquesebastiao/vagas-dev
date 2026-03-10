from http import HTTPStatus

import httpx
from loguru import logger
from pyrate_limiter import limiter_factory
from pyrate_limiter.abstracts.rate import Duration
from pyrate_limiter.extras.httpx_limiter import AsyncRateLimiterTransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.keywords import (
    BACKEND_KEYWORDS,
    FRONTEND_KEYWORDS,
    GOLANG_KEYWORDS,
    JAVA_KEYWORDS,
    PYTHON_KEYWORDS,
)
from app.models import Job


class BotTelegram:
    def __init__(self, token: str):
        self._token = token

    async def send_message(
        self, chat_id: str, text: str, topic_id: str | None = None
    ) -> httpx.Response | None:
        async with httpx.AsyncClient(
            base_url=f'https://api.telegram.org/bot{self._token}', timeout=30
        ) as client:
            payload = {
                'chat_id': chat_id,
                'text': text,
            }

            if topic_id:
                payload['message_thread_id'] = topic_id  # pragma: no cover

            logger.debug(
                'Enviando mensagem para '
                f'chat_id={chat_id} com topic_id={topic_id}'
            )

            try:
                response = await client.post('/sendMessage', json=payload)
            except httpx.ReadTimeout:
                logger.error(
                    'Timeout ao enviar mensagem para '
                    f'chat_id={chat_id} com topic_id={topic_id}'
                )
                return None

            if response.status_code != HTTPStatus.OK:
                logger.error(
                    'Erro ao enviar mensagem: '
                    f'{response.status_code} - {response.text}'
                )

            return response

    async def send_notification_jobs(
        self, jobs: list[dict], chat_id: str, session: AsyncSession
    ) -> bool:
        # Configura um rate limiter para evitar
        # atingir os limites da API do Telegram.
        # 20 mensagens por minuto
        limiter = limiter_factory.create_inmemory_limiter(
            rate_per_duration=20,
            duration=Duration.MINUTE,
        )

        limiter_transport = AsyncRateLimiterTransport(limiter=limiter)

        async with httpx.AsyncClient(
            base_url=f'https://api.telegram.org/bot{self._token}',
            transport=limiter_transport,
            timeout=10,
        ) as client:
            settings = get_settings()

            logger.info(
                '[Telegram] Enviando notificações de vagas para '
                f'chat_id={chat_id} - Total vagas: {len(jobs)}'
            )

            if not jobs:
                logger.info('[Telegram] Nenhuma vaga nova para notificar.')

            for job in jobs:
                keyword = job['keyword']  # noqa
                topic_id = None

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

                description = job['description']

                message = f"""{job['title']}\nEmpresa: {job['company']}
\nLocal: {job['location']}\nModelo: {job['workplace_type']}
\n{description}\n\nLink: {job['url']}"""

                # Verifica se a mensagem excede o limite de
                # caracteres do Telegram (4096 caracteres)
                length_message = len(message)
                if length_message > settings.TELEGRAM_MAX_MESSAGE_LENGTH:
                    exceeded = (
                        length_message - settings.TELEGRAM_MAX_MESSAGE_LENGTH
                    )
                    description = (
                        description[: len(description) - exceeded - 3] + '...'
                    )

                    message = f"""{job['title']}\nEmpresa: {job['company']}
\nLocal: {job['location']}\nModelo: {job['workplace_type']}
\n{description}\n\nLink: {job['url']}"""

                payload = {
                    'chat_id': chat_id,
                    'text': message,
                }

                if topic_id:
                    # Adiciona o ID do tópico ao json da requisição POST
                    payload['message_thread_id'] = topic_id

                try:
                    response = await client.post('/sendMessage', json=payload)
                except httpx.ReadTimeout:
                    logger.error(
                        '[Telegram] Timeout ao enviar mensagem para '
                        f'chat_id={chat_id} com topic_id={topic_id}'
                    )

                    continue

                if response.status_code != HTTPStatus.OK:
                    logger.error(
                        '[Telegram] Erro ao enviar mensagem: '
                        f'{response.status_code} - {response.text}'
                    )
                else:
                    # Marca a vaga como notificada
                    # no banco de dados para evitar
                    job_db = await session.get(Job, job['id'])
                    job_db.telegram_notified = True
                    await session.commit()
            return True
