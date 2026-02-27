import logging
from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Job

logger = logging.getLogger(__name__)


class BaseJobScraper(ABC):
    """Contrato base para todos os scrapers de vagas.

    Cada fonte (Gupy, LinkedIn, etc.) deve herdar desta classe
    e implementar `fetch_jobs()` com a lógica específica de coleta.
    A lógica de deduplicação e persistência é centralizada aqui,
    e não precisa ser reimplementada nos scrapers filhos.
    """

    # Identificador da fonte, ex: "gupy". Deve ser definido na subclasse.
    source_name: str

    @abstractmethod
    async def fetch_jobs(self) -> list[dict]:
        """
        Coleta vagas da fonte externa e retorna numa estrutura padronizada.

        Cada dict deve conter as chaves esperadas pelo model Job
        (exceto `source` e `found_at`, que são preenchidos por `sync`).
        """
        ...

    async def sync(self, session: AsyncSession) -> int:
        """
        Ponto de entrada principal do ciclo de sincronização.

        Orquestra a coleta e persistência:
            1. Busca as vagas disponíveis na fonte via `fetch_jobs()`
            2. Filtra apenas as vagas ainda não registradas no banco
            3. Persiste as novas vagas e retorna o total inserido

        Retorna o número de novas vagas inseridas nesta execução.
        """
        logger.info(f'Iniciando sincronização para fonte: {self.source_name}')
        jobs = await self.fetch_jobs()
        new_count = 0

        for job_data in jobs:
            exists = await session.scalar(
                select(Job).where(
                    Job.external_id == job_data['external_id'],
                    Job.source == self.source_name,
                )
            )
            if exists:
                # Caso a vaga já exista no banco de dados,
                # pulamos para evitar duplicatas.
                continue

            session.add(
                Job(
                    **job_data,
                    source=self.source_name,
                )
            )
            new_count += 1

        await session.commit()
        logger.info(
            f'[{self.source_name}] {new_count} novas vagas '
            f'inseridas de {len(jobs)} encontradas.'
        )
        return new_count
