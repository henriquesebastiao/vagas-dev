---
icon: lucide/rocket
---

# Vagas de Trabalho para DEVs

Num cenário onde as vagas de trabalho em desenvolvimento de software estão cada vez mais dispersas entre diversas plataformas e sites, este projeto surge como uma solução para centralizar a busca por oportunidades na área de tecnologia. Através da coleta automática de vagas de múltiplas fontes, o sistema oferece uma API unificada que permite aos usuários consultar e filtrar as vagas de acordo com seus critérios específicos, facilitando o processo de encontrar a vaga ideal.

A ideia é facilitar a vida de quem está procurando emprego na área de tecnologia, permitindo filtrar por critérios como localização, tipo de trabalho (remoto, híbrido, presencial) e palavras-chave, entre outras funcionalidades.

!!! warning

    O sistema está na sua fase inicial de desenvolvimento. Novas fontes e notificações em mensageiros serão adicionadas em breve.
    Caso queira contribuir, sinta-se à vontade para abrir um PR ou issue com sugestões!

### Notificações

Além de coletar as vagas, o sistema também possui uma funcionalidade de notificações, que pode ser configurada para enviar alertas em mensageiros como Telegram sempre que novas vagas que correspondam a palavras-chave específicas forem encontradas. Isso permite que os usuários fiquem informados em tempo real sobre oportunidades relevantes, sem precisar acessar a API constantemente.

Para entrar para os grupos de notificações, basta clicar no link do mensageiro desejado:

- :simple-telegram: [Telegram](https://t.me/+5faW_wL4ybNhMjY5)
- :simple-discord: [Discord](https://discord.gg/MnnnvNQauf)

## Funcionalidades

- **Busca periódica automática** - scheduler configurável que roda em background e coleta novas vagas em intervalos definidos, sem intervenção manual
- **Notificações** - integração com Telegram para enviar alertas de novas vagas que correspondam a palavras-chave específicas
- **Sem duplicação de vagas** - vagas já registradas são ignoradas automaticamente, garantindo que o banco nunca acumule duplicatas, independente de quantas vezes o scheduler seja executado
- **API REST centralizada** - todas as vagas de todas as fontes acessíveis por um único endpoint, com filtros por palavra-chave, localização, tipo de trabalho e fonte
- **Filtros disponíveis** - busque vagas podendo filtrar pelas seguintes características:
  - **Palavra-chave** - busca no título e descrição da vaga
  - **Localização** - filtra por cidade ou estado (ex: "São Paulo", "Goiás")
  - **Tipo de trabalho** - filtra por `remote`, `hybrid` ou `on-site`
  - **Fonte** - filtra por plataforma de origem (ex: `gupy`, `linkedin`, etc.)
  - **Vagas para pessoas com deficiência** - filtro específico para vagas que aceitam candidaturas de pessoas com deficiência
  - **Paginação** - controle o número de resultados retornados e a partir de qual posição começar (limit/offset)
- **Trigger manual de sync** - é possível disparar uma sincronização sob demanda via endpoint, sem precisar esperar o próximo ciclo do scheduler
- **Arquitetura extensível** - adicionar uma nova fonte de vagas exige apenas criar um novo scraper herdando da classe base; toda a lógica de persistência e deduplicação já está pronta

## Fontes Suportadas

- [x] Gupy (via API)
- [ ] LinkedIn (via scraping)

## Tecnologias Utilizadas

- **FastAPI** - API REST assíncrona
- **SQLAlchemy** - ORM e acesso ao banco de dados
- **APScheduler** - agendamento de tarefas em background
- **httpx** - cliente HTTP assíncrono para os scrapers
- **Pydantic** - validação e serialização de dados