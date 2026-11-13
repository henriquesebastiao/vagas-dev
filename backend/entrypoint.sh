#!/bin/sh
set -e

# Aplica as migrations uma única vez, antes de subir o servidor.
alembic upgrade head

# O scheduler roda dentro do processo da API: com mais de um worker cada
# processo teria o seu próprio scheduler e as coletas rodariam duplicadas.
# Por isso o padrão é 1 worker (a API é assíncrona e atende bem assim).
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --workers "${WORKERS:-1}" \
    --app-dir backend \
    --proxy-headers \
    --forwarded-allow-ips "*"
