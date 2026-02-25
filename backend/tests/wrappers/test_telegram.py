import os
from http import HTTPStatus


async def test_telegram_send_message(bot_telegram):

    chat_id = os.getenv('TELEGRAM_CHAT_ID_TEST')
    response = await bot_telegram.send_message(
        chat_id=chat_id, text='Mensagem de teste', topic_id='1'
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['ok']
