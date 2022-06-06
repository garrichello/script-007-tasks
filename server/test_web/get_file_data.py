import json

import requests

response = requests.get('http://127.0.0.1:8080/files/1.txt')
print(f'code: {response.status_code}')
# print(f'body: {response.text}')
pretty_response = json.dumps(json.loads(response.text))
print(f'body: {pretty_response}')
