import datetime
import functools
import json

from aiohttp import BasicAuth, hdrs, web
from aiohttp.web import middleware
from sqlalchemy.orm import Session

import models
import utils
from db import UserDB


@middleware
class BasicAuthMiddleware(object):

    def __init__(self, force=True):
        self.force = force

    # noinspection PyMethodMayBeStatic
    @classmethod
    def parse_auth_header(cls, request):
        auth_header = request.headers.get(hdrs.AUTHORIZATION)
        if not auth_header:
            return None
        try:
            auth = BasicAuth.decode(auth_header=auth_header)
        except ValueError:  # pragma: no cover
            auth = None
        return auth

    @classmethod
    async def authenticate(cls, request):
        auth = cls.parse_auth_header(request)
        if auth:
            username, password = auth.login, auth.password
        else:
            username, password = "", ""
        if request.body_exists:
            body = await request.json()
        else:
            body = {}
        token = body.get('token', '')
        return (auth is not None or token) and await cls.check_credentials(
            username,
            password,
            token,
            request,
        )

    @classmethod
    async def check_credentials(cls, username, password, token, request):
        success = False

        if token:
            with Session(UserDB.engine) as session:
                sess = session.query(models.Sessions).filter_by(token=token).first()
                if sess:
                    now = datetime.datetime.now()
                    if sess.expires < now:
                        # Session expired
                        session.delete(sess)
                        session.flush()
                        token = ""
                    else:
                        # Update session expires
                        sess.expires = now + datetime.timedelta(days=utils.EXPIRATION_DAYS)
                        session.commit()
                        return True

        if not username or not password:
            return False

        # here, for example, you can search user in the database by passed `username` and `password`, etc.
        with Session(UserDB.engine) as session:
            instance = session.query(models.User).filter_by(name=username).first()
            if instance:
                _, db_salt, db_hash = instance.password_hash.split('$')
                try_pass_hash = utils.get_sha256_salted(password, db_salt)
                _, _, try_hash = try_pass_hash.split('$')

                success = try_hash == db_hash

        return success

    @classmethod
    def challenge(cls):
        return web.Response(
            body=b"",
            status=401,
            reason="UNAUTHORIZED",
            headers={
                hdrs.WWW_AUTHENTICATE: 'Basic realm=""',
                hdrs.CONTENT_TYPE: "text/html; charset=utf-8",
                hdrs.CONNECTION: "keep-alive",
            },
        )

    @classmethod
    def required(cls, handler):
        @functools.wraps(handler)
        async def wrapper(*args):
            request = None

            for arg in args:
                if isinstance(arg, web.View):  # pragma: no cover
                    request = arg.request
                if isinstance(arg, web.Request):
                    request = arg

            if request is None:  # pragma: no cover
                raise ValueError("Request argument not found for handler")

            if await cls.authenticate(request):
                return await handler(*args)
            else:
                return cls.challenge()

        return wrapper

    async def __call__(self, request, handler):
        if not self.force:
            return await handler(request)
        else:
            if await self.authenticate(request):
                return await handler(request)
            else:
                return self.challenge()
