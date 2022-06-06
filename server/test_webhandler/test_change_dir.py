import json
import os

import requests


def test_change_dir(config, test_dir):
    host = config["host"]
    port = config["port"]
    datadir = config["data_directory"]
    response = requests.post(f"http://{host}:{port}/change_dir", data=json.dumps({"path": f"{test_dir}"}))
    assert response.status_code == 200
    assert os.path.exists(os.path.join(datadir, f"{test_dir}"))
