from ctpview.workspace.ctp.infra.zmq_base import ZmqBase
from ctpview.workspace.common.file_util import jsonconfig

class ProxySender:
    def __init__(self):
        self.zmqBase = ''

    def set_config(self):
        pub_port = jsonconfig.get_config('common', 'PubAddPort')
        if self.zmqBase == '' or self.zmqBase.pub_port != pub_port:
            self.zmqBase = ZmqBase()

    def send_msg(self, topic, msg):
        if self.zmqBase == '':
            return
        topic_ = bytes(topic + " ", "utf-8")
        tmp = topic_ + msg
        self.zmqBase.zmq_pub.send(tmp)

proxysender = ProxySender()

if __name__ == "__main__":
    pass
