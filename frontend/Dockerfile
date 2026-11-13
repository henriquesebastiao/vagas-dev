# Interface web do Vagas Dev.
#
# O Next.js está configurado com `output: "export"`, então o build gera um
# site estático em `frontend/out`, servido aqui por um nginx.
#
# Build (a partir da raiz do repositório):
#   docker build -f frontend/Dockerfile -t vagas-ui .
# Execução:
#   docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 vagas-ui

FROM node:20-alpine AS deps

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

FROM node:20-alpine AS builder

WORKDIR /app/frontend

# URL padrão da API, embutida no build. Pode ser trocada sem rebuild com a
# variável de ambiente NEXT_PUBLIC_API_URL ao iniciar o container (ver
# docker-entrypoint.sh). Em ambos os casos é a URL como o NAVEGADOR do
# usuário acessa a API, e não o nome do container na rede do Docker.
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_TELEMETRY_DISABLED=1

COPY --from=deps /app/frontend/node_modules ./node_modules
COPY frontend/ ./

RUN npm run build

FROM nginx:1.31.3-alpine@sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c2c3aeac22d2a470c1752 AS runner

COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --chmod=755 frontend/docker-entrypoint.sh /docker-entrypoint.d/40-vagas-config.sh
COPY --from=builder /app/frontend/out /usr/share/nginx/html

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -q --spider http://127.0.0.1:3000/ || exit 1
