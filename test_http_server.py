import unittest
from pathlib import Path
from socket import SOCK_STREAM, socket, AF_INET
from unittest import mock

from http_server import HttpServer


@unittest.mock.patch("http_server.socket")
def test_http_server_serve_file(mock_socket):
    """
    File serve test
    :param mock_socket: mocket socket object
    """
    request = \
        (f"GET /sample_file.txt HTTP/1.1\r\n"
         f"Host: localhost\r\n"
         f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)"
         f"Gecko/20100101 Firefox/69.0\r\n"
         f"Accept: text/html,application/xhtml+xml"
         f"application/xml;q=0.9,*/*;q=0.8\r\n"
         f"Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3\r\n"
         f"Accept-Encoding: gzip, deflate, br\r\n\r\n"
         )
    (Path.cwd() / "test_www_root").mkdir(parents=True, exist_ok=True)
    with open(Path.cwd() / "test_www_root" / "sample_file.txt", 'w'):
        pass
    mock_socket.return_value.bind.return_value = None
    mock_socket.return_value.listen.return_value = None
    mock_socket.return_value.setblocking.return_value = None
    mock_socket.return_value.settimeout.return_value = None

    mock_socket.return_value.recv.side_effect = [bytes(request, "utf-8")]
    mock_socket.return_value.sendall.side_effect = (
        lambda x: len(x)
    )
    mock_socket.return_value.send.side_effect = (
        lambda x: len(x)
    )
    mock_socket.return_value.fileno.return_value = 0
    mock_socket.return_value.close.return_value = None

    client_instance = mock_socket(AF_INET, SOCK_STREAM)

    mock_socket.return_value.accept.side_effect = [
        (client_instance, None), mock.DEFAULT]

    http_server = HttpServer("test_config.json")
    http_server.run()
    http_server.thread_pool.tasks.join()
    http_server.thread_pool.terminate_all_workers()

    response, *_ = client_instance.sendall.call_args[0]
    str_response = response.decode('utf-8', errors='ignore')
    header = str_response.partition('\r\n')[0]

    assert header == 'HTTP/1.1 200'


@unittest.mock.patch("http_server.socket")
def test_http_server_not_found(mock_socket):
    sample_req = \
        (f"GET /somefile.txt HTTP/1.1\r\n"
         f"Host: localhost\r\n"
         f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)"
         f"Gecko/20100101 Firefox/69.0\r\n"
         f"Accept: text/html,application/xhtml+xml"
         f"application/xml;q=0.9,*/*;q=0.8\r\n"
         f"Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3\r\n"
         f"Accept-Encoding: gzip, deflate, br\r\n\r\n"
         )
    mock_socket.return_value.bind.return_value = None
    mock_socket.return_value.listen.return_value = None
    mock_socket.return_value.setblocking.return_value = None
    mock_socket.return_value.settimeout.return_value = None
    mock_socket.return_value.recv.side_effect = [bytes(sample_req, "utf-8")]
    mock_socket.return_value.sendall.side_effect = (
        lambda x: len(x)
    )
    mock_socket.return_value.send.side_effect = (
        lambda x: len(x)
    )
    mock_socket.return_value.fileno.return_value = 0
    mock_socket.return_value.close.return_value = None
    client_instance = mock_socket(AF_INET, SOCK_STREAM)
    mock_socket.return_value.accept.side_effect = [
        (client_instance, None), mock.DEFAULT]

    http_server = HttpServer("test_config.json")
    http_server.run()
    http_server.thread_pool.tasks.join()
    http_server.thread_pool.terminate_all_workers()

    response, *_ = client_instance.sendall.call_args[0]
    str_response = response.decode('utf-8', errors='ignore')
    header = str_response.partition('\r\n')[0]

    assert header == 'HTTP/1.1 404'


if __name__ == "__main__":
    test_http_server_serve_file()
