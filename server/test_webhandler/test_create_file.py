import base64
import json
import os

import requests


def test_create_file(config, test_dir, test_file, test_content):
    host = config["host"]
    port = config["port"]
    datadir = config["data_directory"]
    target_file = os.path.join(datadir, test_dir, test_file)

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
    assert response.status_code == 201
    assert os.path.exists(target_file)

    with open(target_file, "rb") as f:
        data = f.read()
    assert data == test_content
