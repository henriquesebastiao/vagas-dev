from httpx import AsyncClient

from app.keywords import KEYWORDS
from app.scrapers.base import BaseJobScraper


class GupyScraper(BaseJobScraper):
    """
    Scraper para a API pública de vagas da Gupy.

    Busca vagas por lista de palavras-chave, lidando com paginação
    automaticamente. Vagas que aparecem em múltiplos keywords são
    deduplicadas antes de serem enviadas para persistência.
    """

    source_name = 'gupy'
    BASE_URL = 'https://employability-portal.gupy.io/api/v1/jobs'

    def __init__(self, keywords: list[str] = None, limit: int = 100):
        """Monta o scraper com os parâmetros de busca.

        Args:
            keywords (list): termos de busca.
                Cada keyword gera uma sequência independente de requests.
            limit (int): vagas por página — use o máximo permitido pela API
                para minimizar requests.
        """
        self.keywords = keywords or KEYWORDS
        self.limit = limit

    async def fetch_jobs(self) -> list[dict]:
        """Coleta todas as vagas para cada keyword configurado.

        Itera os keywords sequencialmente para não sobrecarregar a API.
        Ao final, deduplicadas por `external_id` antes de retornar,
        pois a mesma vaga pode aparecer em buscas por keywords diferentes.
        """
        all_jobs = []

        async with AsyncClient(timeout=30) as client:
            for keyword in self.keywords:
                offset = 0
                while True:
                    params = {
                        'jobName': keyword,
                        'limit': self.limit,
                        'offset': offset,
                        # Ordenar por data de publicação para pegar as vagas mais recentes primeiro
                        'sortBy': 'publishedDate',
                        # Ordenar decrescente para garantir que as vagas mais recentes venham primeiro
                        'sortOrder': 'desc',
                    }
                    response = await client.get(self.BASE_URL, params=params)
                    response.raise_for_status()
                    data = response.json()

                    jobs = data.get('data', [])
                    if not jobs:
                        break

                    for job in jobs:
                        # marca a vaga com o keyword que a encontrou
                        job['keyword'] = keyword
                        all_jobs.append(self._parse(job))

                    # Paginação
                    if len(jobs) < self.limit:
                        break
                    offset += self.limit

        # Deduplicar por external_id (pode aparecer em múltiplos keywords)
        seen = {}
        for job in all_jobs:
            seen[job['external_id']] = job
        return list(seen.values())

    @staticmethod
    def _parse(raw: dict) -> dict:
        """Normaliza o payload bruto da API para o formato interno do model.

        Isola o acoplamento com o contrato da API da Gupy neste único método:
        se a API mudar campos, só aqui precisa ser atualizado.
        """

        city = raw.get('city')
        state = raw.get('state')

        location = raw.get('country')
        if state:
            location = f'{state}, {location}'
        if city:
            location = f'{city}, {location}'

        return {
            'external_id': str(raw['id']),
            'keyword': raw.get('keyword', ''),
            'title': raw.get('name', ''),
            'company': raw.get('careerPageName', ''),
            'location': location,
            'url': raw.get('jobUrl', ''),
            'description': raw.get('description'),
            'workplace_type': raw.get('workplaceType'),
            'published_at': raw.get('publishedDate'),
            'end_applications': raw.get('applicationDeadline'),
        }
