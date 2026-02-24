# url = 'https://portal.api.gupy.io/api/job'
#
# params = {
#     'name': 'desenvolvedor',  # parâmetro obrigatório
#     'limit': 10,
#     'offset': 0,
# }
#
# headers = {'User-Agent': 'Mozilla/5.0'}
# response = httpx.get(url, params=params, headers=headers)
# data = response.json()
#
# # pprint(data)  # veja a estrutura primeiro
#
# with open('desenvolvedor.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(data, indent=4, ensure_ascii=False))

from pprint import pprint

import requests

TOKEN = 'SEU_TOKEN'
url = 'https://api.telegram.org/bot8655498459:AAGzyrghYbLIX716DdmAcnSOXJuCw69SvSY/sendMessage'

payload = {
    'chat_id': -1003863195365,
    'message_thread_id': 3,
    'text': 'Mensagem no tópico!',
}

response = requests.post(url, json=payload)
pprint(response.json())
