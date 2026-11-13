<h1 align="center">
  <a href="https://github.com/henriquesebastiao/vagas-dev" target="_blank" rel="noopener noreferrer">
    <picture>
      <img width="599" height="337" alt="Vagas Dev Banner" src="https://github.com/user-attachments/assets/958395bc-3201-4f6f-ba3b-0bf897624f48" />
    </picture>
  </a>
</h1>
<p align="center"><i>Buscador de vagas de trabalho para desenvolvedores no Brasil</i></p>

<div align="center">
  
  [![Test](https://github.com/henriquesebastiao/vagas-dev/actions/workflows/test.yml/badge.svg)](https://github.com/henriquesebastiao/vagas-dev/actions/workflows/test.yml)
  [![Build](https://github.com/henriquesebastiao/vagas-dev/actions/workflows/deploy.yml/badge.svg)](https://github.com/henriquesebastiao/vagas-dev/actions/workflows/deploy.yml)
  [![GitHub Release](https://img.shields.io/github/v/release/henriquesebastiao/vagas-dev?color=blue)](https://github.com/henriquesebastiao/vagas-dev/releases)
  [![Visitors](https://api.visitorbadge.io/api/visitors?path=henriquesebastiao%2Fvagas-dev&label=repository%20visits&countColor=%231182c3&style=flat)](https://github.com/henriquesebastiao/vagas-dev)

</div>

## O que é e por quê?

Um buscador de vagas de emprego para desenvolvedores no Brasil.

As vagas de desenvolvimento de software estão espalhadas por várias plataformas. O Vagas Dev coleta automaticamente as vagas dessas fontes, guarda tudo em um único banco e permite consultar e filtrar por cargo, empresa, nível, modalidade (remoto, híbrido, presencial), local e vagas para pessoas com deficiência.

O sistema é formado por:

- uma **API REST** (FastAPI) que busca vagas novas periodicamente em segundo plano e as disponibiliza com filtros;
- uma **interface web** (Next.js) para navegar pelas vagas e abrir a candidatura no site de origem.

Links da instância pública:

- [Interface web](https://vagas.henriquesebastiao.com/)
- [API](https://vagas-api.henriquesebastiao.com/) (documentação interativa na própria raiz)
- [Documentação](https://henriquesebastiao.github.io/vagas-dev/)

> [!IMPORTANT]
> O projeto está em fase inicial de desenvolvimento. Contribuições, relatos de bugs e sugestões são bem-vindos via issue ou PR.

## Funcionalidades

- **Busca periódica automática**: a API coleta vagas novas assim que inicia e depois a cada `INTERVAL_SYNC` minutos, sem intervenção manual.
- **Sem vagas duplicadas**: vagas já registradas (mesmo ID externo e mesma fonte) são ignoradas, não importa quantas vezes a coleta rode.
- **Nível da vaga deduzido do título**: estágio, júnior, pleno ou sênior, quando o título indica.
- **API REST centralizada**: todas as vagas de todas as fontes em um único endpoint, com filtros e paginação.
- **Sincronização manual**: dispare uma coleta sob demanda por endpoint, sem esperar o próximo ciclo.
- **Interface web**: lista de vagas com filtros, painel de detalhes, tema claro e escuro e layout para celular.
- **Execução via Docker**: imagens prontas da API e da interface, publicadas a cada release.
- **Arquitetura extensível**: uma nova fonte exige apenas um novo scraper; persistência e deduplicação já estão prontas.

## Fontes suportadas

| Fonte    | Método                        | Status                                                                  |
|----------|-------------------------------|-------------------------------------------------------------------------|
| Gupy     | API pública                   | ⚠️ Indisponível: o endpoint usado pelo scraper passou a responder 404    |
| LinkedIn | Scraping da página de busca   | ✅ Disponível (vagas remotas; sem empresa e descrição)                   |

Novas fontes podem ser adicionadas com um scraper que herda de `BaseJobScraper` (veja [Contribuindo](#contribuindo)).

## API

| Método | Rota                  | Descrição                                          |
|--------|-----------------------|----------------------------------------------------|
| `GET`  | `/jobs`               | Lista vagas com filtros opcionais                  |
| `POST` | `/jobs/sync/{source}` | Dispara uma coleta manual da fonte (`gupy`, `linkedin`) |
| `GET`  | `/jobs/sources`       | Lista as fontes e a quantidade de vagas de cada uma |
| `GET`  | `/health`             | Health check da aplicação                          |

A documentação interativa (Swagger) fica na raiz da API (`/`) e a alternativa em `/redoc`.

### Filtros de `GET /jobs`

| Parâmetro        | Tipo   | Descrição                                                        |
|------------------|--------|------------------------------------------------------------------|
| `keyword`        | string | Texto buscado no título da vaga (ex.: `python`, `react`)         |
| `company`        | string | Texto buscado no nome da empresa                                 |
| `source`         | string | Fonte: `gupy` ou `linkedin`                                      |
| `location`       | string | Texto buscado no local (cidade, estado ou país)                  |
| `workplace_type` | string | `remote`, `hybrid` ou `on-site`                                  |
| `level`          | string | `estagio`, `junior`, `pleno`, `senior` ou `trainee`              |
| `for_pcd`        | bool   | `true` para apenas vagas para pessoas com deficiência            |
| `limit`          | int    | Máximo de resultados (padrão 50, máximo 200)                     |
| `offset`         | int    | Quantidade de vagas a pular, para paginação                      |

As vagas são retornadas da mais recente para a mais antiga (data em que foram encontradas).

## Executando com Docker

As imagens são publicadas no GitHub Container Registry a cada release:

- `ghcr.io/henriquesebastiao/vagas-dev/api`
- `ghcr.io/henriquesebastiao/vagas-dev/ui`

O passo a passo completo (compose, variáveis de ambiente e uso atrás de um proxy reverso) está em [Execute você mesmo](https://henriquesebastiao.github.io/vagas-dev/do-it-yourself/).

Para subir tudo a partir do código deste repositório:

```shell
cp .env.example .env
docker compose up -d --build
```

A API fica em `http://localhost:8000` e a interface em `http://localhost:3000`.

## Desenvolvimento

Requisitos: Python 3.14 com [uv](https://docs.astral.sh/uv/), Node.js 20 e Docker (os testes sobem um PostgreSQL com testcontainers).

```shell
make sync    # instala as dependências (inclusive de desenvolvimento e docs)
make dev     # API com hot reload em http://127.0.0.1:8000
make front   # interface em http://localhost:3000
make test    # testes com cobertura
make lint    # verificação de estilo (Python, frontend, YAML, Makefile)
make format  # formatação automática
make doc     # documentação em http://localhost:3000
```

A API aplica as migrations do banco automaticamente ao iniciar. Para criar uma migration depois de alterar `backend/app/models.py`:

```shell
uv run alembic revision --autogenerate -m "descrição da mudança"
```

Depois de adicionar ou remover dependências Python, rode `make export`: a imagem Docker da API instala a partir do `requirements.txt`.

## Contribuindo

### Como adicionar um novo scraper

1. Crie `backend/app/scrapers/minha_fonte.py` com uma classe que herda de `BaseJobScraper` e define `source_name` e `BASE_URL`.
2. Implemente `fetch_jobs()` retornando uma lista de dicts com as chaves do model `Job` (exceto `source` e `found_at`, preenchidos automaticamente).
3. Adicione a fonte ao enum `JobSource` em `backend/app/enum.py`.
4. Registre a coleta periódica em `backend/app/scheduler.py`.
5. Adicione o scraper ao dicionário `scrapers` de `trigger_sync` em `backend/app/api/routes/job.py`.

```python
import httpx

from app.scrapers import build_transport
from app.scrapers.base import BaseJobScraper


class MinhaFonteScraper(BaseJobScraper):
    source_name = 'minha_fonte'
    BASE_URL = 'https://exemplo.com'

    async def fetch_jobs(self) -> list[dict]:
        # Crie um transport novo para cada client (retry + cache HTTP)
        async with httpx.AsyncClient(
            base_url=self.BASE_URL, transport=build_transport()
        ) as client:
            ...
```

## Tecnologias utilizadas

- **FastAPI**: API REST assíncrona
- **SQLAlchemy (async) + Alembic**: ORM, acesso ao banco e migrations
- **PostgreSQL**: banco de dados
- **APScheduler**: agendamento das coletas
- **httpx + BeautifulSoup**: requisições HTTP e scraping
- **Pydantic**: validação e serialização de dados
- **Next.js + React**: interface web (exportada como site estático)
- **Docker**: execução da API, da interface e do banco
