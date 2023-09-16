import socket

import zmq


class ZmqBase:

    def __init__(self):
        self.context = zmq.Context()
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)


zmqbase = ZmqBase()
