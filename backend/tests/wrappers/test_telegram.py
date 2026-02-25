import os
from http import HTTPStatus


async def test_telegram_send_message(bot_telegram):
    chat_id = os.getenv('TELEGRAM_CHAT_ID_TEST')
    response = await bot_telegram.send_message(
        chat_id=chat_id, text='Mensagem de teste'
    )

    if response.status_code != HTTPStatus.OK:
        print('Response content:', response.content)

    assert response.status_code == HTTPStatus.OK
    assert response.json()['ok']


async def test_telegram_send_message_with_topic_id(bot_telegram):
    chat_id = os.getenv('TELEGRAM_CHAT_ID_TEST')
    topic_id = os.getenv('TELEGRAM_PYTHON_TOPIC_ID')
    response = await bot_telegram.send_message(
        chat_id=chat_id,
        text='Mensagem de teste com topic_id',
        topic_id=topic_id,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['ok']


async def test_telegram_send_notification_jobs(bot_telegram):
    chat_id = os.getenv('TELEGRAM_CHAT_ID_TEST')

    jobs = []

    data = {
        'title': 'Vaga de Teste',
        'company': 'Empresa de Teste',
        'location': 'Brasil',
        'url': 'https://example.com/job/123',
        'description': 'Descrição da vaga de teste',
        'workplace_type': 'remote',
    }

    keywords = [
        'python',
        'java',
        'golang',
        'frontend',
        'backend',
    ]

    for keyword in keywords:
        job = data.copy()
        job['keyword'] = keyword
        jobs.append(job)

    result = await bot_telegram.send_notification_jobs(
        jobs=jobs, chat_id=chat_id
    )

    assert result
