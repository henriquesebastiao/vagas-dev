lint:
	yamlfmt -lint .
	mbake format --check Makefile
	prettier --check frontend/.
	uv run ruff check .; uv run ruff check . --diff

format:
	yamlfmt .
	mbake format Makefile
	prettier --write frontend/.
	ruff format .; ruff check . --fix

radon:
	uv run radon cc ./backend -a -na

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --app-dir backend

dev:
	uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 --app-dir backend --reload --log-level debug

front:
	npm run dev --prefix frontend

doc:
	uv run zensical serve --dev-addr localhost:3000 --open

test:
	uv run pytest -s -x --cov=backend/app -v; coverage html

sync:
	uv sync --all-groups
	uv export --no-hashes --no-dev -o requirements.txt

export:
	uv export --no-hashes --no-dev -o requirements.txt

changelog:
	uv run towncrier build

safety:
	uv run safety scan

.PHONY: lint format radon run dev doc test sync export changelog front safety