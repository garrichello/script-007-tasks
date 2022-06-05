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
        self.cur = self.conn.cursor()
        self.cur.autocommit = True

        query = """
create table if not exists users (
  id uuid primary key,
  name varchar(50) not null,
  password char(64) not null, -- 32 bytes of sha256 in hex form (multiple by 2)
  registration timestamp,
  last_login timestamp
);

create table if not exists sessions (
  id uuid primary key,
  user_id uuid references users(id),
  expires timestamp
);
"""

    def __del__(self) -> None:
        self.cur.close()
        self.conn.close()


def register(username: str, password: str) -> None:
    query = "insert into users (id, name, registration, lost_login) values (?, ?, ?, ?)"



def login(username: str, password: str) -> None:
    pass


def check_auth(token: str) -> bool:
    pass


def logout(token: str) -> None:
    pass
