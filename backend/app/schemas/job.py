from datetime import datetime

from pydantic import BaseModel

from app.models import JobSource, WorkplaceType


class JobOut(BaseModel):
    """Schema for job output

    Attributes:
        id: ID da vaga no banco de dados
        external_id: ID da vaga no site de origem
        source: Fonte da vaga (e.g. "gupy", "linkedin")
        title: Título da vaga
        company: Empresa contratante
        location: Localização da vaga (e.g. "São Paulo, SP")
        url: URL da vaga no site de origem
        description: Descrição da vaga (pode ser None se não disponível)
        workplace_type: Tipo de trabalho (remote, hybrid, on-site)
            ou None se não disponível
        published_at: Data de publicação da vaga no site de origem ou
            None se não disponível
        end_applications: Data de encerramento das candidaturas ou None
            se não disponível
        found_at: Data em que a vaga foi encontrada e salva no banco de dados
    """

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
