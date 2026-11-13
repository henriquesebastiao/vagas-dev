---
icon: lucide/map
---

# Roadmap

Esta página resume o que já foi feito no projeto e o que está planejado.

## Concluído

- [x] **Scrapers para múltiplas fontes**
    - [x] Gupy (via API)
    - [x] LinkedIn (via scraping)
- [x] **Busca periódica automática**: coleta ao iniciar e depois em intervalos configuráveis
- [x] **Sincronização manual** por endpoint
- [x] **Sem vagas duplicadas**
- [x] **API REST centralizada** com filtros por título, empresa, fonte, local, modalidade, nível e vagas PCD
- [x] **Nível de experiência** (estágio, júnior, pleno, sênior) deduzido do título da vaga
- [x] **Interface web** com filtros, detalhes da vaga e layout para celular
- [x] **Imagens Docker** da API e da interface publicadas a cada release

## Próximos passos

- [ ] **Restaurar a coleta da Gupy**: o endpoint público usado pelo scraper passou a responder 404 e precisa ser migrado para a API atual da Gupy
- [ ] **Mais dados nas vagas do LinkedIn**: coletar empresa e descrição, hoje ausentes
- [ ] **Novas fontes**: outras plataformas populares de vagas, como Indeed e Glassdoor

## Sugestões

Caso tenha alguma sugestão de funcionalidade ou fonte de vagas, abra uma issue ou PR no [repositório](https://github.com/henriquesebastiao/vagas-dev). O projeto é open source e toda contribuição é bem-vinda.
