import zmq

from ctpview.workspace.ctp.infra.zmq_base import zmqbase


class DirectSender:

    def __init__(self):
        self.zmq_pub = zmqbase.context.socket(zmq.PUB)
        self.zmq_pub.connect('tcp://%s:8101' % (zmqbase.ip))

    def send_msg(self, topic, msg):
        topic_ = bytes(topic + " ", "utf-8")
        tmp = topic_ + msg
        self.zmq_pub.send(tmp)


directsender = DirectSender()
