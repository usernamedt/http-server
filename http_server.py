import logging
from socket import SOCK_STREAM, socket, AF_INET, timeout

from proxy_passer import ProxyPasser
from request_handler import RequestHandler
from request_parser import RequestParser
from response import Response
from server_config import ServerConfig
from thread_pool import ThreadPool


class HttpServer:
    __request_parser: RequestParser = RequestParser()
    __request_processor: RequestHandler = RequestHandler()

    def __init__(self, config_name="config.json"):
        self.__config = ServerConfig(config_name)
        logging.basicConfig(filename=self.__config.log_file,
                            level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.thread_pool = ThreadPool()

    def run(self):
        """Binds, listens, processing HTTP requests on socket"""
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.__config.host, self.__config.port))
        s.listen(self.__config.queue_size)
        logging.info(f'Launched at {self.__config.port}')
        while True:
            try:
                client_connection, _ = s.accept()
            except Exception as e:
                logging.info(e)
                s.close()
                break
            client_connection.settimeout(self.__config.max_req_time)
            self.thread_pool.add_task(self.__route_request, client_connection)

    def __route_request(self, client):
        """Routes request to handler if exists, then closes the connection"""
        if self.__config.proxy_pass_mode:
            __proxy_passer = ProxyPasser(client)
            __proxy_passer.run()
            return
        while True:
            try:
                raw_request = self.__read_from_socket(client)
            except timeout:
                logging.info("Caught timeout waiting for socket connection")
                break
            except ReadSocketError:
                bad_response = Response(code=400)
                client.sendall(bad_response.get_bytes())
                client.close()
                logging.info(f'Failed to read request. Returned response'
                             f' {bad_response.code}')
                return
            req = self.__request_parser.parse(raw_request)
            if req.method == "GET":
                response_func, response = self.__request_processor.handle_get(
                    req)
                logging.info(f'Received GET {req.path}, '
                             f'returned response {response.code}')
                response_func(client=client)
            if "Connection" not in req.headers \
                    or req.headers["Connection"].lower() != "keep-alive":
                break
        client.close()

    def __read_from_socket(self, client):
        """Reads request data from socket. If request method or protocol
        are not supported, rejects it"""
        result = bytearray()
        req = None
        head_len = 0
        total_len = None
        while not total_len or head_len < total_len:
            chunk = client.recv(8192)
            if not chunk:
                break
            result += chunk
            head_len += len(chunk)
            if not req:
                req = self.__request_parser.try_get_headers(result)
                if not req:
                    continue
            if req.method not in self.__config.supported_methods or \
                    req.proto not in self.__config.supported_protos:
                logging.info(f'Received unsupported request {req}')
                raise ReadSocketError("Request of this type not supported")
            total_len = req.headers.get("Content-Length")
            if not total_len:
                break
        return result


class ReadSocketError(Exception):
    """Error indicating there was some issues reading from the socket."""
    pass
