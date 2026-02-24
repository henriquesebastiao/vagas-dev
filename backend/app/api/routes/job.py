from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status
from sqlalchemy import func, or_, select

from app.models import Job
from app.schemas.job import JobOut
from app.scrapers.gupy import GupyScraper
from app.utils import Session

router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.get('/', response_model=list[JobOut])
async def list_jobs(
    session: Session,
    source: Annotated[str | None, Query()] = None,
    keyword: Annotated[str | None, Query()] = None,
    location: Annotated[str | None, Query()] = None,
    workplace_type: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(le=200)] = 50,
    offset: Annotated[int, Query()] = 0,
):
    query = select(Job).order_by(Job.found_at.desc())

    if source:
        query = query.where(Job.source == source)
    if keyword:
        query = query.where(
            or_(
                Job.title.ilike(f'%{keyword}%'),
                Job.description.ilike(f'%{keyword}%'),
            )
        )
    if location:
        query = query.where(Job.location.ilike(f'%{location}%'))
    if workplace_type:
        query = query.where(Job.workplace_type == workplace_type)

    query = query.limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/sync/{source}', status_code=status.HTTP_202_ACCEPTED)
async def trigger_sync(
    source: str, background_tasks: BackgroundTasks, session: Session
):
    """Dispara uma sincronização manual via endpoint."""
    scrapers = {'gupy': GupyScraper}

    if source not in scrapers:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Source '{source}' não suportado."
        )

    async def _run():
        await scrapers[source]().sync(session)

    background_tasks.add_task(_run)
    return {'message': f"Sync de '{source}' iniciado em background."}


@router.get('/sources')
async def list_sources(db: Session):
    result = await db.execute(
        select(Job.source, func.count(Job.id)).group_by(Job.source)
    )
    return [{'source': r[0], 'count': r[1]} for r in result.all()]
