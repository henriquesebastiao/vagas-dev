---
icon: lucide/play
---

# Execute você mesmo

Você pode executar a sua própria instância do Vagas Dev com Docker Compose, usando as imagens publicadas a cada
release no GitHub Container Registry:

| Imagem                                     | Conteúdo                                 | Porta  |
|--------------------------------------------|------------------------------------------|--------|
| `ghcr.io/henriquesebastiao/vagas-dev/api`  | API REST e coleta periódica de vagas     | `8000` |
| `ghcr.io/henriquesebastiao/vagas-dev/ui`   | Interface web (site estático em nginx)   | `3000` |

Além delas é necessário um PostgreSQL. As tags disponíveis são `latest` e a versão de cada release.

## Arquivo `docker-compose.yml`

Crie um arquivo docker compose com o seguinte conteúdo:

```yaml
services:
  api:
    image: ghcr.io/henriquesebastiao/vagas-dev/api:latest
    container_name: api
    restart: always
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      database:
        condition: service_healthy

  ui:
    container_name: ui
    image: ghcr.io/henriquesebastiao/vagas-dev/ui:latest
    restart: always
    depends_on:
      - api
    environment:
      # URL da API como o navegador acessa (não use o nome do container)
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL:-http://localhost:8000}
    ports:
      - "3000:3000"

  database:
    container_name: database
    image: postgres:18.4-alpine
    # Sem `ports`: o banco só precisa ser acessível pela API, na rede interna.
    volumes:
      # A partir do Postgres 18 o volume é montado em /var/lib/postgresql
      - pgdata:/var/lib/postgresql
    env_file:
      - .env
    restart: always
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}" ]
      interval: 10s
      retries: 5
      start_period: 30s
      timeout: 10s

volumes:
  pgdata:
```

Esse arquivo cria três containers: a API, a interface web e o banco de dados. A API fica em
`http://localhost:8000` e a interface em `http://localhost:3000`.

Se você já tem um compose com outros serviços, basta copiar os três serviços (e o volume) para ele. Ajuste os nomes
como preferir, lembrando que o host em `DATABASE_URL` deve ser o nome do serviço do banco.

## Variáveis de ambiente

Crie um arquivo `.env` na mesma pasta do `docker-compose.yml` com o conteúdo abaixo. A API e o banco o leem pelo
`env_file`, e o Docker Compose usa `NEXT_PUBLIC_API_URL` para preencher a variável do serviço `ui`.

```dotenv
POSTGRES_DB="vagas-db"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="password"
POSTGRES_HOST="database"
POSTGRES_PORT="5432"

# O host é o nome do serviço do banco no docker-compose.yml
DATABASE_URL="postgresql+psycopg://postgres:password@database:5432/vagas-db"

# App
INTERVAL_SYNC="30" # Intervalo de sincronização em minutos

# UI
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

Abaixo a descrição de cada variável:

### Banco de dados

| Variável            | Descrição                                                                        |
|---------------------|----------------------------------------------------------------------------------|
| `POSTGRES_DB`       | Nome do banco de dados que será criado no PostgreSQL                             |
| `POSTGRES_USER`     | Usuário do PostgreSQL                                                            |
| `POSTGRES_PASSWORD` | Senha do usuário do PostgreSQL — use uma senha forte em produção                 |
| `POSTGRES_HOST`     | Host do banco de dados — use `database` para referenciar o container do compose  |
| `POSTGRES_PORT`     | Porta do PostgreSQL — padrão `5432`                                              |
| `DATABASE_URL`      | URL de conexão completa usada pelo SQLAlchemy — deve refletir as variáveis acima |

### Aplicação

| Variável        | Descrição |
|-----------------|-----------|
| `INTERVAL_SYNC` | Intervalo em minutos entre cada ciclo de busca por novas vagas. A primeira busca acontece assim que a API inicia |
| `WORKERS`       | Opcional. Número de processos da API (padrão `1`). Mantenha `1`: cada processo roda o seu próprio agendador, e mais de um duplicaria as buscas |

### Interface web

| Variável              | Descrição |
|-----------------------|-----------|
| `NEXT_PUBLIC_API_URL` | URL da API como o navegador do usuário a acessa — em produção aponte para o domínio da sua API; localmente use `http://localhost:8000`. Não use o nome do container (ex.: `http://api:8000`), pois quem faz as requisições é o navegador. O container da interface lê esta variável ao iniciar, sem precisar de novo build |

## Executando

Com os arquivos `docker-compose.yml` e `.env` criados, suba os containers:

```shell
docker compose up -d
```

Ao iniciar, a API aplica as migrations do banco e faz a primeira coleta de vagas; depois repete a coleta a cada
`INTERVAL_SYNC` minutos. Acompanhe pelos logs:

```shell
docker compose logs -f api
```

Os containers da API e da interface têm healthcheck: `docker compose ps` mostra `healthy` quando estão prontos.

## Publicando com domínio e HTTPS

O projeto não inclui proxy reverso. Use o que você já tem no servidor (Traefik, Caddy, Nginx Proxy Manager etc.):

1. Aponte um domínio para a API (porta `8000`) e outro para a interface (porta `3000`).
2. Defina `NEXT_PUBLIC_API_URL` com o endereço público da API, por exemplo `https://vagas-api.seudominio.com`.
3. Recrie o container da interface para aplicar o valor: `docker compose up -d ui`.

Se o proxy estiver na mesma rede Docker, as linhas `ports` da API e da interface podem ser removidas.

## Atualizando

```shell
docker compose pull
docker compose up -d
```

As migrations de banco de uma nova versão são aplicadas automaticamente quando a API reinicia.
