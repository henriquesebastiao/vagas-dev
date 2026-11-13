---
icon: lucide/info
---

# Introdução

Esta seção apresenta a documentação da API REST do projeto, detalhando os endpoints disponíveis, os parâmetros de consulta e as respostas esperadas. A API foi projetada para fornecer acesso unificado às vagas de trabalho coletadas de múltiplas fontes, permitindo que os usuários filtrem e busquem por oportunidades de acordo com seus critérios específicos.

Você pode usar a API REST para consultar as vagas de trabalho, disparar sincronizações manuais e obter informações sobre as fontes de vagas integradas.

REST é um padrão de mercado para construção de APIs, baseado em recursos e utilizando os métodos HTTP (GET, POST, etc.) para realizar operações sobre esses recursos. A API deste projeto segue os princípios RESTful, garantindo uma estrutura clara e fácil de usar para os consumidores da API.

## Endereço

Os exemplos desta documentação usam `http://localhost:8000`, endereço padrão de uma instância local
(veja [Execute você mesmo](../do-it-yourself.md)). A instância pública fica em
`https://vagas-api.henriquesebastiao.com`.

A API não exige autenticação e aceita requisições de qualquer origem (CORS liberado).

## Documentação interativa

Toda instância da API gera a própria documentação a partir do código:

- **Swagger UI** na raiz (`/`), onde é possível testar os endpoints direto no navegador;
- **ReDoc** em `/redoc`.
