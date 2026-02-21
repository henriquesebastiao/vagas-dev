from datetime import datetime
from enum import Enum

from sqlalchemy.orm import registry, mapped_column, Mapped
from sqlalchemy import String, Text, DateTime, func, UniqueConstraint
import pytz

class JobSource(str, Enum):
    linkedin = "linkedin"
    gupy = "gupy"

table_registry = registry()

@table_registry.mapped_as_dataclass
class Job:
    __tablename__ = "job"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    external_id: Mapped[str] = mapped_column(String(255))
    source: Mapped[JobSource] = mapped_column(String(50))  # "gupy", "linkedin", etc.
    title: Mapped[str] = mapped_column(String(500))
    company: Mapped[str] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(String(1000))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    workplace_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # remote, hybrid, on-site
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    found_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(tz=pytz.timezone("America/Sao_Paulo")))

    __table_args__ = (
        UniqueConstraint("external_id", "source", name="uq_job_source"),
    )

