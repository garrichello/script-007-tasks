import pytest

from config import ServerConfig


@pytest.fixture
def test_dir():
    return "123"


@pytest.fixture
def test_file():
    return "poem.txt"


@pytest.fixture
def test_content():
    return b"sample data"


@pytest.fixture()
def config():
    return ServerConfig().config
