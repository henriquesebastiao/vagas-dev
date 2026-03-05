<h1 align="center">
  <a href="https://github.com/henriquesebastiao/vagas-dev" target="_blank" rel="noopener noreferrer">
    <picture>
      <img width="599" height="337" alt="Vagas Dev Banner" src="https://github.com/user-attachments/assets/958395bc-3201-4f6f-ba3b-0bf897624f48" />
    </picture>
  </a>
</h1>
<p align="center"><i>Sistema para busca de vagas de trabalho para desenvolvedores no Brasil</i></p>

<div align="center">
  
  [![Test](https://github.com/henriquesebastiao/vagas-dev/actions/workflows/test.yml/badge.svg)](https://github.com/henriquesebastiao/vagas-dev/actions/workflows/test.yml)
  [![Build](https://github.com/henriquesebastiao/vagas-dev/actions/workflows/deploy.yml/badge.svg)](https://github.com/henriquesebastiao/vagas-dev/actions/workflows/deploy.yml)
  [![GitHub Release](https://img.shields.io/github/v/release/henriquesebastiao/vagas-dev?color=blue)](https://github.com/henriquesebastiao/vagas-dev/releases)
  [![Visitors](https://api.visitorbadge.io/api/visitors?path=henriquesebastiao%2Fvagas-dev&label=repository%20visits&countColor=%231182c3&style=flat)](https://github.com/henriquesebastiao/vagas-dev)

</div>

## ✨ O que e porquê?

Um sistema de busca de vagas de emprego para desenvolvedores e notificações via apps de mensagens.

Num cenário onde as vagas de trabalho em desenvolvimento de software estão cada vez mais dispersas entre diversas plataformas e sites, este projeto surge como uma solução para centralizar a busca por oportunidades na área de tecnologia. Através da coleta automática de vagas de múltiplas fontes, o sistema oferece uma API unificada que permite aos usuários consultar e filtrar as vagas de acordo com seus critérios específicos, facilitando o processo de encontrar a vaga ideal.

A ideia é facilitar a vida de quem está procurando emprego na área de tecnologia, permitindo filtrar por critérios como localização, tipo de trabalho (remoto, híbrido, presencial) e palavras-chave, entre outras funcionalidades.

Esse sistema é composto por uma API REST que busca por novas vagas de trabalho periódicamente em fontes como [Gupy](https://portal.gupy.io/) e [LinkedIn](https://www.linkedin.com) em background e notifica sobre as novas vagas encontradas via apps de mensagens como Telegram e Discord.

Os links de acesso ao sistema estão listados abaixo:

- [Documentação](https://henriquesebastiao.github.io/vagas-dev/)
- [Interface Web](https://vagas.henriquesebastiao.com/)
- [API](https://vagas-api.henriquesebastiao.com/)

> [!IMPORTANT]
> O sistema está na sua fase inicial de desenvolvimento. Novas fontes e notificações em mensageiros podem adicionadas em breve.
> Caso queira contribuir com desenvolvimento, relatar bugs ou sugerir melhorias, sinta-se à vontade para abrir um PR ou issue com sua contribuição!

## 🔔 Notificações

Para receber alerta das vagas encontradas pelo sistema faça parte do grupo de alerta no seu app mensageiro de preferência entre os listados abaixo:

> O link de cada um é o link de convite para o grupo ou servidor.

- [Telegram](https://t.me/+5faW_wL4ybNhMjY5)
- [Discord](https://discord.gg/MnnnvNQauf)

## Funcionalidades

- **Busca periódica automática** — scheduler configurável que roda em background e coleta novas vagas em intervalos definidos, sem intervenção manual
- **Notificações** — integração com Telegram e Discord para enviar alerta de novas vagas que correspondam a palavras-chave específicas
- **Sem duplicação de vagas** — vagas já registradas são ignoradas automaticamente, garantindo que o banco nunca acumule duplicatas, independente de quantas vezes o scheduler seja executado
- **API REST centralizada** — todas as vagas de todas as fontes acessíveis por um único endpoint, com filtros por palavra-chave, localização, tipo de trabalho e fonte
- **Filtros disponíveis** - busque vagas podendo filtrar pelas seguintes características:
  - **Palavra-chave** — busca no título e descrição da vaga
  - **Localização** — filtra por cidade ou estado (ex: "São Paulo", "Goiás")
  - **Tipo de trabalho** — filtra por `remote`, `hybrid` ou `on-site`
  - **Fonte** — filtra por plataforma de origem (ex: `gupy`, `linkedin`, etc.)
  - **Vagas para pessoas com deficiência** — filtro específico para vagas que aceitam candidaturas de pessoas com deficiência
  - **Paginação** — controle o número de resultados retornados e a partir de qual posição começar (limit/offset)
- **Trigger manual de sync** — é possível disparar uma sincronização sob demanda via endpoint, sem precisar esperar o próximo ciclo do scheduler
- **Arquitetura extensível** — adicionar uma nova fonte de vagas exige apenas criar um novo scraper herdando da classe base; toda a lógica de persistência e deduplicação já está pronta
- **Interface Web** - interface web desenvolvida com [Next.js](https://nextjs.org/) para visualização e busca das vagas encontradas pelo sistema.

## Fontes Suportadas

| Fonte    | Método  | Status       |
|----------|---------|--------------|
| Gupy     | API     | ✅ Disponível |
| LinkedIn | Scraper | ✅ Disponível |

> Novas fontes podem ser adicionadas criando um scraper que implementa `BaseJobScraper`.

## Endpoints

| Método | Rota                  | Descrição                                    |
|--------|-----------------------|----------------------------------------------|
| `GET`  | `/jobs`               | Lista vagas com filtros opcionais            |
| `POST` | `/jobs/sync/{source}` | Dispara sync manual de uma fonte             |
| `GET`  | `/jobs/sources`       | Lista fontes e quantidade de vagas por fonte |
| `GET`  | `/health`             | Health check da aplicação                    |

### Filtros disponíveis em `GET /jobs`

| Parâmetro        | Tipo   | Descrição                           |
|------------------|--------|-------------------------------------|
| `keyword`        | string | Busca no título e descrição da vaga |
| `source`         | string | Filtra por fonte (`gupy`, etc.)     |
| `location`       | string | Filtra por cidade ou estado         |
| `workplace_type` | string | `remote`, `hybrid` ou `on-site`     |
| `limit`          | int    | Máximo de resultados (padrão: 50)   |
| `offset`         | int    | Paginação                           |


## Contribuindo

### Como Adicionar um Novo Scraper

Caso queira adicionar uma nova fonte de vagas, siga os passos abaixo para adicionar um novo scraper:

1. Crie um arquivo em `scrapers/minha_fonte.py`
2. Herde de `BaseJobScraper` e defina `source_name`
3. Implemente `fetch_jobs()` retornando uma lista de dicts no formato do model `Job`
4. Registre um job no `scheduler.py` com o intervalo desejado

```python
from app.scrapers.base import BaseJobScraper


class MinhaFonteScraper(BaseJobScraper):
    source_name = "minha_fonte"

    async def fetch_jobs(self) -> list[dict]:
        # sua lógica aqui
        ...
```

## Tecnologias Utilizadas

- **FastAPI** — API REST assíncrona
- **SQLAlchemy (async)** — ORM e acesso ao banco de dados
- **APScheduler** — agendamento de tarefas em background
- **httpx** — cliente HTTP assíncrono para os scrapers
- **Pydantic** — validação e serialização de dados
