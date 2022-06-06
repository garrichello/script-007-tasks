import base64
import json

import requests

DATA_KEYS = set(["name", "create_date", "edit_date", "size"])


def test_get_files(config, test_dir, test_file, test_content):
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
    response = requests.get(f"http://{host}:{port}/files")

    assert response.status_code == 200

    resp_dict = json.loads(response.text)
    assert isinstance(resp_dict["data"], list)
    assert len(resp_dict["data"]) == 1
    file_info = resp_dict["data"][0]
    assert set(file_info.keys()) == DATA_KEYS
    assert test_file in file_info["name"]
