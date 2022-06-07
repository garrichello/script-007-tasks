"""Web handlers module"""
import base64
import copy
import json
import logging

from aiohttp import BasicAuth, hdrs, web

from auth import BasicAuthMiddleware as auth

from .FileService import FileService
from .UserService import UserService


class WebHandler:
    """aiohttp handler with coroutines."""

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._fs = FileService()
        self._us = UserService()
        self._headers = {"Access-Control-Allow-Origin": "*"}

    async def handle(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Basic coroutine for connection testing.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with status.
        """

        self._logger.debug(f"{request.path} was requested.")

        return web.json_response(data={"status": "success"}, headers=self._headers)

    async def change_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for changing working directory with files.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "path": "string. Directory path. Required",
            }.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        self._logger.debug(f"{request.path} was requested.")

        data = await request.json()
        new_path = data.get("path")
        message = "success"
        status = web.HTTPOk.status_code
        cur_path = self._fs.current_dir()
        try:
            cur_path = self._fs.change_dir(new_path, autocreate=True)
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
            self._logger.error(message)
        finally:
            return web.json_response(
                data={"status": message, "current path": cur_path}, status=status, headers=self._headers
            )

    async def current_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        self._logger.debug(f"{request.path} was requested.")

        message = "success"
        status = web.HTTPOk.status_code
        cur_path = ""
        try:
            cur_path = self._fs.current_dir()
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
            self._logger.error(message)
        finally:
            return web.json_response(
                data={"status": message, "current path": cur_path}, status=status, headers=self._headers
            )

    async def delete_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleteing working directory with files.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "path": "string. Directory path. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        self._logger.debug(f"{request.path} was requested.")

        data = await request.json()
        new_dir = data.get("path")
        message = "success"
        status = web.HTTPOk.status_code
        try:
            self._fs.delete_dir(new_dir, recursive=True)
        except FileNotFoundError as e:
            message = str(e)
            status = web.HTTPNotFound.status_code
            self._logger.error(message)
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
            self._logger.error(message)
        finally:
            return web.json_response(data={"status": message}, status=status, headers=self._headers)

    async def get_files(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting info about all files in working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """

        self._logger.debug(f"{request.path} was requested.")

        message = "success"
        status = web.HTTPOk.status_code
        files_meta = []
        cur_path = self._fs.current_dir()
        try:
            files_meta = self._fs.get_files()
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
            self._logger.error(message)
        finally:
            return web.json_response(
                data={"status": message, "data": files_meta, "current path": cur_path},
                status=status,
                dumps=lambda x: json.dumps(x, default=str),
                headers=self._headers,
            )

    async def get_file_data(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting full info about file in working directory.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        self._logger.debug(f"{request.path} was requested.")

        filename = request.match_info["filename"]

        message = "success"
        status = web.HTTPOk.status_code
        file_data = dict()
        try:
            file_data = self._fs.get_file_data(filename)
            file_data["content"] = base64.b64encode(file_data["content"]).decode("utf-8")
            # Use base64.b64decode(file_data['content']) to restore original bytes
        except RuntimeError as e:
            message = str(e)
            status = web.HTTPNotFound.status_code
            self._logger.error(message)
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
            self._logger.error(message)
        finally:
            return web.json_response(
                data={"status": message, "data": file_data},
                status=status,
                dumps=lambda x: json.dumps(x, default=str),
                headers=self._headers,
            )

    async def create_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for creating file.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                'filename': 'string. filename',
                'content': 'string. Content string. Optional',
            }.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        self._logger.debug(f"{request.path} was requested.")

        data = await request.json()
        filename = data.get("filename")
        # Check content. It should be base64 encoded.
        try:
            content = base64.b64decode(data.get("content"))
        except Exception as e:
            self._logger.error(f"Bad content for file {filename}")
            return web.json_response(
                data={"status": "bad content", "data": {}},
                status=web.HTTPBadRequest.status_code,
                headers=self._headers,
            )

        message = "success"
        status = web.HTTPCreated.status_code
        file_meta = dict()
        try:
            file_meta = self._fs.create_file(filename, content)
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
            self._logger.error(message)
        finally:
            # Add Location header
            new_headers = copy.copy(self._headers)
            new_headers["Location"] = request.raw_path + "/" + filename
            return web.json_response(
                data={"status": message, "data": file_meta},
                status=status,
                dumps=lambda x: json.dumps(x, default=str),
                headers=new_headers,
            )

    async def delete_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting file.

        Args:
            request (Request): aiohttp request, contains filename.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """
        self._logger.debug(f"{request.path} was requested.")

        filename = request.match_info["filename"]

        message = "success"
        status = web.HTTPOk.status_code
        try:
            self._fs.delete_file(filename)
        except RuntimeError as e:
            message = str(e)
            status = web.HTTPNotFound.status_code
            self._logger.error(message)
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
            self._logger.error(message)
        finally:
            return web.json_response(data={"status": message}, status=status, headers=self._headers)

    async def register(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Register a new user"""

        self._logger.debug(f"Registering a new user was requested.")

        message = ""
        status = web.HTTPOk.status_code
        if "Authorization" in request.headers:
            auth_info = request.headers["Authorization"].split()
            if len(auth_info) == 2:
                auth_val = auth_info[1]
                try:
                    username, password = base64.b64decode(auth_val).decode("utf-8").split(":")
                except:
                    message = "Bad 'Authorization' value!"
                    status = web.HTTPBadRequest.status_code
                    self._logger.error(message)
                    return web.json_response(data={"status": message}, status=status, headers=self._headers)
                if self._us.register(username=username, password=password):
                    message = "success"
                    status = web.HTTPOk.status_code
                    self._logger.debug(f"User '{username}' registered.")
                else:
                    message = f"User '{username}' already registered!"
                    status = web.HTTPBadRequest.status_code
                    self._logger.error(message)
            else:
                message = "Bad 'Authorization' value!"
                status = web.HTTPBadRequest.status_code
                self._logger.error(message)
        else:
            message = "No 'Authorization' HTTP-header!"
            status = web.HTTPBadRequest.status_code
            self._logger.error(message)
        return web.json_response(data={"status": message}, status=status, headers=self._headers)

    @auth.required
    async def login(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Login a new user"""

        self._logger.debug(f"User login was requested.")

        if request.body_exists:
            body = await request.json()
        else:
            body = {}
        token = body.get('token', '')

        if not token:
            # Get a new token.
            status = ""
            auth_header = request.headers.get(hdrs.AUTHORIZATION, "")
            if auth_header:
                auth = BasicAuth.decode(auth_header=auth_header)
                token = self._us.login(username=auth.login)
            
        if token:
            message = "success"
            status = web.HTTPOk.status_code
        else:
            message = "Authentication failed"
            status = web.HTTPUnauthorized.status_code
        
        return web.json_response(data={"status": message, "token": token}, status=status, headers=self._headers)
