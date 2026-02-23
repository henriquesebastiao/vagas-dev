# from pprint import pprint
import json

import httpx

url = 'https://portal.api.gupy.io/api/job'

params = {
    'name': 'desenvolvedor',  # parâmetro obrigatório
    'limit': 10,
    'offset': 0,
}

headers = {'User-Agent': 'Mozilla/5.0'}
response = httpx.get(url, params=params, headers=headers)
data = response.json()

# pprint(data)  # veja a estrutura primeiro

with open('desenvolvedor.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
