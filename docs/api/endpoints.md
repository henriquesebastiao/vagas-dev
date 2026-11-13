---
icon: lucide/milestone
---

# Endpoints

Os exemplos usam `http://localhost:8000`; troque pelo endereço da sua instância.

## Vagas

### Listar vagas

**GET** `/jobs`

Retorna as vagas registradas no banco, da encontrada mais recentemente para a mais antiga. Todos os filtros são
opcionais e podem ser combinados.

#### Parâmetros de consulta

| Parâmetro        | Tipo   | Descrição                                                              | Exemplo       |
|------------------|--------|------------------------------------------------------------------------|---------------|
| `keyword`        | string | Texto buscado no título da vaga, sem diferenciar maiúsculas (máx. 100) | `python`      |
| `company`        | string | Texto buscado no nome da empresa (máx. 100)                            | `nubank`      |
| `source`         | string | Fonte da vaga: `gupy` ou `linkedin`                                    | `linkedin`    |
| `location`       | string | Texto buscado no local (cidade, estado ou país)                        | `São Paulo`   |
| `workplace_type` | string | Modalidade: `remote`, `hybrid` ou `on-site`                            | `remote`      |
| `level`          | string | Nível: `estagio`, `junior`, `pleno`, `senior` ou `trainee`             | `pleno`       |
| `for_pcd`        | bool   | `true` para apenas vagas para pessoas com deficiência                  | `true`        |
| `limit`          | int    | Máximo de resultados (padrão `50`, máximo `200`)                       | `20`          |
| `offset`         | int    | Quantidade de vagas a pular, para paginação (padrão `0`)               | `40`          |

Para percorrer todas as vagas, aumente `offset` de `limit` em `limit` até receber uma lista com menos itens que `limit`.

#### Requisição

=== "Shell"

    ```bash
    curl -s \
      -H "accept: application/json" \
      "http://localhost:8000/jobs?keyword=python&level=pleno&limit=10"
    ```

=== ":fontawesome-brands-python: Python"

    ```python
    import httpx

    response = httpx.get(
        'http://localhost:8000/jobs',
        params={'keyword': 'python', 'level': 'pleno', 'limit': 10},
    )

    for job in response.json():
        print(job['title'], job['url'])
    ```

#### Resposta

```json
[
  {
    "id": 1,
    "external_id": "12345",
    "keyword": "python",
    "source": "gupy",
    "title": "Desenvolvedor Python Pleno",
    "company": "Tech Company",
    "location": "São Paulo, SP, Brasil",
    "url": "https://techcompany.gupy.io/jobs/12345",
    "description": "Vaga para desenvolvedor Python com experiência em FastAPI.",
    "workplace_type": "remote",
    "published_at": "2026-11-10T10:00:00",
    "end_applications": "2026-12-10T23:59:59",
    "found_at": "2026-11-11T12:00:00",
    "for_pcd": false,
    "level": "pleno"
  }
]
```

| Campo              | Descrição                                                                    |
|--------------------|------------------------------------------------------------------------------|
| `id`               | ID da vaga no banco do Vagas Dev                                             |
| `external_id`      | ID da vaga na fonte de origem                                                |
| `keyword`          | Termo de busca que encontrou a vaga                                          |
| `source`           | Fonte da vaga (`gupy` ou `linkedin`)                                         |
| `title`            | Título da vaga                                                               |
| `company`          | Empresa contratante, ou `null` quando a fonte não informa (LinkedIn)         |
| `location`         | Local da vaga                                                                |
| `url`              | Página da vaga na fonte de origem, onde é feita a candidatura                |
| `description`      | Descrição da vaga, ou `null` quando a fonte não informa (LinkedIn)           |
| `workplace_type`   | `remote`, `hybrid`, `on-site` ou `null`                                      |
| `published_at`     | Data de publicação na fonte, ou `null`                                       |
| `end_applications` | Prazo para candidatura, ou `null`                                            |
| `found_at`         | Data em que a vaga foi encontrada pelo Vagas Dev                             |
| `for_pcd`          | `true` se a vaga é destinada a pessoas com deficiência                       |
| `level`            | Nível deduzido do título (`estagio`, `junior`, `pleno`, `senior`, `trainee`) ou `null` |

#### Códigos de resposta

| Código | Descrição                                                                 |
|--------|---------------------------------------------------------------------------|
| `200`  | Requisição bem-sucedida (a lista pode vir vazia)                          |
| `422`  | Parâmetro inválido, como `level` fora da lista ou `limit` acima de `200`  |

### Disparar sincronização manual

**POST** `/jobs/sync/{source}`

Dispara uma coleta de vagas da fonte informada sem esperar o próximo ciclo automático. A coleta roda em segundo
plano: a resposta chega na hora e as vagas novas aparecem em `GET /jobs` assim que a coleta termina.

#### Parâmetros de caminho

| Parâmetro | Tipo   | Descrição                               | Exemplo    |
|-----------|--------|-----------------------------------------|------------|
| `source`  | string | Fonte a coletar: `gupy` ou `linkedin`   | `linkedin` |

#### Requisição

```bash
curl -s -X POST "http://localhost:8000/jobs/sync/linkedin"
```

#### Resposta

```json
{
  "message": "Sync de 'linkedin' iniciado em background."
}
```

#### Códigos de resposta

| Código | Descrição                    |
|--------|------------------------------|
| `202`  | Coleta iniciada              |
| `422`  | Fonte inexistente            |

### Listar fontes

**GET** `/jobs/sources`

Retorna as fontes que já têm vagas registradas e a quantidade de vagas de cada uma.

#### Resposta

```json
[
  {
    "source": "gupy",
    "count": 120
  },
  {
    "source": "linkedin",
    "count": 342
  }
]
```

## Health

**GET** `/health`

Indica se a API está no ar. É o endpoint usado pelo healthcheck da imagem Docker.

#### Resposta

```json
{
  "status": "ok"
}
```
