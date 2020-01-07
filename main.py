from http_server import HttpServer


def main():
    """Init and run HttpServer"""
    server = HttpServer("config.json")
    server.run()


if __name__ == '__main__':
    main()
