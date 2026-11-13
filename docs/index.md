---
icon: lucide/rocket
---

<h1 align="center">
  <a href="#">
    <picture>
      <img width="599" height="337" alt="Vagas Dev Banner" src="https://github.com/user-attachments/assets/958395bc-3201-4f6f-ba3b-0bf897624f48" />
    </picture>
  </a>
</h1>
<p align="center"><i>Buscador de vagas de trabalho para desenvolvedores no Brasil</i></p>

<div align="center">
  <img alt="Test" src="https://github.com/henriquesebastiao/vagas-dev/actions/workflows/test.yml/badge.svg">
  <img alt="Build" src="https://github.com/henriquesebastiao/vagas-dev/actions/workflows/deploy.yml/badge.svg">
  <img alt="GitHub Release" src="https://img.shields.io/github/v/release/henriquesebastiao/vagas-dev?color=blue">
  <img alt="Visitors" src="https://api.visitorbadge.io/api/visitors?path=henriquesebastiao%2Fvagas-dev&label=repository%20visits&countColor=%231182c3&style=flat">
</div>


As vagas de desenvolvimento de software estão espalhadas por várias plataformas. O Vagas Dev coleta
automaticamente as vagas dessas fontes, guarda tudo em um único banco e permite consultar e filtrar por cargo,
empresa, nível, modalidade (remoto, híbrido, presencial), local e vagas para pessoas com deficiência.

O sistema é formado por uma **API REST**, que busca vagas novas periodicamente em segundo plano, e por uma
**interface web** para navegar pelas vagas e abrir a candidatura no site de origem. Os dois serviços são
distribuídos como imagens Docker e podem ser hospedados por qualquer pessoa: veja [Execute você mesmo](do-it-yourself.md).
Também existe uma instância pública:

- [Interface web](https://vagas.henriquesebastiao.com)
- [API REST](https://vagas-api.henriquesebastiao.com)

!!! warning

    O projeto está em fase inicial de desenvolvimento. Caso queira contribuir, abra uma issue ou PR no
    [repositório](https://github.com/henriquesebastiao/vagas-dev).

## Funcionalidades

- **Busca periódica automática**: a API coleta vagas novas assim que inicia e depois a cada `INTERVAL_SYNC` minutos, sem intervenção manual.
- **Sem vagas duplicadas**: vagas já registradas (mesmo ID externo e mesma fonte) são ignoradas, não importa quantas vezes a coleta rode.
- **Nível da vaga deduzido do título**: estágio, júnior, pleno ou sênior, quando o título indica.
- **API REST centralizada**: todas as vagas de todas as fontes em um único endpoint, com filtros por texto no título, empresa, fonte, local, modalidade, nível e vagas PCD, além de paginação. Veja os [endpoints](api/endpoints.md).
- **Sincronização manual**: dispare uma coleta sob demanda por endpoint, sem esperar o próximo ciclo.
- **Interface web**: lista de vagas com filtros, painel de detalhes, tema claro e escuro e layout para celular.
- **Arquitetura extensível**: uma nova fonte exige apenas um novo scraper; persistência e deduplicação já estão prontas.

## Fontes suportadas

| Fonte    | Método                      | Status                                                               |
|----------|-----------------------------|----------------------------------------------------------------------|
| Gupy     | API pública                 | Indisponível: o endpoint usado pelo scraper passou a responder 404   |
| LinkedIn | Scraping da página de busca | Disponível (vagas remotas; sem empresa e descrição)                  |

## Tecnologias utilizadas

- **FastAPI**: API REST assíncrona
- **SQLAlchemy (async) + Alembic**: ORM, acesso ao banco e migrations
- **PostgreSQL**: banco de dados
- **APScheduler**: agendamento das coletas
- **httpx + BeautifulSoup**: requisições HTTP e scraping
- **Pydantic**: validação e serialização de dados
- **Next.js + React**: interface web (exportada como site estático)
- **Docker**: execução da API, da interface e do banco
