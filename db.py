"""User DB manipulation functions."""

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

import models


class UserDB:
    """Database access class"""

    engine = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(UserDB, cls).__new__(cls)
        return cls.instance

    def __init__(self, db_user: str = "", db_pw: str = "", db_host: str = "", db_port: int = 0, db_name: str = ""):
        if db_host:
            UserDB.engine = create_engine(
                f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}", echo=False, future=True
            )

    def init_db(self):
        """Initializes empty users DB"""

        if database_exists(UserDB.engine.url):
            drop_database(UserDB.engine.url)
        create_database(UserDB.engine.url)

        models.Base.metadata.create_all(self.engine)
