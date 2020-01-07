from request import Request


class RequestParser:
    def parse(self, data):
        """Parse raw request and return Request object
        :type data: bytearray
        """
        headers_end = self.get_headers_end(data)
        body_raw = data[headers_end:]
        head_fields = data[:headers_end]\
            .decode('utf-8', errors='ignore')\
            .splitlines()
        headers = {}
        for field in head_fields[1:-1]:
            try:
                key, value = field.split(':', maxsplit=1)
                headers[key] = value.strip()
            except ValueError:
                continue
        return Request(head_fields[0], headers, body_raw)

    @staticmethod
    def get_headers_end(request_raw):
        """Get index of header block ending in the provided client request
        :type request_raw: bytearray
        """
        end_line = bytearray(b'\r\n\r\n')
        try:
            headers_end = request_raw.index(end_line) + len(end_line)
        except ValueError:
            raise ValueError('Failed to process headers. Aborting.')
        return headers_end

    def try_get_headers(self, data):
        """Retrieves Content-Length from partially received raw response.
        :type data: bytearray
        """
        try:
            request = self.parse(data)
            if request:
                return request
        except ValueError:
            return None
