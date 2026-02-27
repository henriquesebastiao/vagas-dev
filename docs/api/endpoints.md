---
icon: lucide/milestone
---

# Endpoints

## Jobs

### Listar vagas

**GET** `http://localhost:8000/jobs`

Retorna uma lista de vagas de trabalho encontradas e registradas no banco de dados, com suporte a diversos filtros para refinar a busca.

#### Parâmetros de consulta

| Parâmetro        | Tipo   | Descrição                                 | Exemplo de valor |
|------------------|--------|-------------------------------------------|------------------|
| `keyword`        | string | Busca no título e descrição da vaga       | "python"         |
| `source`         | string | Filtra por fonte (`gupy`, etc.)           | "gupy"           |
| `location`       | string | Filtra por cidade ou estado               | "São Paulo"      |
| `workplace_type` | string | `remote`, `hybrid` ou `on-site`           | "remote"         |
| `for_pcd`        | bool   | Filtra vagas para pessoas com deficiência | true             |
| `limit`          | int    | Máximo de resultados (padrão: 50)         | 20               |
| `offset`         | int    | Paginação                                 | 0                |

#### Request

=== "Shell"

    ```bash
    curl -s \
      -H "accept: application/json" \
      "http://127.0.0.1:8000/jobs?keyword=python&limit=10"
    ```

=== ":fontawesome-regular-python: Python"

    ```python
    import requests
    
    url = 'http://127.0.0.1:8000/jobs'
    
    headers = {'accept': 'application/json'}
    params = {
        'keyword': 'python',
        'limit': 10,
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    print(response.text)

    ```

#### Resposta

```json
[
  {
    "id": 1,
    "external_id": "12345",
    "keyword": "python",
    "source": "gupy",
    "title": "Desenvolvedor Python",
    "company": "Tech Company",
    "location": "São Paulo",
    "url": "https://www.gupy.io/vagas/12345",
    "description": "Vaga para desenvolvedor Python com experiência em FastAPI.",
    "workplace_type": "remote",
    "published_at": "2024-05-30T10:00:00Z",
    "end_applications": "2024-06-30T23:59:59Z",
    "found_at": "2024-06-01T12:00:00Z",
    "notified": false,
    "for_pcd": false,
  },
  ...
]
```

#### Responses

| Código | Descrição                        |
|--------|----------------------------------|
| `200`  | Requisição bem-sucedida          |
| `422`  | Parâmetros de consulta inválidos |

### Disparar sincronização manual

**POST** `http://localhost:8000/jobs/sync/{source}`

Permite disparar uma sincronização manual de uma fonte específica, sem precisar esperar o próximo ciclo do scheduler. Isso é útil para testar a integração de uma nova fonte ou forçar uma atualização imediata.

#### Parâmetros de caminho

| Parâmetro | Tipo   | Descrição                         | Exemplo de valor |
|-----------|--------|-----------------------------------|------------------|
| `source`  | string | Fonte de vagas a ser sincronizada | "gupy"           |

#### Resposta

```json
{
  "message": "Sincronização da fonte 'gupy' iniciada com sucesso."
}
```

## Fontes

**GET** `http://localhost:8000/jobs/sources`

Retorna uma lista das fontes de vagas integradas ao sistema, juntamente com a quantidade de vagas registradas para cada fonte.

#### Resposta

```json
[
  {
    "source": "gupy",
    "job_count": 120
  },
  {
    "source": "linkedin",
    "job_count": 80
  },
  ...
]
```

## Health

**GET** `http://localhost:8000/health`

Retorna o status de saúde da aplicação, indicando se está funcionando corretamente.

#### Resposta

```json
{
  "status": "ok"
}
```