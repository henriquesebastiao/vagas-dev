---
icon: lucide/map
---

# Roadmap

Este documento apresenta o roadmap de desenvolvimento do projeto, detalhando as funcionalidades planejadas, as fontes de vagas a serem integradas e as tecnologias que serão utilizadas. O objetivo é fornecer uma visão clara do progresso atual e das próximas etapas para alcançar a visão completa do projeto.

## Funcionalidades Planejadas

- [x] **Scrappers para múltiplas fontes** - além da Gupy, planeja-se integrar outras plataformas populares de vagas, como LinkedIn, Indeed, Glassdoor, etc., utilizando scraping ou APIs oficiais quando disponíveis;
    - [x] Gupy (via API)
    - [x] LinkedIn (via scraping)
- [x] **Busca periódica automática** - scheduler configurável que roda em background e coleta novas vagas em intervalos definidos, sem intervenção manual;
- [x] **Trigger manual de sync** - é possível disparar uma sincronização sob
- [x] **Notificações** - integração com mensageiros para enviar alertas de novas vagas que correspondam a palavras-chave específicas:
    - [x] Telegram
    - [x] Discord
- [x] **Sem duplicação de vagas** - vagas já registradas são ignoradas automaticamente, garantindo que o banco nunca acumule duplicatas, independente de quantas vezes o scheduler seja executado;
- [x] **API REST centralizada** - todas as vagas de todas as fontes acessíveis por um único endpoint, com filtros por palavra-chave, localização, tipo de trabalho e fonte;
- [ ] **Filtros avançados** - além dos filtros básicos, planeja-se adicionar opções como:
    - Nível de experiência (júnior, pleno, sênior)

## Sugestões

Casa tenha alguma sugestão de funcionalidade ou fonte de vaga que gostaria de ver integrada, sinta-se à vontade para abrir um issue ou PR no [repositório](https://github.com/henriquesebastiao/vagas-dev) com a sua ideia! O projeto é open source e toda contribuição é bem-vinda.
