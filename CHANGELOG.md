## [0.2.1](https://github.com/henriquesebastiao/vagas-dev/releases/0.2.1) - 2026-03-05

### Funcionalidade

- Adicionando descrição ao frontend e mais filtros


## [0.1.1](https://github.com/henriquesebastiao/vagas-dev/releases/0.1.1) - 2026-03-04

### Funcionalidade

- Alterando tempo de intervalo entre buscas de vagas para 60 minutos


## [0.1.0](https://github.com/henriquesebastiao/vagas-dev/releases/0.1.0) - 2026-03-04

### Core

- Refatorando código e melhorias na busca de vagas


## [0.1.0-beta.5](https://github.com/henriquesebastiao/vagas-dev/releases/0.1.0-beta.5) - 2026-03-04

### Funcionalidade

- Buscando vagas mais acertivamente no linkedin usando filtros ([#16](https://github.com/henriquesebastiao/vagas-dev/issues/16))


## [0.1.0-beta.4](https://github.com/henriquesebastiao/vagas-dev/releases/0.1.0-beta.4) - 2026-03-04

### Correção de Bug

- Corrigindo versão das imagens docker


## [0.1.0-beta.3](https://github.com/henriquesebastiao/vagas-dev/releases/0.1.0-beta.3) - 2026-03-04

### Core

- Atualizando dependências da API


## [0.1.0-beta.2](https://github.com/henriquesebastiao/vagas-dev/releases/0.1.0-beta.2) - 2026-03-04

### Correção de Bug

- Corrigindo arquivo de CI de build das imagens Docker


## [0.1.0-beta](https://github.com/henriquesebastiao/vagas-dev/releases/0.1.0-beta) - 2026-03-03

### Funcionalidade

- Listando vagas para PCDs ([#1](https://github.com/henriquesebastiao/vagas-dev/issues/1))
- Configurando aplicação em Docker ([#3](https://github.com/henriquesebastiao/vagas-dev/issues/3))
- Implementando alerta de vagas via Discord ([#4](https://github.com/henriquesebastiao/vagas-dev/issues/4))
- Implementando logging ([#6](https://github.com/henriquesebastiao/vagas-dev/issues/6))
- Filtrando vagas por senioridade ([#8](https://github.com/henriquesebastiao/vagas-dev/issues/8))
- Implementando busca de vagas no LinkedIn ([#14](https://github.com/henriquesebastiao/vagas-dev/issues/14))
- Implementando frontend ([#15](https://github.com/henriquesebastiao/vagas-dev/issues/15))
- Ajustando parâmetros de busca para Enum
- Implementando rotas da API
- Implementando wrapper do Telegram
- Marcando se a notificação foi enviada por tipo de mensageiro
- Ordenando resultados da API do Gupy por mais recentes

### Correção de Bug

- Formatando mensagem a ser enviada via Telegram para não extrapolar o limite de 4096 caracteres por mensagem

### Documentação

- Documentando endpoints da API ([#5](https://github.com/henriquesebastiao/vagas-dev/issues/5))
- Adicionando roadmap à documentação ([#7](https://github.com/henriquesebastiao/vagas-dev/issues/7))
- Desativando exibição do path na documentação
- Gerando changelogs com towncrier
- Iniciando documentação

### Core

- Aplica migrações automaticamente com alembic
- Configurando banco de dados
- Implementando boas práticas com clientes http
- Implementando pre-commit

### Atualizações

- fastapi 0.129.0 -> 0.131.0
- fastapi 0.131.0 -> 0.132.0
- fastapi 0.133.0 -> 0.134.0
- fastapi 0.134.0 -> 0.135.0
- ruff 0.15.2 -> 0.15.3
- ruff 0.15.3 -> 0.15.4
