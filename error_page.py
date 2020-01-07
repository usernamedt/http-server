import logging
from functools import lru_cache
from pathlib import Path

from server_config import ServerConfig


class ErrorPage:
    __errors = [
        {
            "code": 400,
            "short_desc": "Bad Request",
            "long_desc": "Syntax of the request not understood by the server."
        },
        {
            "code": 401,
            "short_desc": "Not Authorized",
            "long_desc": "Request requires user authentication"
        },
        {
            "code": 402,
            "short_desc": "Payment Required",
            "long_desc": "Reserved for future use."
        },
        {
            "code": 403,
            "short_desc": "Forbidden",
            "long_desc": "Server refuses to fulfill the request."
        },
        {
            "code": 404,
            "short_desc": "Not Found",
            "long_desc": "Document or file requested by the client was not"
                         "found."
        },
        {
            "code": 405,
            "short_desc": "Method Not Allowed",
            "long_desc": "Method specified in the Request-Line was not allowed"
                         "for the specified resource."
        },
        {
            "code": 406,
            "short_desc": "Not Acceptable",
            "long_desc": "Resource requested generates response entities that"
                         "has content characteristics not specified in"
                         "he accept headers."
        },
        {
            "code": 407,
            "short_desc": "Proxy Authentication Required",
            "long_desc": "Request requires the authentication with the proxy."
        },
        {
            "code": 408,
            "short_desc": "Request Timeout",
            "long_desc": "Client fails to send a request in the time allowed"
                         "by the server."
        },
        {
            "code": 409,
            "short_desc": "Conflict",
            "long_desc": "Request was unsuccessful due to a conflict in the"
                         "state of the resource."
        },
        {
            "code": 410,
            "short_desc": "Gone",
            "long_desc": "Resource requested is no longer available with no"
                         "forwarding address"
        },
        {
            "code": 411,
            "short_desc": "Length Required",
            "long_desc": "Server doesn’t accept the request without a valid"
                         "Content-Length header field."
        },
        {
            "code": 412,
            "short_desc": "Precondition Failed",
            "long_desc": "Precondition specified in the Request-Header field"
                         "returns false."
        },
        {
            "code": 413,
            "short_desc": "Request Entity Too Large",
            "long_desc": "Request unsuccessful as the request entity is larger"
                         "than that allowed by the server"
        },
        {
            "code": 414,
            "short_desc": "Request URL Too Long",
            "long_desc": "Request unsuccessful as the URL specified is longer"
                         "than the one, the server is willing to process."
        },
        {
            "code": 415,
            "short_desc": "Unsupported Media Type",
            "long_desc": "Request unsuccessful as the entity of the request is"
                         "in a format not supported by the requested resource"
        },
        {
            "code": 416,
            "short_desc": "Requested Range Not Satisfiable",
            "long_desc": "Request included a Range request-header field"
                         "without any range-specifier value"
        },
        {
            "code": 417,
            "short_desc": "Expectation Failed",
            "long_desc": "Expectation given in the Expect request-header"
                         "was not fulfilled by the server."
        },
        {
            "code": 422,
            "short_desc": "Unprocessable Entity",
            "long_desc": "Request well-formed but unable to process because"
                         "of semantic errors"
        },
        {
            "code": 423,
            "short_desc": "Locked",
            "long_desc": "Resource accessed was locked"
        },
        {
            "code": 424,
            "short_desc": "Failed Dependency",
            "long_desc": "Request failed because of the failure of a"
                         "previous request"
        },
        {
            "code": 426,
            "short_desc": "Upgrade Required",
            "long_desc": "Client should switch to Transport Layer Security"
        },
        {
            "code": 500,
            "short_desc": "Internal Server Error",
            "long_desc": "Request unsuccessful because of an unexpected"
                         "condition encountered by the server."
        },
        {
            "code": 501,
            "short_desc": "Not Implemented",
            "long_desc": "Request unsuccessful as the server could not "
                         "support the functionality needed to fulfill"
                         " the request."
        },
        {
            "code": 502,
            "short_desc": "Bad Gateway",
            "long_desc": "Server received an invalid response from the"
                         "upstream server while trying to fulfill the request."
        },
        {
            "code": 503,
            "short_desc": "Service Unavailable",
            "long_desc": "Request unsuccessful to the server being down"
                         "or overloaded."
        },
        {
            "code": 504,
            "short_desc": "Gateway Timeout",
            "long_desc": "Upstream server failed to send a request in the"
                         "time allowed by the server."
        },
        {
            "code": 505,
            "short_desc": "HTTP Version Not Supported",
            "long_desc": "Server does not support the HTTP version specified"
                         "in the request."
        }
    ]
    __instance = None
    __config = ServerConfig()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.__instance = super(ErrorPage, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        page_loc = Path.cwd() / self.__config.error_page_loc
        if page_loc.is_file():
            with open(page_loc, 'rb') as output:
                self.error_page = output.read().decode("utf-8")
        else:
            logging.error("Error page was not found. Using default.")
            self.error_page = "{{CODE}} {{SHORT_DESC}} {{LONG_DESC}}"

    @lru_cache()
    def get_page_content(self, code):
        """
        Get error page content as string
        :param code: error code
        :return:
        """
        error = next((e for e in self.__errors if e.get("code") == code), None)
        result = self.error_page.replace("{{CODE}}", str(code))
        result = result.replace("{{SHORT_DESC}}", error.get("short_desc"))
        return result.replace("{{LONG_DESC}}", error.get("long_desc"))
