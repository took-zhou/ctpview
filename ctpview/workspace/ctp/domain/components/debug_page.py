import streamlit as st

from ctpview.workspace.common.protobuf import ctpview_market_pb2 as cmp
from ctpview.workspace.common.protobuf import ctpview_trader_pb2 as ctp
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender

class debug():
    def __init__(self):
        pass

    def update(self):
        mode_str = ['Login Control', 'Check Strategy Alive', 'Block Quotation']
        debug_mode = st.selectbox('Debug mode', mode_str, key='debug_mode')

        if debug_mode == 'Login Control':
            self.login_control()
        elif debug_mode == 'Check Strategy Alive':
            self.check_alive()
        elif debug_mode == 'Block Quotation':
            self.block_quotation()

    def login_control(self):
        contain = st.container()
        col1,col2,col3 = contain.columns(3)

        if col1.button('market login'):
            topic = "ctpview_market.LoginControl"
            msg = cmp.message()
            mlc = msg.login_control
            mlc.command = cmp.LoginControl.Command.login
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col2.button('market logout'):
            topic = "ctpview_market.LoginControl"
            msg = cmp.message()
            mlc = msg.login_control
            mlc.command = cmp.LoginControl.Command.logout
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col3.button('market reserve'):
            topic = "ctpview_market.LoginControl"
            msg = cmp.message()
            mlc = msg.login_control
            mlc.command = cmp.LoginControl.Command.reserve
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col1.button('trader login'):
            topic = "ctpview_trader.LoginControl"
            msg = ctp.message()
            mlc = msg.login_control
            mlc.command = ctp.LoginControl.Command.login
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col2.button('trader logout'):
            topic = "ctpview_trader.LoginControl"
            msg = ctp.message()
            mlc = msg.login_control
            mlc.command = ctp.LoginControl.Command.logout
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col3.button('trader reserve'):
            topic = "ctpview_trader.LoginControl"
            msg = ctp.message()
            mlc = msg.login_control
            mlc.command = ctp.LoginControl.Command.reserve
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

    def check_alive(self):
        if st.button('check'):
            topic = "ctpview_market.CheckStrategyAlive"
            msg = cmp.message()
            mlc = msg.check_alive
            mlc.check = "yes"
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

    def block_quotation(self):
        contain = st.container()
        col1,col2 = contain.columns(2)

        if col1.button('block'):
            topic = "ctpview_market.BlockControl"
            msg = cmp.message()
            mlc = msg.block_control
            mlc.command = cmp.BlockControl.Command.block
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col2.button('unblock'):
            topic = "ctpview_market.BlockControl"
            msg = cmp.message()
            mlc = msg.block_control
            mlc.command = cmp.BlockControl.Command.unblock
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

debug_page = debug()
