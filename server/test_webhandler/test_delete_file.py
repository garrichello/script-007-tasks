import base64
import json
import os

import requests


def test_delete_file(config, test_dir, test_file, test_content):
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
    response = requests.delete(f"http://{host}:{port}/files/{test_file}")

    assert response.status_code == 200
    assert not os.path.exists(target_file)
