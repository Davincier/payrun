__author__ = 'Joe'

import socket
from .rpc_exception import RpcException
from .rpc import RpcParameter, Rpc


class RpcServer(object):

    user = None

    def __init__(self, hostname, port):
        self.host = hostname
        self.port = port
        self.is_open = False
        self.socket = None

    def open(self):
        my_hostname = socket.gethostname()
        my_ip = socket.gethostbyname(my_hostname)
        self.socket = None
        try:
            vista_info = socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM)
            af, socktype, proto, canonname, sa = vista_info[0]
            self.socket = socket.socket(af, socktype, proto)
            self.socket.connect(sa)
        except:
            if self.socket:
                self.socket.close()
                self.socket = None
            raise
        params = [
            RpcParameter(RpcParameter.LITERAL, my_ip),
            RpcParameter(RpcParameter.LITERAL, my_hostname)
        ]
        rpc = Rpc.create('HELLO', params)
        try:
            response = self.execute(rpc)
        except Exception as e:
            raise RpcException('On response: ' + e.args[0])
        if response != 'accept':
            self.close()
            raise RpcException('Connection not accepted: ' + response)
        self.is_open = True

    def execute(self, rpc):
        response = f.read()
        f.close()
        return response.decode()

    def _send(self, rpc):
        try:
            self.socket.send(bytes(rpc, 'utf-8'))
        except socket.error as e:
            raise RpcException('On send: ' + e.args[0])

    def _recv(self):
        # Header first...
        buf = self.socket.recv(256)
        if buf is None:
            raise RpcException('Error receiving: no response')
        buf = buf.decode('utf-8')

        # SECURITY error?
        if buf[0] != "\x00":
            buf = buf[1:ord(buf[0])]
            raise RpcException('VistA SECURITY error: ' + buf)

        # APPLICATION error?
        if buf[1] != "\x00":
            buf = buf[1:len(buf)]
            raise RpcException('VistA APPLICATION error: ' + buf)

        buf = buf[2:len(buf)]

        # Is there more response?
        end_idx = buf.find(Rpc.EOT)

        # If not, trim the EOT off the end
        if end_idx != -1:
            buf = buf[0:-1]

        # Sometimes there's a trailing '\0'
        if buf[-1] == "\x00":
            buf = buf[0:-1]

        # Here's the response so far...
        response = buf

        # Add to it if there's more...
        while end_idx == -1:
            buf = self.socket.recv(256)
            if buf is None:
                raise RpcException('Error receiving: no EOT and no MORE')
            buf = buf.decode('utf-8')

            # Is there more response?
            end_idx = buf.find(Rpc.EOT)

            # If not, trim the EOT off the end
            if end_idx != -1:
                buf = buf[0:-1]

            # Sometimes there's a trailing '\0'
            if buf[-1] == "\x00":
                buf = buf[0:-1]

            response += buf

        # Was there an error?
        if response.startswith('M  ERROR'):
            raise RpcException(response)

        return response

    def close(self):
        if self.is_open:
            rpc = Rpc.create('BYE')
            self.execute(rpc)
            self.socket.close()
            self.is_open = False
