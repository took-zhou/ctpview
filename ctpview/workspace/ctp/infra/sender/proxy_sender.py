from ctpview.workspace.ctp.infra.zmq_base import zmqbase

class ProxySender:
    def __init__(self):
        pass

    def send_msg(self, topic, msg):
        topic_ = bytes(topic + " ", "utf-8")
        tmp = topic_ + msg
        zmqbase.zmq_pub.send(tmp)

proxysender = ProxySender()

if __name__ == "__main__":
    pass
