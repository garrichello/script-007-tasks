import base64
import json

import requests

RESPONSE_KEYS = set(['status', 'data'])
DATA_KEYS = set(['name', 'create_date', 'edit_date', 'size', 'content'])


def test_get_file_data(config, test_dir, test_file, test_content):
    host = config["host"]
    port = config["port"]

    response = requests.post(f"http://{host}:{port}/change_dir", data=json.dumps({"path": f"{test_dir}"}))
    response = requests.post(
        f"http://{host}:{port}/files",
        data=json.dumps(
            {
                "filename": test_file,
                "content": base64.b64encode(test_content).decode("utf-8"),
            }
        ),
    )
    response = requests.get(f'http://{host}:{port}/files/{test_file}')

    resp_dict = json.loads(response.text)

    assert response.status_code == 200
    assert set(resp_dict.keys()) == RESPONSE_KEYS
    assert set(resp_dict['data'].keys()) == DATA_KEYS
    assert resp_dict['data']['content'] == base64.b64encode(test_content).decode("utf-8")
