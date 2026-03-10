import asyncio

import discord
from discord.ext import commands
from loguru import logger
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

settings = get_settings()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    activity=discord.Game(name='Buscando vagas...'),
    application_id=settings.DISCORD_BOT_ID,
)


async def send_notification_jobs(
    jobs: list[dict], session: AsyncSession
) -> bool:
    await bot.wait_until_ready()
    guild = await bot.fetch_guild(settings.DISCORD_GUILD_ID)

    logger.info(f'[Discord] Enviando notificações - Total vagas: {len(jobs)}')

    if not jobs:
        logger.info('[Discord] Nenhuma vaga nova para notificar.')
        return True

    for job in jobs:
        keyword = job['keyword']  # noqa
        channel_id = None

        # Define o canal/fórum correto com base na keyword,
        # seguindo o mesmo padrão de tópicos do Telegram
        if keyword in PYTHON_KEYWORDS:
            channel_id = settings.DISCORD_PYTHON_CHANNEL_ID
        elif keyword in JAVA_KEYWORDS:
            channel_id = settings.DISCORD_JAVA_CHANNEL_ID
        elif keyword in GOLANG_KEYWORDS:
            channel_id = settings.DISCORD_GOLANG_CHANNEL_ID
        elif keyword in FRONTEND_KEYWORDS:
            channel_id = settings.DISCORD_FRONTEND_CHANNEL_ID
        elif keyword in BACKEND_KEYWORDS:
            channel_id = settings.DISCORD_BACKEND_CHANNEL_ID

        # Usa o canal específico da keyword ou o canal padrão
        channel = await guild.fetch_channel(channel_id)

        if not channel:
            logger.error(f'[Discord] Canal {channel_id} não encontrado.')
            continue

        description = job['description'] or ''

        max_desc_length = settings.DISCORD_MAX_DESCRIPTION_LENGTH
        if len(description) > max_desc_length:
            description = description[: max_desc_length - 3] + '...'

        embed = discord.Embed(
            title=job['title'],
            url=job['url'],
            color=discord.Color.blurple(),
        )
        embed.add_field(name='Empresa', value=job['company'], inline=True)
        embed.add_field(
            name='Local',
            value=job['location'] or 'Não informado',
            inline=True,
        )
        embed.add_field(
            name='Modalidade',
            value=job['workplace_type'] or 'N/A',
            inline=True,
        )

        if description:
            embed.add_field(name='Descrição', value=description, inline=False)

        embed.add_field(name='Link', value=job['url'], inline=False)
        embed.set_footer(text=f'Fonte: {job["source"]} • keyword: {keyword}')

        try:
            await channel.send(embed=embed)

            # Marca a vaga como notificada no banco
            # para evitar reenvio na próxima execução
            job_db = await session.get(Job, job['id'])
            job_db.discord_notified = True
            await session.commit()

            # Pausa entre mensagens para não sobrecarregar a API do Discord
            # Discord permite ~5 mensagens/segundo por canal
            await asyncio.sleep(0.5)

        except discord.HTTPException as e:
            logger.error(
                f'[Discord] Erro ao enviar mensagem: {e.status} - {e.text}'
            )
            continue
    return True
