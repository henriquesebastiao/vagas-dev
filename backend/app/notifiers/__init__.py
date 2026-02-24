async def notify_new_jobs(job: dict):
    """Notifica os usuários sobre novas vagas.

    Por enquanto, só loga no console, mas pode ser expandido para enviar
    emails, mensagens em Slack, etc.
    """
    print(
        f'Nova vaga encontrada: {job["title"]} '
        f'na {job["company"]} - {job["url"]}'
    )
    return True
