from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Job
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseJobScraper(ABC):
    source_name: str

    @abstractmethod
    async def fetch_jobs(self) -> list[dict]:
        """Retorna lista de vagas no formato padronizado"""
        ...

    async def sync(self, db: AsyncSession) -> int:
        """Busca vagas e salva apenas as novas. Retorna quantas foram inseridas."""
        jobs = await self.fetch_jobs()
        new_count = 0

        for job_data in jobs:
            exists = await db.scalar(
                select(Job).where(
                    Job.external_id == job_data["external_id"],
                    Job.source == self.source_name,
                )
            )
            if exists:
                continue

            db.add(Job(**job_data, source=self.source_name, found_at=datetime.utcnow()))
            new_count += 1

        await db.commit()
        logger.info(f"[{self.source_name}] {new_count} novas vagas inseridas de {len(jobs)} encontradas.")
        return new_count