"""Web handlers module"""
import base64
import json
import os

from aiohttp import web

from .FileService import FileService


class WebHandler:
    """aiohttp handler with coroutines."""

    def __init__(self) -> None:
        self._fs = FileService()

    async def handle(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Basic coroutine for connection testing.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with status.
        """

        return web.json_response(data={"status": "success"})

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
        finally:
            return web.json_response(data={"status": message, "current path": cur_path}, status=status)

    async def current_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        message = "success"
        status = web.HTTPOk.status_code
        cur_path = ""
        try:
            cur_path = self._fs.current_dir()
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
        finally:
            return web.json_response(data={"status": message, "current path": cur_path}, status=status)

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

        data = await request.json()
        new_dir = data.get("path")
        message = "success"
        status = web.HTTPOk.status_code
        try:
            self._fs.delete_dir(new_dir, recursive=True)
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
        finally:
            return web.json_response(data={"status": message}, status=status)

    async def get_files(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting info about all files in working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """

        message = "success"
        status = web.HTTPOk.status_code
        files_meta = []
        cur_path = self._fs.current_dir()
        try:
            files_meta = self._fs.get_files()
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
        finally:
            return web.json_response(
                data={"status": message, "data": files_meta, "current path": cur_path},
                status=status,
                dumps=lambda x: json.dumps(x, default=str),
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

        filename = request.match_info["filename"]

        message = "success"
        status = web.HTTPOk.status_code
        file_data = dict()
        try:
            file_data = self._fs.get_file_data(filename)
            # file_data['content'] = base64.b64encode(file_data['content']).decode('utf-8')
            # Use base64.b64decode(file_data['content']) to restore original bytes
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
        finally:
            return web.json_response(
                data={"status": message, "data": file_data},
                status=status,
                dumps=lambda x: json.dumps(x, default=str),
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

        data = await request.json()
        filename = data.get("filename")
        content = bytes(data.get("content"), encoding="utf-8")

        message = "success"
        status = web.HTTPOk.status_code
        file_meta = dict()
        try:
            file_meta = self._fs.create_file(filename, content)
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
        finally:
            return web.json_response(
                data={"status": message, "data": file_meta}, status=status, dumps=lambda x: json.dumps(x, default=str)
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

        filename = request.match_info["filename"]

        message = "success"
        status = web.HTTPOk.status_code
        try:
            self._fs.delete_file(filename)
        except Exception as e:
            message = str(e)
            status = web.HTTPBadRequest.status_code
        finally:
            return web.json_response(data={"status": message}, status=status)
