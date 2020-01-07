import os

from error_page import ErrorPage
from server_config import ServerConfig


class Response:
    __config = ServerConfig()
    __error_page = ErrorPage()

    def __init__(self, code, def_headers=None):
        """
        HTTP response data class
        :type def_headers: dict
        :type code: int
        """
        if def_headers is None:
            def_headers = self.__config.default_headers.copy()
        self.code = code
        if self.__is_error(code):
            self.body = self.__error_page.get_page_content(code)
        else:
            self.body = ""
        self.headers = def_headers
        if len(self.body) != 0:
            body_len = len(bytes(self.body, "utf-8"))
            self.headers["Content-Length"] = body_len

    def add_header(self, name, value):
        """Adds a header for response
        :type value: str
        :type name: str
        """
        self.headers[name] = value

    def get_headers_string(self):
        """Return headers as a string"""
        response = ""
        for row in self.headers:
            response += f"{row}: {self.headers[row]}\r\n"
        return response

    def get_bytes(self):
        """Returns response as byte array"""
        return bytearray(
            f"HTTP/1.1 {self.code}\r\n"
            f"{self.get_headers_string()}\r\n"
            f"{self.body}", "utf-8")

    @staticmethod
    def __is_error(code):
        return int(code / 100) == 4 or int(code / 100) == 5
