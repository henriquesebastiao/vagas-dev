import httpx

url = "https://portal.api.gupy.io/api/job"

params = {
    "name": "desenvolvedor",  # parâmetro obrigatório
    "limit": 10,
    "offset": 0
}

headers = {"User-Agent": "Mozilla/5.0"}
response = httpx.get(url, params=params, headers=headers)
data = response.json()

print(data)  # veja a estrutura primeiro

for vaga in data["data"]:
    print(vaga["name"])
    print(vaga["companyName"])
    print(vaga["city"])
    print("---")