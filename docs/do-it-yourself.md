---
icon: lucide/play
---

# Execute você mesmo

Casa você queira, por algum motivo, executar sua própria instância do projeto basta fazer isso via Docker Compose
seguindo os passos abaixo.

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

Este arquivo `docker-compose.yml` quando executado irá criar três containers, sendo eles a API REST, a interface web e o banco de dados, respectivamente.

A API fica em `http://localhost:8000` e a interface em `http://localhost:3000`. Para publicar com domínio e HTTPS, aponte o seu proxy reverso (Traefik, Caddy, Nginx Proxy Manager etc.) para as portas `8000` (API) e `3000` (interface) e defina `NEXT_PUBLIC_API_URL` com o endereço público da API. Os dois containers têm healthcheck (`/health` na API).

## Varáveis de ambiente

Crie um arquivo `.env` no qual vão estar todas as variáveis de ambiente necessárias para o funcionamento do sistema.
Crie o arquivo com o seguinte conteúdo:

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

| Variável        | Descrição                                                      |
|-----------------|----------------------------------------------------------------|
| `INTERVAL_SYNC` | Intervalo em minutos entre cada ciclo de busca por novas vagas. A primeira busca acontece assim que a API inicia |
| `WORKERS`       | Opcional. Número de processos da API (padrão `1`). Mantenha `1`: cada processo roda o seu próprio agendador, e mais de um duplicaria as buscas |

### Interface web

| Variável              | Descrição                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `NEXT_PUBLIC_API_URL` | URL da API como o navegador do usuário a acessa — em produção aponte para o domínio da sua API; localmente use `http://localhost:8000`. Não use o nome do container (ex.: `http://api:8000`), pois quem faz as requisições é o navegador. O container da interface lê esta variável ao iniciar, sem precisar de novo build |

## Executando

Após criar os arquivos `docker-compose.yml` e `.env`, agora você pode executar os container do sistema com o comando:

```shell
docker compose -f docker-compose.yml up -d
```