import logging
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status
from sqlalchemy import func, select

from app.enum import JobLevel, JobSource, Keyword, WorkplaceType
from app.models import Job
from app.schemas import Message
from app.schemas.job import JobOut, SourceOut
from app.scrapers.gupy import GupyScraper
from app.utils import Session

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.get('', response_model=list[JobOut])
async def list_jobs(
    session: Session,
    source: Annotated[JobSource | None, Query()] = None,
    keyword: Annotated[Keyword | None, Query()] = None,
    location: Annotated[str | None, Query()] = None,
    workplace_type: Annotated[WorkplaceType | None, Query()] = None,
    for_pcd: Annotated[bool | None, Query()] = None,
    level: Annotated[JobLevel | None, Query()] = None,
    limit: Annotated[int, Query(le=200)] = 50,
    offset: Annotated[int, Query()] = 0,
):
    """
    Lista as vagas de emprego encontradas com base nos filtros opcionais.
    Os seguintes filtros estão disponíveis:

    - **source**: filtra por fonte de onde a vaga foi coletada (ex: "gupy")
    - **keyword**: busca por palavra-chave no título ou descrição da vaga
    - **location**: filtra por localidade (ex: "Brasil", "São Paulo", etc.)
    - **workplace_type**: filtra por tipo de trabalho (ex: "remote", "hybrid", "on-site")
    - **for_pcd**: filtra por vagas destinadas a pessoas com deficiência (true/false)
    - **level**: filtra por nível de senioridade (ex: "junior", "pleno", "senior", "estagio", "trainee")
    - **limit**: número máximo de vagas a retornar (padrão: 50, máximo: 200)
    - **offset**: número de vagas a pular para paginação (padrão: 0)
    """
    query = select(Job).order_by(Job.found_at.desc())

    if source:
        source = source.value
        query = query.where(Job.source == source)
    if keyword:
        keyword = keyword.value
        query = query.where(Job.title.ilike(f'%{keyword}%'))
    if location:
        query = query.where(Job.location.ilike(f'%{location}%'))
    if workplace_type:
        workplace_type = workplace_type.value
        query = query.where(Job.workplace_type == workplace_type)
    if for_pcd:
        query = query.where(Job.for_pcd == for_pcd)
    if level:
        level = level.value
        query = query.where(Job.level == level)

    query = query.limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


@router.post(
    '/sync/{source}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Message,
)
async def trigger_sync(
    source: JobSource, background_tasks: BackgroundTasks, session: Session
):
    """Dispara uma sincronização manual via endpoint."""
    logger.info(f'Iniciando sync manual para fonte: {source}')
    scrapers = {'gupy': GupyScraper}

    if source not in scrapers:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Source '{source}' não suportado."
        )

    async def _run():
        await scrapers[source]().sync(session)

    background_tasks.add_task(_run)
    return {'message': f"Sync de '{source}' iniciado em background."}


@router.get('/sources', response_model=list[SourceOut])
async def list_sources(db: Session):
    result = await db.execute(
        select(Job.source, func.count(Job.id)).group_by(Job.source)
    )
    return [{'source': r[0], 'count': r[1]} for r in result.all()]
