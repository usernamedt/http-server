from request import Request
from request_handler import RequestHandler


def test_handle_get_notfound():
    """
    Handle not found request
    :return:
    """
    request_handler = RequestHandler()
    request = Request(req_line="GET /test1.txt HTTP/1.1",
                      headers={"User-Agent": "TestPython",
                               "Connection": "keep-alive"},
                      body=bytearray())
    _, response = request_handler.handle_get(request)

    assert response.code == 404
