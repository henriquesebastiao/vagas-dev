from pprint import pprint

import httpx

url = 'https://portal.api.gupy.io/api/v1/jobs?perPage=10&page=1'

headers = {'accept': 'application/json'}

response = httpx.get(url, headers=headers)

pprint(response.text)
