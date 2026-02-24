from datetime import datetime
from enum import Enum

from pytz import utc
from sqlalchemy import DateTime, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, registry


class JobSource(str, Enum):
    linkedin = 'linkedin'
    gupy = 'gupy'


class WorkplaceType(str, Enum):
    remote = 'remote'
    hybrid = 'hybrid'
    on_site = 'on-site'


table_registry = registry()


@table_registry.mapped_as_dataclass
class Job:
    __tablename__ = 'jobs'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    external_id: Mapped[str] = mapped_column(String(255))
    source: Mapped[JobSource] = mapped_column(
        String(50)
    )  # "gupy", "linkedin", etc.
    title: Mapped[str] = mapped_column(String(500))
    company: Mapped[str] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(String(1000))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    workplace_type: Mapped[WorkplaceType | None] = mapped_column(
        String(7), nullable=True
    )  # remote, hybrid, on-site
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    end_applications: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    found_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(tz=utc),
    )
    notified: Mapped[bool] = mapped_column(
        init=False, default=False, server_default='false'
    )

    __table_args__ = (
        UniqueConstraint('external_id', 'source', name='uq_job_source'),
    )
