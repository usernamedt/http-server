import os
from functools import lru_cache

from server_config import ServerConfig


class FileCache:
    __config = ServerConfig()

    def __init__(self):
        self.__cache_max_size = self.__config.file_cache_size
        self.__cache_errors = self.__config.file_cache_errors
        self.__read_file_desc = self.__prepare_read_file_desc()

    def get_fd(self, path):
        """
        Get descriptor of specified file
        :param path: path to file
        :return: None or file descriptor
        """
        if self.__cache_errors:
            return self.__read_file_desc(path)
        else:
            try:
                return self.__read_file_desc(path)
            except IOError:
                return None

    def __prepare_read_file_desc(self):
        """
        Wraps a descriptor read function with an LRU cache
        :return: read descriptor func decorated with LRU cache
        """
        @lru_cache(maxsize=self.__cache_max_size)
        def result(filename):
            if self.__cache_errors:
                descriptor = None
                try:
                    descriptor = os.open(filename, os.O_RDONLY)
                except IOError:
                    pass
            else:
                descriptor = os.open(filename, os.O_RDONLY)
            return descriptor

        return result
