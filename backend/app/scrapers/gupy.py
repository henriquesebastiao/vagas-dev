import html
import logging
import re

import hishel
import hishel.httpx
import httpx
from httpx_retries import Retry, RetryTransport

from app.keywords import KEYWORDS
from app.scrapers.base import BaseJobScraper
from app.utils import (
    add_time,
    after_request,
    before_request,
    get_level_seniority,
)

logger = logging.getLogger(__name__)


class GupyScraper(BaseJobScraper):
    """
    Scraper para a API pública de vagas da Gupy.

    Busca vagas por lista de palavras-chave, lidando com paginação
    automaticamente. Vagas que aparecem em múltiplos keywords são
    deduplicadas antes de serem enviadas para persistência.
    """

    source_name = 'gupy'
    BASE_URL = 'https://employability-portal.gupy.io/api/v1'

    def __init__(self, keywords: list[str] = None, limit: int = 100):
        """Monta o scraper com os parâmetros de busca.

        Args:
            keywords (list): termos de busca.
                Cada keyword gera uma sequência independente de requests
            limit (int): vagas por página — use o máximo permitido pela API
                para minimizar requests
        """
        self.keywords = keywords or KEYWORDS
        self.limit = limit

    async def fetch_jobs(self) -> list[dict]:
        """Coleta todas as vagas para cada keyword configurado.

        Itera os keywords sequencialmente para não sobrecarregar a API.
        Ao final, deduplicadas por `external_id` antes de retornar,
        pois a mesma vaga pode aparecer em buscas por keywords diferentes.
        """
        logger.info(
            f'Iniciando coleta de vagas da Gupy para keywords: {self.keywords}'
        )
        all_jobs = []

        # Configura retry para lidar com falhas temporárias da API (ex: 500, 502, etc.)
        retry = Retry(total=5, backoff_factor=0.5)
        transport = httpx.AsyncHTTPTransport(verify=False)
        retry_transport = RetryTransport(transport, retry=retry)

        # Cache HTTP para evitar buscar os dados quando não houver mudanças
        transport = hishel.httpx.AsyncCacheTransport(
            next_transport=retry_transport,
            storage=hishel.AsyncSqliteStorage(),
        )

        async with httpx.AsyncClient(
            base_url=self.BASE_URL,
            transport=transport,
            timeout=10,
            event_hooks={
                'request': [before_request, add_time],
                'response': [after_request],
            },
        ) as client:
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

                    try:
                        response = await client.get('/jobs', params=params)
                    except httpx.ReadTimeout:
                        logger.warning(
                            'Timeout ao buscar vagas para keyword '
                            f'"{keyword}" com offset {offset}. '
                            'Pulando para o próximo keyword.'
                        )
                        break

                    response.raise_for_status()
                    data = response.json()

                    jobs = data.get('data', [])
                    if not jobs:
                        break

                    for job in jobs:
                        # marca a vaga com o keyword que a encontrou
                        job['keyword'] = keyword

                        # extrai o nível de senioridade do título da vaga usando a função utilitária
                        title = job.get('name', '')
                        level = get_level_seniority(title)
                        job['level'] = level

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
    def _clean_description(raw_text: str | None) -> str | None:

        # Decodifica entidades HTML (&nbsp; → espaço, &amp; → &, etc.)
        text = html.unescape(raw_text)

        # Remove tags HTML residuais (<br>, <p>, <strong>, etc.)
        text = re.sub(r'<[^>]+>', '\n', text)

        # Remove caracteres de lista estranhos (·, •, ·)
        text = re.sub(r'[·•]', '-', text)

        # Colapsa múltiplos espaços em um só
        text = re.sub(r' {2,}', ' ', text)

        # Colapsa mais de duas quebras de linha seguidas
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Remove espaços no início e fim de cada linha
        lines = [line.strip() for line in text.splitlines()]

        return '\n'.join(lines).strip()

    def _parse(self, raw: dict) -> dict:
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
            'description': self._clean_description(raw.get('description')),
            'workplace_type': raw.get('workplaceType'),
            'published_at': raw.get('publishedDate'),
            'end_applications': raw.get('applicationDeadline'),
            'for_pcd': raw.get('badges', {}).get('isPWD', False),
            'level': raw.get('level', None),
        }
