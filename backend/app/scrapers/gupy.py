import httpx

from app.scrapers.base import BaseJobScraper


class GupyScraper(BaseJobScraper):
    source_name = 'gupy'
    BASE_URL = 'https://portal.api.gupy.io/api/v1/jobs'

    def __init__(self, keywords: list[str] = None, limit: int = 100):
        self.keywords = keywords or ['python', 'backend']
        self.limit = limit

    async def fetch_jobs(self) -> list[dict]:
        all_jobs = []

        async with httpx.AsyncClient(timeout=30) as client:
            for keyword in self.keywords:
                offset = 0
                while True:
                    params = {
                        'jobName': keyword,
                        'limit': self.limit,
                        'offset': offset,
                    }
                    resp = await client.get(self.BASE_URL, params=params)
                    resp.raise_for_status()
                    data = resp.json()

                    jobs = data.get('data', [])
                    if not jobs:
                        break

                    for job in jobs:
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
        city = raw.get('city')
        state = raw.get('state')

        location = raw.get('country')
        if state:
            location = f'{state}, {location}'
        if city:
            location = f'{city}, {location}'

        return {
            'external_id': str(raw['id']),
            'title': raw.get('name', ''),
            'company': raw.get('careerPageName', ''),
            'location': location,
            'url': raw.get('jobUrl', ''),
            'description': raw.get('description'),
            'workplace_type': raw.get('workplaceType'),
            'published_at': raw.get('publishedDate'),
            'end_applications': raw.get('applicationDeadline'),
        }
