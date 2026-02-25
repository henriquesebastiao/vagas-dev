from app.core.settings import get_settings
from app.wrappers.telegram import BotTelegram


async def notify_new_jobs(jobs: list[dict]):
    """Notifica os usuários sobre novas vagas.

    Envia uma mensagem formatada para os canais
    configurados com as informações das vagas.
    """
    settings = get_settings()

    telegram = BotTelegram(token=settings.TELEGRAM_BOT_TOKEN)

    # Envia notificações com novas vagas para os canais
    await telegram.send_notification_jobs(
        jobs=jobs, chat_id=settings.TELEGRAM_CHAT_ID
    )
