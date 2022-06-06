import json

import requests


def test_root():
    response = requests.get('http://127.0.0.1:8080/')
    assert response.status_code == 200
    assert json.loads(response.text) == {"status": "success"}
