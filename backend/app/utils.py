from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.enum import JobLevel

Session = Annotated[AsyncSession, Depends(get_session)]


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
