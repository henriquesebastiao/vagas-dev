from datetime import datetime

from pytz import utc
from sqlalchemy import DateTime, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, registry

from .enum import JobLevel, JobSource, WorkplaceType

table_registry = registry()


@table_registry.mapped_as_dataclass
class Job:
    __tablename__ = 'jobs'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    keyword: Mapped[str | None] = mapped_column(
        String(255), server_default=None
    )
    source: Mapped[JobSource] = mapped_column(
        String(50)
    )  # "gupy", "linkedin", etc.
    title: Mapped[str] = mapped_column(String(500))
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(String(1000))
    workplace_type: Mapped[WorkplaceType | None] = mapped_column(
        String(7), nullable=True
    )  # remote, hybrid, on-site
    end_applications: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, server_default=None, default=None
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, server_default=None, default=None
    )
    company: Mapped[str | None] = mapped_column(
        String(255), nullable=True, server_default=None, default=None
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, server_default=None, default=None
    )
    external_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, server_default=None, default=None
    )
    found_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(tz=utc),
    )
    telegram_notified: Mapped[bool] = mapped_column(
        init=False, default=False, server_default='false'
    )
    for_pcd: Mapped[bool] = mapped_column(
        default=False, server_default='false'
    )
    level: Mapped[JobLevel | None] = mapped_column(
        String(10), nullable=True, server_default=None, default=None
    )

    __table_args__ = (
        UniqueConstraint('external_id', 'source', name='uq_job_source'),
    )
