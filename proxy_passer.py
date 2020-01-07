import logging
import socket
from select import select
import traceback

from server_config import ServerConfig


class ProxyPasser:
    __config = ServerConfig()

    def __init__(self, client_socket, target_socket=None):
        self.__client = client_socket
        if target_socket is not None:
            self.__target = target_socket
        else:
            self.__target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__target_host = self.__config.proxy_pass_host
        self.__target_port = self.__config.proxy_pass_port

    def run(self):
        """
        Init connection client <> target
        :return:
        """
        logging.info(f"Client <> Target opened")
        self.__client.setblocking(False)
        target_host_socket = self.__target
        target_host_socket.connect((self.__target_host, self.__target_port))
        target_host_socket.setblocking(False)

        client_data = bytearray()
        target_data = bytearray()
        while True:
            inputs = [self.__client, target_host_socket]
            outputs = []

            if len(client_data) > 0:
                outputs.append(self.__client)

            if len(target_data) > 0:
                outputs.append(target_host_socket)

            try:
                in_rdy, out_rdy, _ = select(inputs, outputs, [], 1.0)
            except Exception as e:
                logging.error(e)
                logging.error(traceback.format_exc())
                break

            data = bytearray()
            for connection in in_rdy:
                try:
                    data = connection.recv(4096)
                except Exception as e:
                    logging.error(e)

                if data is not None:
                    if len(data) > 0:
                        if connection == self.__client:
                            target_data += data
                        else:
                            client_data += data
                    else:
                        self.__close_conn(target_host_socket)
                        return

            for connection in out_rdy:
                if connection == self.__client and len(client_data) > 0:
                    bytes_written = self.__client.send(client_data)
                    if bytes_written > 0:
                        client_data = client_data[bytes_written:]
                elif connection == target_host_socket and len(target_data) > 0:
                    bytes_written = target_host_socket.send(target_data)
                    if bytes_written > 0:
                        target_data = target_data[bytes_written:]

    def __close_conn(self, target_host_socket):
        """
        Close target and client connections
        :param target_host_socket:
        :return:
        """
        self.__client.close()
        target_host_socket.close()
        logging.info("Client <> Target closed")
