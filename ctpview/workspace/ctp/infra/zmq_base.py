import zmq
from ctpview.workspace.common.file_util import jsonconfig

class ZmqBase:
    def __init__(self):
        context = zmq.Context()

        self.pub_port = jsonconfig.get_config('common', 'PubAddPort')
        self.zmq_pub = context.socket(zmq.PUB)
        self.zmq_pub.connect(self.pub_port)

if __name__ == "__main__":
    pass
    # zmq1 = ZmqBase()
    # zmq1.zmq_connect()
