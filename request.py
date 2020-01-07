class Request:
    def __init__(self, req_line, headers, body):
        """
        HTTP request data class
        :type body: bytearray
        :type headers: dict
        :type req_line: str
        """
        self.method, self.path, self.proto = req_line.split()
        self.headers = headers
        self.body = body
