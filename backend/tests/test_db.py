from datetime import datetime

from app.models import Job
from sqlalchemy import select


async def test_create_job(session):
    job = Job(
        title='Desenvolvedor Python',
        description='Vaga para desenvolvedor Python com experiência em FastAPI.',
        workplace_type='remote',
        external_id='12345',
        source='gupy',
        company='Tech Company',
        url='https://example.com/job/12345',
        keyword='python',
        location='Brasil',
        published_at=datetime(2024, 6, 1, 12, 0, 0),
        end_applications=datetime(2024, 7, 1, 12, 0, 0),
    )
    session.add(job)
    await session.commit()

    job = await session.scalar(select(Job).where(Job.external_id == '12345'))

    assert job is not None
    assert job.title == 'Desenvolvedor Python'
    assert (
        job.description
        == 'Vaga para desenvolvedor Python com experiência em FastAPI.'
    )
    assert job.workplace_type == 'remote'
    assert job.external_id == '12345'
    assert job.source == 'gupy'
    assert job.company == 'Tech Company'
    assert job.url == 'https://example.com/job/12345'
