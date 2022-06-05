import psycopg2
from utils.Config import config


class UserService:

    def __init__(self):
        self.conn = psycopg2.connect(
            host=config.database.host,
            port=config.database.port,
            dbname=config.database.name,
            user=config.database.user,
            password=config.database.password,
        )


def register(username: str, password: str) -> None:
    pass


def login(username: str, password: str) -> None:
    pass


def check_auth(token: str) -> bool:
    pass


def logout(token: str) -> None:
    pass
