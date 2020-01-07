import logging
from os import path
from mimetypes import MimeTypes
from pathlib import Path

from error_page import ErrorPage
from file_cache import FileCache
from request import Request

from response import Response
from server_config import ServerConfig


class RequestHandler:
    __mime: MimeTypes = MimeTypes()
    __work_dir: Path = Path.cwd()
    __buff_size: int = 4096
    __config: ServerConfig = ServerConfig()
    __file_cache: FileCache = FileCache()
    __error_page: ErrorPage = ErrorPage()

    def handle_get(self, request):
        """GET request handler. Returns file to client
        :type request: Request
        """
        logging.info(f'Processing GET request {request.path}')
        path_to_file = self.__get_abs_path(request.path)
        file_descriptor = self.__file_cache.get_fd(path_to_file)
        if file_descriptor and path_to_file.is_file():
            response = Response(code=200)
            response.add_header("Content-Length", str(path.getsize(
                path_to_file)))
            file_type, charset = self.__mime.guess_type(path_to_file.as_uri())
            response.add_header("Content-Type", file_type)
            return self.__send_file_response(
                response=response, file_descriptor=file_descriptor), response
        else:
            bad_req_response = Response(code=404)
            return self.__send_general_response(
                bad_req_response), bad_req_response

    @staticmethod
    def __send_file_response(response, file_descriptor,
                             buffer_size=__buff_size):
        """Return response func with file loaded from specified path
        :type buffer_size: int
        :type file_descriptor: int
        :type response: Response
        """
        def result(client):
            request_data = response.get_bytes()
            client.sendall(request_data)
            with open(file_descriptor, 'rb', closefd=False) as output:
                while True:
                    data = output.read(buffer_size)
                    if not data:
                        break
                    client.sendall(data)
                output.seek(0)

        return result

    @staticmethod
    def __send_general_response(response):
        """Return simple response func
        :type response: Response
        """
        def result(client):
            data = response.get_bytes()
            client.sendall(data)

        return result

    def __get_abs_path(self, req_path):
        """Helper to get absolute path to requested file
        :type req_path: str
        """
        path_components = req_path.split("/")
        result = self.__work_dir / self.__config.www_dir
        for part in path_components:
            result = result / part
        return result
