# CLAUDE.md

Este arquivo orienta o Claude Code (claude.ai/code) ao trabalhar neste repositório.

## Visão geral

**Vagas Dev** coleta periodicamente vagas de emprego para desenvolvedores (Gupy via API pública, LinkedIn via scraping de HTML), persiste em PostgreSQL, expõe uma API REST (FastAPI) e envia notificações das vagas novas para Telegram (tópicos de um grupo) e Discord (canais de um servidor). Há também uma interface web em Next.js.

Código, comentários, docstrings, logs, mensagens de commit/changelog e documentação são escritos em **português**. Mantenha esse padrão.

## Comandos

Gerenciador de dependências: **uv** (Python 3.14). Os comandos existem no `Makefile` e também como tasks do taskipy em `pyproject.toml`.

```bash
make sync        # uv sync --all-groups + regenera requirements.txt
make dev         # uvicorn com reload em 127.0.0.1:8000 (--app-dir backend)
make test        # pytest -s -x --cov=backend/app -v + relatório HTML
make lint        # yamlfmt, mbake, prettier, eslint (frontend) e ruff
make format      # formata tudo (ruff format + ruff check --fix, prettier, ...)
make radon       # complexidade ciclomática (também roda na CI)
make export      # regenera requirements.txt a partir do uv.lock
make front       # next dev do frontend
make doc         # documentação (zensical) em localhost:3000
make changelog   # towncrier build
```

Rodar um teste específico:

```bash
uv run pytest backend/tests/api/routes/test_job.py::test_list_jobs -s -v
```

- **Os testes precisam de Docker**: `backend/tests/conftest.py` sobe um Postgres real via `testcontainers` (`postgres:18-alpine`) com escopo de sessão; as tabelas são criadas/dropadas por teste via `table_registry.metadata`. Requisições HTTP externas são mockadas com `respx` (fixture `respx_mock`). `asyncio_mode = auto`, então testes `async def` não precisam de decorator.
- Stack completa local: `docker compose up` (app + Postgres + nginx na porta 80; o override expõe 8000 e faz watch de `./backend`). Copie `.env.example` para `.env`.

## Arquitetura

Tudo do backend fica em `backend/app/`. O app é executado com `--app-dir backend`, portanto os imports usam `from app...` (os testes também). Exceção: `migrations/env.py` importa `backend.app...` porque o Alembic roda a partir da raiz (`alembic.ini` → `prepend_sys_path = .`).

Fluxo principal:

1. **Startup** (`main.py`, `lifespan`): configura loguru (intercepta todos os loggers stdlib; grava também em `logs/app.log`), **executa `alembic upgrade head` como subprocesso**, inicia o bot do Discord em background e chama `setup_scheduler()`.
2. **Scheduler** (`scheduler.py`, APScheduler): três jobs com o mesmo intervalo `INTERVAL_SYNC` (minutos) — sync Gupy, sync LinkedIn e notificação de vagas novas.
3. **Scrapers** (`scrapers/`): cada fonte herda de `BaseJobScraper` (`scrapers/base.py`) e implementa apenas `fetch_jobs() -> list[dict]` com dicts nas chaves do model `Job` (exceto `source`/`found_at`). `BaseJobScraper.sync()` centraliza deduplicação (por `external_id` + `source`, também garantida pela `UniqueConstraint uq_job_source`) e persistência. Todos compartilham o `transport` de `scrapers/__init__.py`: httpx com retry (`httpx-retries`) + cache HTTP em SQLite (`hishel`).
   - Gupy: paginação por `offset`, ordenado por data desc; `level` é inferido do título via `utils.get_level_seniority`; descrição HTML limpa em `_clean_description`.
   - LinkedIn: parse com BeautifulSoup; `external_id` é um hash MD5 do título (não há ID real); `level`/`workplace_type` vêm dos filtros usados na busca; status 999 → retry com sleep.
