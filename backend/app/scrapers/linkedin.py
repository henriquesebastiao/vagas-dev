import asyncio
import hashlib
import logging
from http import HTTPStatus

import httpx
from bs4 import BeautifulSoup

from app.scrapers import transport
from app.scrapers.base import BaseJobScraper

logger = logging.getLogger(__name__)

linkedin_level_id = {
    'estagio': 1,
    'junior': 3,
    'pleno': 4,
}

linkedin_workplace_type_id = {
    'remote': 2,
    # 'hybrid': 3,
    # 'on-site': 1,
}


class LinkedInScraper(BaseJobScraper):
    source_name = 'linkedin'
    BASE_URL = 'https://www.linkedin.com'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def fetch_jobs(self) -> list[dict]:
        logger.info(
            'Iniciando coleta de vagas da fonte '
            f'{self.source_name.title()} para keywords: {self.keywords}'
        )
        all_jobs = []

        async with httpx.AsyncClient(
            base_url=self.BASE_URL,
            transport=transport,
            timeout=30,
        ) as client:
            for keyword in self.keywords:
                for level, level_id in linkedin_level_id.items():
                    for (
                        workplace_type,
                        workplace_type_id,
                    ) in linkedin_workplace_type_id.items():
                        while True:
                            params = {
                                'keywords': f'"{keyword}"',
                                'f_E': level_id,
                                'f_WT': workplace_type_id,
                                'location': 'Brasil',
                                'geoId': '106057199',
                            }

                            try:
                                response = await client.get(
                                    '/jobs/search', params=params
                                )
                            except httpx.ReadTimeout:
                                logger.warning(
                                    'Timeout ao buscar vagas para keyword '
                                    f'"{keyword}". Pulando para o próximo keyword.'
                                )
                                break

                            if response.status_code == HTTPStatus.OK:
                                bs = BeautifulSoup(
                                    response.text, 'html.parser'
                                )

                                # Busca pelos links e títulos das vagas.
                                jobs_list = bs.find_all(
                                    'a', {'class': 'base-card__full-link'}
                                )

                                if len(jobs_list) == 0:
                                    break

                                jobs = []

                                for job in jobs_list:
                                    job_data = {
                                        'title': job.get_text(strip=True),
                                        'url': job['href'],
                                    }
                                    jobs.append(job_data)

                                for job in jobs:
                                    external_id = hashlib.md5(
                                        job['title'].encode()
                                    ).hexdigest()[:10]
                                    content = {
                                        'external_id': external_id,
                                        'keyword': keyword,
                                        'title': job['title'],
                                        'description': None,
                                        'company': None,
                                        'location': 'Brasil',
                                        'url': job['url'],
                                        'workplace_type': workplace_type,
                                        'published_at': None,
                                        'end_applications': None,
                                        'for_pcd': False,
                                        'level': level,
                                    }

                                    all_jobs.append(self._parse(content))
                                break
                            elif response.status_code == 999:  # noqa
                                logger.warning(
                                    'Status 999 recebido, tentando novamente...'
                                )
                                await asyncio.sleep(
                                    2
                                )  # Aguarda antes de tentar novamente
                                continue  # Repete o while com os mesmos valores
                            else:
                                logger.warning(
                                    'Erro ao buscar vagas '
                                    f'para keyword "{keyword}". '
                                    f'Status code: {response.status_code}. '
                                    f'Resposta: {response.text[:200]}... '
                                    'Pulando para o próximo keyword.'
                                )
                                break
        return all_jobs

    @staticmethod
    def _parse(raw: dict) -> dict:
        """Normaliza o payload bruto para o formato interno do model."""
        return {
            'external_id': raw.get('external_id', None),
            'keyword': raw.get('keyword', ''),
            'title': raw.get('title', ''),
            'company': raw.get('company', None),
            'location': raw.get('location', ''),
            'url': raw.get('url', ''),
            'description': raw.get('description', None),
            'workplace_type': raw.get('workplace_type'),
            'published_at': raw.get('published_at', None),
            'end_applications': raw.get('end_applications', None),
            'for_pcd': raw.get('for_pcd', False),
            'level': raw.get('level', None),
        }
