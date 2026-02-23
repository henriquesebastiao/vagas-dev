from datetime import datetime

from pydantic import BaseModel

from app.models import JobSource, WorkplaceType


class JobOut(BaseModel):
    id: int
    external_id: str
    source: JobSource
    title: str
    company: str
    location: str | None
    url: str
    description: str | None
    workplace_type: WorkplaceType | None
    published_at: datetime | None
    end_applications: datetime | None
    found_at: datetime
