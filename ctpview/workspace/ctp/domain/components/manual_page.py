import datetime
import json
import os
import sqlite3
import time

import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig
from ctpview.workspace.common.protobuf import ctpview_market_pb2 as cmp
from ctpview.workspace.common.protobuf import ctpview_trader_pb2 as ctp
from ctpview.workspace.ctp.domain.components.control_page import control
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender


class manual():

    def __init__(self):
        pass

    def update(self):
        mode_str = [
            'Login Control', 'Check Strategy Alive', 'Block Quotation', 'Bug Injection', 'Simulate MarketState', 'Profiler Control',
            'Backtest Control', 'Virtual Account Set'
        ]
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
        elif manual_mode == 'Backtest Control':
            self.backtest_control()
        elif manual_mode == 'Virtual Account Set':
            self.virtual_account_set()

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
            st.info('market login send ok')

        if col2.button('market logout'):
            topic = "ctpview_market.LoginControl"
            msg = cmp.message()
            mlc = msg.login_control
            mlc.command = cmp.LoginControl.Command.logout
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)
            st.info('market logout send ok')

        if col3.button('market reserve'):
            topic = "ctpview_market.LoginControl"
            msg = cmp.message()
            mlc = msg.login_control
            mlc.command = cmp.LoginControl.Command.reserve
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)
            st.info('market reserve send ok')

        if col1.button('trader login'):
            topic = "ctpview_trader.LoginControl"
            msg = ctp.message()
            mlc = msg.login_control
            mlc.command = ctp.LoginControl.Command.login
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)
            st.info('trader login send ok')

        if col2.button('trader logout'):
            topic = "ctpview_trader.LoginControl"
            msg = ctp.message()
            mlc = msg.login_control
            mlc.command = ctp.LoginControl.Command.logout
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)
            st.info('trader logout send ok')

        if col3.button('trader reserve'):
            topic = "ctpview_trader.LoginControl"
            msg = ctp.message()
            mlc = msg.login_control
            mlc.command = ctp.LoginControl.Command.reserve
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)
            st.info('trader reserve send ok')

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
        subscribe_list = []
        try:
            username = jsonconfig.get_config('market', 'User')[0]
            control_db_path = '%s/%s/control.db' % (jsonconfig.get_config('market', 'ControlParaFilePath'), username)
            conn = sqlite3.connect(control_db_path)
            try:
                command = 'select ins from publish_control;'
                subscribe_list = [item[0] for item in conn.execute(command).fetchall()]
            except:
                # error_msg = traceback.format_exc()
                # print(error_msg)
                pass
            conn.close()
        except:
            pass

        select_ins_list = st.multiselect('select ins', subscribe_list)

        contain = st.container()
        col1, col2 = contain.columns(2)

        if col1.button('block'):
            topic = "ctpview_market.BlockControl"
            msg = cmp.message()
            mlc = msg.block_control
            mlc.command = cmp.BlockControl.Command.block
            for item in select_ins_list:
                mlc.instrument.append(item)
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        if col2.button('unblock'):
            topic = "ctpview_market.BlockControl"
            msg = cmp.message()
            mlc = msg.block_control
            mlc.command = cmp.BlockControl.Command.unblock
            for item in select_ins_list:
                mlc.instrument.append(item)
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

    def bug_injection(self):
        contain = st.container()
        col1, col2 = contain.columns(2)

        if col1.button('market doublefree'):
            topic = "ctpview_market.BugInjection"
            msg = cmp.message()
            mbi = msg.bug_injection
            mbi.type = cmp.BugInjection.InjectionType.double_free
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)
            st.info('market doublefree send ok')

        if col2.button('trader doublefree'):
            topic = "ctpview_trader.BugInjection"
            msg = ctp.message()
            mbi = msg.bug_injection
            mbi.type = ctp.BugInjection.InjectionType.double_free
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)
            st.info('trader doublefree send ok')

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

    def backtest_control(self):
        control_para = []
        usernames = jsonconfig.get_config('market', 'User')
        if len(usernames) > 0:
            temp_dir = '%s/%s/' % (jsonconfig.get_config('market', 'ControlParaFilePath'), usernames[0])
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            control_db_path = '%s/backtest.db' % temp_dir
            conn = sqlite3.connect(control_db_path)
            try:
                command = 'select begin, end, now, speed, source, indication from backtest_control;'
                control_para = conn.execute(command).fetchall()[0]
            except:
                command = "create table if not exists backtest_control(begin TEXT, end TEXT, now TEXT, speed INT, source INT, indication INT);"
                conn.execute(command)
                command = "insert into backtest_control(begin, end, now, speed, source, indication) select '2015-01-01 09:00:00', '2020-12-31 15:00:00', '', 1, 0, 0 where not exists (select * from backtest_control);"
                conn.execute(command)
                conn.commit()
            conn.close()

            if len(control_para) > 0:
                updated_para = self.hand_backtest_operation(control_para)
                if updated_para[0] == control_para[0] and updated_para[1] == control_para[1] and updated_para[2] == control_para[
                        3] and updated_para[3] == control_para[4] and updated_para[4] == control_para[5]:
                    pass
                else:
                    topic = "ctpview_market.BackTestControl"
                    msg = cmp.message()
                    mbc = msg.backtest_control
                    mbc.begin_time = updated_para[0]
                    mbc.end_time = updated_para[1]
                    mbc.speed = updated_para[2]
                    mbc.source = updated_para[3]
                    mbc.indication = updated_para[4]
                    msg_bytes = msg.SerializeToString()
                    proxysender.send_msg(topic, msg_bytes)

                    conn = sqlite3.connect(control_db_path)
                    command = "update backtest_control set begin = '%s', end = '%s', speed = %d, source = %d, indication = %d;" % (
                        updated_para[0], updated_para[1], updated_para[2], updated_para[3], updated_para[4])
                    conn.execute(command)
                    conn.commit()
                    conn.close()

    def hand_backtest_operation(self, control_para):
        source_dict = {}
        source_dict[0] = 'rawtick'
        source_dict[1] = 'level1'
        source_dict[2] = 'm1_kline'
        indication_dict = {}
        indication_dict[0] = 'idle'
        indication_dict[1] = 'start'
        indication_dict[2] = 'stop'
        indication_dict[3] = 'finish'
        source_list = [source_dict[item] for item in source_dict]

        contain = st.container()
        col1, col2, col3, col4 = contain.columns(4)
        if control_para[5] in [cmp.BackTestControl.Indication.start, cmp.BackTestControl.Indication.stop]:
            begin = col1.text_input('begin time', control_para[0], disabled=True)
            end = col2.text_input('end time', control_para[1], disabled=True)
        else:
            begin = col1.text_input('begin time', control_para[0])
            end = col2.text_input('end time', control_para[1])
        source = col4.selectbox('source', source_list, source_list.index(source_dict[control_para[4]]))
        speed = col3.number_input('speed', 1, 1000, control_para[3], 10)
        source = source_list.index(source)
        indication = control_para[5]
        contain = st.container()
        col1, col2, col3 = contain.columns(3)
        if col1.button('start', key='start2'):
            indication = cmp.BackTestControl.Indication.start
        if col2.button('stop', key='stop2'):
            indication = cmp.BackTestControl.Indication.stop
        if col3.button('finish', key='finish2'):
            indication = cmp.BackTestControl.Indication.finish

        begin_date = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        if control_para[2] != '':
            temp_date = control_para[2].split('.')[0]
            now_date = datetime.datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')
        else:
            now_date = begin_date
        level1_iteration1 = st.empty()
        level1_bar = st.progress(0)
        process = int((now_date.timestamp() - begin_date.timestamp()) / (end_date.timestamp() - begin_date.timestamp()) * 100)
        process = 0 if process < 0 else process
        process = 100 if process > 100 else process
        level1_iteration1.text(f'Iteration {process}, now time: %s, status: %s' % (now_date, indication_dict[indication]))
        level1_bar.progress(process)

        return [begin, end, speed, source, indication]

    def virtual_account_set(self):
        account_para = []
        usernames = jsonconfig.get_config('trader', 'User')
        for username in usernames:
            if 'btp' not in username and 'ftp' not in username:
                continue
            temp_dir = jsonconfig.get_config('trader', 'ControlParaFilePath')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            control_db_path = '%s/backtest.db' % temp_dir
            conn = sqlite3.connect(control_db_path)
            try:
                user_id = username.split('_')[0]
                command = "select user_id, balance, rspmode from virtual_account where user_id = '%s';" % (user_id)
                account_para = conn.execute(command).fetchall()[0]
            except:
                command = "create table if not exists virtual_account(user_id TEXT, balance REAL, rspmode INT);"
                conn.execute(command)
                user_id = username.split('_')[0]
                command = "insert into virtual_account(user_id, balance, rspmode) select '%s', 1000000, 0 where not exists (select * from virtual_account where user_id = '%s');" % (
                    user_id, user_id)
                conn.execute(command)
                conn.commit()
            conn.close()

            if len(account_para) > 0:
                updated_para = self.hand_account_operation(account_para)
                if updated_para[0] == account_para[1] and updated_para[1] == account_para[2]:
                    pass
                else:
                    conn = sqlite3.connect(control_db_path)
                    command = "update virtual_account set balance = %f, rspmode = %d where user_id = '%s';" % (updated_para[0],
                                                                                                               updated_para[1], user_id)
                    conn.execute(command)
                    conn.commit()
                    conn.close()

    def hand_account_operation(self, account_para):
        rspmode_dict = {}
        rspmode_dict[0] = 'success'
        rspmode_dict[1] = 'waiting'
        rspmode_dict[2] = 'part_success'
        rspmode_dict[3] = 'no_money'
        rspmode_dict[4] = 'no_open'
        rspmode_dict[5] = 'no_time'
        rspmode_list = [rspmode_dict[item] for item in rspmode_dict]

        contain = st.container()
        col1, col2, col3 = contain.columns(3)
        account = col1.text_input('account', account_para[0], key='1_%s' % account_para[0], disabled=True)
        balance = col2.text_input('balance', account_para[1], key='2_%s' % account_para[0])
        rspmode = col3.selectbox('source', rspmode_list, rspmode_list.index(rspmode_dict[account_para[2]]), key='3_%s' % account_para[0])
        rspmode = rspmode_list.index(rspmode)

        return [float(balance), rspmode]


manual_page = manual()
