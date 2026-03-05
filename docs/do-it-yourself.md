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
    image: hcr.io/henriquesebastiao/vagas-dev/ui:latest
    restart: always
    depends_on:
      - app
    environment:
      - NEXT_PUBLIC_API_URL=http://api:8000
    ports:
      - "3000:3000"

  database:
    container_name: database
    image: postgres:18.3-alpine
    ports:
      - "8016:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
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

## Varáveis de ambiente

Crie um arquivo `.env` no qual vão estar todas as variáveis de ambiente necessárias para o funcionamento do sistema.
Crie o arquivo com o seguinte conteúdo:

```dotenv
POSTGRES_DB="vagas-db"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="password"
POSTGRES_HOST="vagas-db"
POSTGRES_PORT="5432"

DATABASE_URL="postgresql+psycopg://postgres:password@vagas-db:5432/vagas-db"

# App
INTERVAL_SYNC="30" # Intervalo de sincronização em minutos

# Telegram
TELEGRAM_BOT_TOKEN="TELEGRAM-TOKEN"
TELEGRAM_CHAT_ID="CHAT-ID"
TELEGRAM_PYTHON_TOPIC_ID=""
TELEGRAM_JAVA_TOPIC_ID=""
TELEGRAM_GOLANG_TOPIC_ID=""
TELEGRAM_FRONTEND_TOPIC_ID=""
TELEGRAM_BACKEND_TOPIC_ID=""

# Discord
DISCORD_BOT_ID="BOT-ID"
DISCORD_TOKEN="DISCORD-TOKEN"
DISCORD_GUILD_ID="GUILD-ID"
DISCORD_PYTHON_CHANNEL_ID=""
DISCORD_JAVA_CHANNEL_ID=""
DISCORD_GOLANG_CHANNEL_ID=""
DISCORD_FRONTEND_CHANNEL_ID=""
DISCORD_BACKEND_CHANNEL_ID=""

# UI
NEXT_PUBLIC_API_URL="https://vagas-api.henriquesebastiao.com"
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
| `INTERVAL_SYNC` | Intervalo em minutos entre cada ciclo de busca por novas vagas |

### Telegram

Para obter as variáveis do Telegram, crie um bot pelo [@BotFather](https://t.me/BotFather) e adicione-o ao seu grupo ou canal.

| Variável                     | Descrição                                                                          |
|------------------------------|------------------------------------------------------------------------------------|
| `TELEGRAM_BOT_TOKEN`         | Token de autenticação do bot, fornecido pelo @BotFather ao criar o bot             |
| `TELEGRAM_CHAT_ID`           | ID do grupo ou canal onde as vagas serão enviadas                                  |
| `TELEGRAM_PYTHON_TOPIC_ID`   | ID do tópico destinado a vagas de Python — deixe vazio para usar o canal principal |
| `TELEGRAM_JAVA_TOPIC_ID`     | ID do tópico destinado a vagas de Java                                             |
| `TELEGRAM_GOLANG_TOPIC_ID`   | ID do tópico destinado a vagas de Golang                                           |
| `TELEGRAM_FRONTEND_TOPIC_ID` | ID do tópico destinado a vagas de Frontend                                         |
| `TELEGRAM_BACKEND_TOPIC_ID`  | ID do tópico destinado a vagas de Backend genérico                                 |

### Discord

Para obter as variáveis do Discord, acesse o [Discord Developer Portal](https://discord.com/developers/applications), crie uma aplicação e adicione um bot. Ative o **Modo Desenvolvedor** no Discord em Configurações → Avançado para conseguir copiar IDs de servidores e canais.

| Variável                      | Descrição                                                                                           |
|-------------------------------|-----------------------------------------------------------------------------------------------------|
| `DISCORD_BOT_ID`              | ID da aplicação do bot, disponível no Developer Portal                                              |
| `DISCORD_TOKEN`               | Token de autenticação do bot — nunca compartilhe este valor                                         |
| `DISCORD_GUILD_ID`            | ID do servidor (guild) onde o bot está instalado — clique com botão direito no servidor para copiar |
| `DISCORD_PYTHON_CHANNEL_ID`   | ID do canal destinado a vagas de Python                                                             |
| `DISCORD_JAVA_CHANNEL_ID`     | ID do canal destinado a vagas de Java                                                               |
| `DISCORD_GOLANG_CHANNEL_ID`   | ID do canal destinado a vagas de Golang                                                             |
| `DISCORD_FRONTEND_CHANNEL_ID` | ID do canal destinado a vagas de Frontend                                                           |
| `DISCORD_BACKEND_CHANNEL_ID`  | ID do canal destinado a vagas de Backend genérico                                                   |

### Interface web

| Variável              | Descrição                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `NEXT_PUBLIC_API_URL` | URL pública da API consumida pela interface — em produção aponte para o domínio da sua API; localmente use `http://localhost:8000` |

## Executando

Após criar os arquivos `docker-compose.yml` e `.env`, agora você pode executar os container do sistema com o comando:

```shell
docker compose -f docker-compose.yml up -d
```