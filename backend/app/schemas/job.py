from pydantic import BaseModel
from datetime import datetime

class JobOut(BaseModel):
    id: int
    external_id: str
    source: str
    title: str
    company: str
    location: str | None
    url: str
    workplace_type: str | None
    published_at: datetime | None
    found_at: datetime

    model_config = {"from_attributes": True}