4. **Notificações** (`notifiers.py` + `wrappers/`): busca vagas com `telegram_notified == False` / `discord_notified == False`, envia e marca a flag como `True` vaga a vaga. O roteamento para tópico/canal é feito pela `keyword` usando os conjuntos em `keywords.py` (`PYTHON_KEYWORDS`, `JAVA_KEYWORDS`, ...) mapeados para IDs em `core/settings.py`. Telegram usa rate limit de 20 msg/min (`pyrate-limiter`) e corta a descrição em 4096 caracteres; Discord usa embeds (descrição até 1024).
5. **API** (`api/routes/job.py`, prefixo `/jobs`): `GET /jobs` (filtros `source`, `keyword`, `location`, `workplace_type`, `for_pcd`, `level`, `limit<=200`, `offset`; ordenado por `found_at` desc), `POST /jobs/sync/{source}` (sync em `BackgroundTasks`, retorna 202), `GET /jobs/sources` (contagem por fonte). `GET /health` fica em `main.py`. Swagger em `/`.

Outros pontos:

- `models.py`: único model `Job`, usando `registry().mapped_as_dataclass` (campos com `init=False` não entram no construtor). Sessão injetada via `Session = Annotated[AsyncSession, Depends(get_session)]` em `utils.py`.
- `enum.py`: `JobSource`, `JobLevel`, `WorkplaceType`, `Keyword`. O filtro `keyword` da API só aceita valores do enum `Keyword` e busca **apenas no título** (`ilike`).
- `keywords.KEYWORDS` é a lista de termos buscados automaticamente pelos scrapers.
- Configuração via `pydantic-settings` (`core/settings.py`, lê `.env`, `get_settings()` com `lru_cache`).

## Tarefas comuns

**Adicionar uma nova fonte de vagas:**
1. Criar `backend/app/scrapers/<fonte>.py` herdando `BaseJobScraper`, definindo `source_name`, `BASE_URL` e `fetch_jobs()` (use o `transport` compartilhado).
2. Adicionar o valor em `JobSource` (`enum.py`).
3. Registrar a função de sync e o job em `scheduler.py`.
4. Adicionar ao dicionário `scrapers` em `trigger_sync` (`api/routes/job.py`).

**Adicionar uma nova keyword / categoria de notificação:** atualizar `KEYWORDS` e/ou os conjuntos em `keywords.py`, o enum `Keyword`, e — se for uma nova categoria — os campos `TELEGRAM_*_TOPIC_ID` / `DISCORD_*_CHANNEL_ID` em `settings.py`, `.env.example` e o `if/elif` de roteamento em **ambos** `wrappers/telegram.py` e `wrappers/discord_bot.py`.

**Alterar o schema do banco:** editar `models.py`, depois `uv run alembic revision --autogenerate -m "..."` (Postgres acessível via `DATABASE_URL`). Migrations ficam em `backend/app/migrations/versions/` e são aplicadas automaticamente no startup. Atualize também `schemas/job.py` se o campo for exposto.

**Alterar dependências:** use `uv add`/`uv remove` e depois `make export` — a imagem Docker do backend instala a partir de `requirements.txt`, não do `uv.lock`.

## Convenções

- Ruff: `line-length = 79`, aspas **simples**, regras `I, F, E, W, PL, PT, FAST` (preview). Exceções por arquivo em `[tool.ruff.lint.per-file-ignores]`. Pre-commit roda `uv-lock`, `towncrier-check` e ruff.
- Changelog com towncrier: `uv run towncrier create` gera fragmentos em `changelogs/<tipo>/` (tipos: `feat`, `format`, `bugfix`, `doc`, `core`, `bump`); `make changelog` consolida em `CHANGELOG.md`. A versão está em `backend/app/__init__.py` (`__version__`).
- CI (`.github/workflows/test.yml`): ruff, radon e pytest em todo push/PR.

## Frontend

`frontend/` é Next.js 16 + React 19 + Tailwind 4, em JavaScript (sem TypeScript), com `output: "export"` (site estático). `app/page.js` é um client component que concentra o estado; `lib/api.js` encapsula as chamadas à API usando `NEXT_PUBLIC_API_URL` (padrão `http://localhost:8000`); `lib/constants.js` tem labels/cores de nível e modalidade. Estilos são majoritariamente inline. Deploy no Cloudflare Pages via `.github/workflows/deploy.yml` após a CI passar na `main`. O serviço `ui` no `docker-compose.yml` está comentado e `frontend/Dockerfile` espera build `standalone` (incompatível com o `output: "export"` atual).

## Documentação

Docs em `docs/` com Zensical (`zensical.toml`), publicadas no GitHub Pages a cada push na `main`. Ao mudar endpoints ou o fluxo de contribuição, atualize `README.md` e `docs/` (ex.: `docs/api/endpoints.md`).
