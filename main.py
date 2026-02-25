import json

import httpx

url = 'https://employability-portal.gupy.io/api/v1/jobs/companies?jobName=python&limit=1000&sortBy=company&sortOrder=asc'
headers = {'accept': 'application/json'}

response = httpx.get(url, headers=headers)

# Converte a resposta para dict/list Python
data = response.json()

# Salva no arquivo JSON
with open('gupy_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Arquivo salvo com sucesso!')
