import zmq
import socket

class ZmqBase:
    def __init__(self):
        context = zmq.Context()

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        self.pub_port = 'tcp://%s:5556'%(ip)
        self.zmq_pub = context.socket(zmq.PUB)
        self.zmq_pub.connect(self.pub_port)

if __name__ == "__main__":
    pass
    # zmq1 = ZmqBase()
    # zmq1.zmq_connect()

zmqbase = ZmqBase()
