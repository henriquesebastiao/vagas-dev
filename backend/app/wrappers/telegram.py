from httpx import AsyncClient


class BotTelegram:
    def __init__(self, token: str):
        self.token = token

    async def send_message(
        self, chat_id: int, text: str, topic_id: int | None = None
    ):
        async with AsyncClient(
            base_url=f'https://api.telegram.org/bot{self.token}', timeout=30
        ) as client:
            payload = {
                'chat_id': chat_id,
                'text': text,
            }

            if topic_id:
                payload['message_thread_id'] = topic_id

            response = await client.post('/sendMessage', json=payload)

            return response
