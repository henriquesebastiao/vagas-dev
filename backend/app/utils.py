import logging
import time
import uuid
from typing import Annotated

import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.enum import JobLevel

Session = Annotated[AsyncSession, Depends(get_session)]
_logger = logging.getLogger(__name__)


def get_level_seniority(title: str) -> str | None:
    """Determina o nível de senioridade da vaga com base no título.

    Usa palavras-chave comuns para classificar a vaga como "junior",
    "pleno" ou "senior". Retorna None se não for possível determinar
    o nível.

    Args:
        title (str): O título da vaga (e.g. "Desenvolvedor Python Pleno")
    """

    estagio = ['estágio', 'estagio']
    junior = ['junior', 'jr', 'júnior']
    pleno = ['pleno', 'pl']
    senior = ['senior', 'sr', 'sênior']

    title = title.lower().split()

    if any(word in title for word in estagio):
        return JobLevel.estagio
    elif any(word in title for word in junior):
        return JobLevel.junior
    elif any(word in title for word in pleno):
        return JobLevel.pleno
    elif any(word in title for word in senior):
        return JobLevel.senior
    else:
        return None


async def before_request(request: httpx.Request):
    request_id = str(uuid.uuid4())
    request.headers['X-Request-ID'] = request_id
    request.extensions['request_id'] = request_id


async def add_time(request: httpx.Request):
    request.extensions['start_time'] = time.monotonic()


async def after_request(response: httpx.Response):
    request = response.request
    start = response.request.extensions.get('start_time', None)
    if start:
        elapsed = time.monotonic() - start
    else:
        elapsed = None

    _logger.info(
        f'{request.method} {request.url} {response.status_code}'
        f'{elapsed} {request.extensions.get("request_id")}'
    )
