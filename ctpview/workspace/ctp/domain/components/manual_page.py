import datetime
import os
import time

import streamlit as st

from ctpview.workspace.common.protobuf import ctpview_market_pb2 as cmp
from ctpview.workspace.common.protobuf import ctpview_trader_pb2 as ctp
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender


class manual():

    def __init__(self):
        pass

    def update(self):
        mode_str = ['Login Control', 'Check Strategy Alive', 'Block Quotation', 'Bug Injection', 'Simulate MarketState', 'Profiler Control']
        manual_mode = st.selectbox('Manual mode', mode_str, key='manual_mode')

        if manual_mode == 'Login Control':
            self.login_control()
        elif manual_mode == 'Check Strategy Alive':
            self.check_alive()
        elif manual_mode == 'Block Quotation':
            self.block_quotation()
        elif manual_mode == 'Bug Injection':
            self.bug_injection()
        elif manual_mode == 'Simulate MarketState':
            self.simulate_market_state()
        elif manual_mode == 'Profiler Control':
            self.profiler_control()

    def login_control(self):
        contain = st.container()
        col1, col2, col3 = contain.columns(3)

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

            topic = "ctpview_trader.CheckStrategyAlive"
            msg = ctp.message()
            mlc = msg.check_alive
            mlc.check = "yes"
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

    def block_quotation(self):
        contain = st.container()
        col1, col2 = contain.columns(2)

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

    def bug_injection(self):
        contain = st.container()
        col1, col2 = contain.columns(2)

        if col1.button('market: doublefree'):
            topic = "ctpview_market.BugInjection"
            msg = cmp.message()
            mbi = msg.bug_injection
            mbi.type = cmp.BugInjection.InjectionType.double_free
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col2.button('trader: doublefree'):
            topic = "ctpview_trader.BugInjection"
            msg = ctp.message()
            mbi = msg.bug_injection
            mbi.type = ctp.BugInjection.InjectionType.double_free
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

    def get_newest_date(self):
        if datetime.date.today().weekday() in [0, 1, 2, 3, 4]:
            if datetime.datetime.now().hour <= 20:
                select_date = st.date_input('select data', datetime.date.today())
            else:
                if datetime.date.today().weekday() == 4:
                    select_date = st.date_input('select data', datetime.date.today() + datetime.timedelta(days=3))
                else:
                    select_date = st.date_input('select data', datetime.date.today() + datetime.timedelta(days=1))
        elif datetime.date.today().weekday() == 5:
            select_date = st.date_input('select data', datetime.date.today() + datetime.timedelta(days=2))
        elif datetime.date.today().weekday() == 6:
            select_date = st.date_input('select data', datetime.date.today() + datetime.timedelta(days=1))

        datestr = '%04d%02d%02d' % (select_date.year, select_date.month, select_date.day)

        return datestr

    def simulate_market_state(self):
        market_state = st.selectbox('market state', ['day_open', 'day_close', 'night_open', 'night_close'], key='market_state')
        datestr = self.get_newest_date()
        # target = st.selectbox('target', ['strategy', 'manage'], key='target')

        if st.button('send'):
            topic = "ctpview_market.SimulateMarketState"
            msg = cmp.message()
            msms = msg.simulate_market_state
            if market_state == 'day_open':
                msms.market_state = cmp.SimulateMarketState.MarketState.day_open
            elif market_state == 'day_close':
                msms.market_state = cmp.SimulateMarketState.MarketState.day_close
            elif market_state == 'night_open':
                msms.market_state = cmp.SimulateMarketState.MarketState.night_open
            elif market_state == 'night_close':
                msms.market_state = cmp.SimulateMarketState.MarketState.night_close
            else:
                msms.market_state = cmp.SimulateMarketState.MarketState.reserve

            msms.date = datestr
            msms.target = ''
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

    def network_disconnect(self):
        if st.button('network disconnect'):
            command = 'sudo tc qdisc add dev eth0 root netem loss 100%'
            os.system(command)
            time.sleep(130)
            command = 'sudo tc qdisc del dev eth0 root'
            os.system(command)

    def profiler_control(self):
        contain = st.container()
        col1, col2 = contain.columns(2)

        if col1.button('market start write'):
            topic = "ctpview_market.ProfilerControl"
            msg = cmp.message()
            mlc = msg.profiler_control
            mlc.profiler_action = cmp.ProfilerControl.ProfilerAction.start_write
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col2.button('market stop write'):
            topic = "ctpview_market.ProfilerControl"
            msg = cmp.message()
            mlc = msg.profiler_control
            mlc.profiler_action = cmp.ProfilerControl.ProfilerAction.stop_write
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col1.button('trader start write'):
            topic = "ctpview_trader.ProfilerControl"
            msg = ctp.message()
            mlc = msg.profiler_control
            mlc.profiler_action = ctp.ProfilerControl.ProfilerAction.start_write
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col2.button('trader stop write'):
            topic = "ctpview_trader.ProfilerControl"
            msg = ctp.message()
            mlc = msg.profiler_control
            mlc.profiler_action = ctp.ProfilerControl.ProfilerAction.stop_write
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)


manual_page = manual()
