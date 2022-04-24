from .components import ComponentBase
from .regmodule import regmodule

import socket

class Socket(regmodule):

    port = 5000
    host = 'localhost'

    __server = None

    def __init__(self, port=5000, host='localhost'):
        self.port = port
        self.host = host
        self.init_server()

    def server(self):
        return self.__server

    def init_server(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind((self.host, self.port))
        self.__server.settimeout(0.2)
        self.__server.listen(5)


class Server(ComponentBase):

    __socket = Socket()

    def __init__(self):
        super().__init__()
        self.is_alive = True

    def update(self):
        if self.is_alive:
            try:
                client, address = self.__socket.server().accept()
            except socket.timeout:
                return
            except Exception as e:
                print(e)
                return
            
            print(f'Connection from {address}')
            # do handshake protocol

            # hand it off to the handler class
        else:
            self.__socket.server().close()

    def turn_off(self):
        self.is_alive = False



