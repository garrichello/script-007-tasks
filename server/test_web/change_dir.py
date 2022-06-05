import json

import requests

response = requests.post('http://127.0.0.1:8080/change_dir', data=json.dumps({'path': '123'}))
print(f'code: {response.status_code}')
print(f'body: {response.text}')
