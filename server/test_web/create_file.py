import json

import requests

response = requests.post('http://127.0.0.1:8080/files', data=json.dumps({
    'filename': 'poem.txt',
    'content': 'New file content\r\nIn two lines!',
}))
print(f'code: {response.status_code}')
print(f'body: {response.text}')
