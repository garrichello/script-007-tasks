import datetime
import logging
import uuid

from sqlalchemy.orm import Session

import models
import utils
from db import UserDB


class UserService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def register(self, username: str, password: str) -> bool:
        """Register a new user in the DB"""
        with Session(UserDB.engine) as session:
            instance = session.query(models.User).filter_by(name=username).first()
            if instance:
                return False

            salt = uuid.uuid4().hex
            password_hash = utils.get_sha256_salted(data=password, salt=salt)
            user = models.User(name=username, password_hash=password_hash, last_login=None)

            session.add(user)

            session.commit()

        return True

    def login(self, username: str) -> str:
        "Login user"
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(days=utils.EXPIRATION_DAYS)
        token = str(uuid.uuid4())

        with Session(UserDB.engine) as session:
            user = session.query(models.User).filter_by(name=username).first()
            if user:
                user.last_login = now
                new_sess = models.Sessions(user_id=user.id, token=token, expires=expires)
                session.add(new_sess)
                session.commit()
            else:
                token = ""
        if token:
            self._logger.debug(f"User {username} logged in!")
        else:
            self._logger.error(f"User {username} not found")

        return token
