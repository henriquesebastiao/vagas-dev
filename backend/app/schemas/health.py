from pydantic import BaseModel


class HealthOut(BaseModel):
    """Schema para resposta de health check"""

    status: str
