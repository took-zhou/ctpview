import datetime
import os
import sqlite3
import time

import streamlit as st
from ticknature.instrument_info import instrumentinfo

from ctpview.workspace.common.file_util import jsonconfig
from ctpview.workspace.common.protobuf import ctpview_market_pb2 as cmp
from ctpview.workspace.common.protobuf import ctpview_trader_pb2 as ctp
from ctpview.workspace.common.protobuf import market_trader_pb2 as mtp
from ctpview.workspace.common.protobuf import strategy_market_pb2 as smp
from ctpview.workspace.common.protobuf import strategy_trader_pb2 as stp
from ctpview.workspace.ctp.domain.components.control_page import control
from ctpview.workspace.ctp.infra.sender.direct_sender import directsender
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender


class manual():

    def __init__(self):
        pass

    def update(self):
        mode_str = [
            'login control', 'block quotation', 'bug injection', 'profiler control', 'backtest control', 'virtual account set',
            'order test', 'subscribe instrument', 'send test email', 'market state'
        ]
        manual_mode = st.selectbox('Manual mode', mode_str, key='manual_mode')

        if manual_mode == 'login control':
            self.login_control()
        elif manual_mode == 'block quotation':
            self.block_quotation()
        elif manual_mode == 'bug injection':
            self.bug_injection()
        elif manual_mode == 'profiler control':
            self.profiler_control()
        elif manual_mode == 'backtest control':
            self.backtest_control()
        elif manual_mode == 'virtual account set':
            self.virtual_account_set()
        elif manual_mode == 'order test':
            self.order_test()
        elif manual_mode == 'subscribe instrument':
            self.subscribe_instrument()
        elif manual_mode == 'send test email':
            self.send_test_email()
        elif manual_mode == 'market state':
            self.market_state()

    def login_control(self):
        contain = st.container()
        col1, col2, col3 = contain.columns(3)

        if col1.button('market login'):
            with st.status("market login send...") as st_status:
                topic = "ctpview_market.LoginControl"
                msg = cmp.message()
                mlc = msg.login_control
                mlc.command = cmp.LoginControl.Command.login
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="market login send complete", state="complete")

        if col2.button('market logout'):
            with st.status("market logout send...") as st_status:
                topic = "ctpview_market.LoginControl"
                msg = cmp.message()
                mlc = msg.login_control
                mlc.command = cmp.LoginControl.Command.logout
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="market logout send complete", state="complete")

        if col3.button('market reserve'):
            with st.status("market reserve send...") as st_status:
                topic = "ctpview_market.LoginControl"
                msg = cmp.message()
                mlc = msg.login_control
                mlc.command = cmp.LoginControl.Command.reserve
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="market reserve send complete", state="complete")

        if col1.button('trader login'):
            with st.status("trader login send...") as st_status:
                topic = "ctpview_trader.LoginControl"
                msg = ctp.message()
                mlc = msg.login_control
                mlc.command = ctp.LoginControl.Command.login
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="trader login send complete", state="complete")

        if col2.button('trader logout'):
            with st.status("trader logout send...") as st_status:
                topic = "ctpview_trader.LoginControl"
                msg = ctp.message()
                mlc = msg.login_control
                mlc.command = ctp.LoginControl.Command.logout
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="trader logout send complete", state="complete")

        if col3.button('trader reserve'):
            with st.status("trader reserve send...") as st_status:
                topic = "ctpview_trader.LoginControl"
                msg = ctp.message()
                mlc = msg.login_control
                mlc.command = ctp.LoginControl.Command.reserve
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="trader reserve send complete", state="complete")

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

        select_ins_list = st.multiselect('Select ins', subscribe_list)

        contain = st.container()
        col1, col2 = contain.columns(2)

        if col1.button('block'):
            with st.status("block send...") as st_status:
                topic = "ctpview_market.BlockControl"
                msg = cmp.message()
                mlc = msg.block_control
                mlc.command = cmp.BlockControl.Command.block
                for item in select_ins_list:
                    mlc.instrument.append(item)
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="block send complete", state="complete")

        if col2.button('unblock'):
            with st.status("unblock send...") as st_status:
                topic = "ctpview_market.BlockControl"
                msg = cmp.message()
                mlc = msg.block_control
                mlc.command = cmp.BlockControl.Command.unblock
                for item in select_ins_list:
                    mlc.instrument.append(item)
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="unblock send complete", state="complete")

    def bug_injection(self):
        contain = st.container()
        col1, col2 = contain.columns(2)

        if col1.button('market doublefree'):
            with st.status("market doublefree send...") as st_status:
                topic = "ctpview_market.BugInjection"
                msg = cmp.message()
                mbi = msg.bug_injection
                mbi.type = cmp.BugInjection.InjectionType.double_free
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="market doublefree send complete", state="complete")

        if col2.button('trader doublefree'):
            with st.status("trader doublefree send...") as st_status:
                topic = "ctpview_trader.BugInjection"
                msg = ctp.message()
                mbi = msg.bug_injection
                mbi.type = ctp.BugInjection.InjectionType.double_free
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="trader doublefree send complete", state="complete")

    def profiler_control(self):
        contain = st.container()
        col1, col2 = contain.columns(2)

        if col1.button('market start write'):
            with st.status("market start write send...") as st_status:
                topic = "ctpview_market.ProfilerControl"
                msg = cmp.message()
                mlc = msg.profiler_control
                mlc.profiler_action = cmp.ProfilerControl.ProfilerAction.start_write
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="market start write send complete", state="complete")

        if col2.button('market stop write'):
            with st.status("market stop write send...") as st_status:
                topic = "ctpview_market.ProfilerControl"
                msg = cmp.message()
                mlc = msg.profiler_control
                mlc.profiler_action = cmp.ProfilerControl.ProfilerAction.stop_write
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="market stop write send complete", state="complete")

        if col1.button('trader start write'):
            with st.status("trader start write send...") as st_status:
                topic = "ctpview_trader.ProfilerControl"
                msg = ctp.message()
                mlc = msg.profiler_control
                mlc.profiler_action = ctp.ProfilerControl.ProfilerAction.start_write
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="trader start write send complete", state="complete")

        if col2.button('trader stop write'):
            with st.status("trader stop write send...") as st_status:
                topic = "ctpview_trader.ProfilerControl"
                msg = ctp.message()
                mlc = msg.profiler_control
                mlc.profiler_action = ctp.ProfilerControl.ProfilerAction.stop_write
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="trader stop write send complete", state="complete")

    def backtest_control(self):
        control_para = []
        usernames = jsonconfig.get_config('market', 'User')
        if len(usernames) == 0 or usernames[0] == None or 'ftp' not in usernames[0]:
            st.info('need in ftp api and select account')
            return

        temp_dir = '%s/%s/' % (jsonconfig.get_config('market', 'ControlParaFilePath'), usernames[0])
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        control_db_path = '%s/backtest.db' % temp_dir
        conn = sqlite3.connect(control_db_path)
        command = "create table if not exists backtest_control(begin TEXT, end TEXT, now TEXT, speed INT, source INT, indication INT);"
        conn.execute(command)
        if 'backtest_control' in st.session_state:
            backtest_para = st.session_state['backtest_control']
            command = "insert into backtest_control(begin, end, now, speed, source, indication) select '%s', '%s', '', %d, %d, 0 where not exists (select * from backtest_control);" % (
                backtest_para[0], backtest_para[1], backtest_para[2], backtest_para[3])
        else:
            command = "insert into backtest_control(begin, end, now, speed, source, indication) select '2015-01-01 09:00:00', '2020-12-31 15:00:00', '', 1, 0, 0 where not exists (select * from backtest_control);"
        conn.execute(command)
        command = 'select begin, end, now, speed, source, indication from backtest_control;'
        control_para = conn.execute(command).fetchall()[0]
        conn.commit()
        conn.close()

        if len(control_para) > 0:
            updated_para = self.hand_backtest_operation(control_para)

        if st.button("update backtest control"):
            with st.status("update backtest control...") as st_status:
                self.backtest_control_click(updated_para)
                st_status.update(label="update backtest control complete", state="complete")

    def hand_backtest_operation(self, control_para):
        source_dict = {}
        source_dict[0] = 'rawtick'
        source_dict[1] = 'level1'
        source_dict[2] = 'm1_kline'
        indication_dict = {}
        indication_dict[0] = 'idle'
        indication_dict[1] = 'start'
        indication_dict[2] = 'stop'
        indication_dict[3] = 'step'
        indication_dict[4] = 'finish'
        source_list = [source_dict[item] for item in source_dict]
        indication_list = [indication_dict[item] for item in indication_dict]

        contain = st.container()
        col1, col2 = contain.columns(2)
        if control_para[5] in [1, 2]:
            begin = col1.text_input('Begin time', control_para[0], disabled=True)
            end = col2.text_input('End time', control_para[1], disabled=True)
        else:
            begin = col1.text_input('Begin time', control_para[0])
            end = col2.text_input('End time', control_para[1])
        col1, col2, col3 = contain.columns(3)
        speed = col1.number_input('Speed', 1, 10000, control_para[3], 10)
        source = col2.selectbox('Source', source_list, source_list.index(source_dict[control_para[4]]))
        indication = col3.selectbox('Indication', indication_list, indication_list.index(indication_dict[control_para[5]]))
        source = source_list.index(source)
        indication = indication_list.index(indication)

        begin_date = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        if control_para[2] != '':
            temp_date = control_para[2].split('.')[0]
            now_date = datetime.datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')
        else:
            now_date = begin_date
        level1_iteration1 = st.empty()
        level1_bar = st.progress(0)
        process = int((now_date.timestamp() - begin_date.timestamp()) / (end_date.timestamp() - begin_date.timestamp()) * 100 + 0.5)
        process = 0 if process < 0 else process
        process = 100 if process > 100 else process
        level1_iteration1.text(f'Iteration {process}, now time {now_date}, status {indication_dict[indication]}')
        level1_bar.progress(process)

        return [begin, end, speed, source, indication]

    def backtest_control_click(self, updated_para):
        usernames = jsonconfig.get_config('market', 'User')
        temp_dir = '%s/%s/' % (jsonconfig.get_config('market', 'ControlParaFilePath'), usernames[0])
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        control_db_path = '%s/backtest.db' % temp_dir
        conn = sqlite3.connect(control_db_path)
        command = "update backtest_control set begin = '%s', end = '%s', speed = %d, source = %d, indication = %d;" % (
            updated_para[0], updated_para[1], updated_para[2], updated_para[3], updated_para[4])
        conn.execute(command)
        conn.commit()
        conn.close()
        st.session_state['backtest_control'] = updated_para

    def virtual_account_set(self):
        account_para = []
        usernames = jsonconfig.get_config('trader', 'User')

        username = st.selectbox("User", usernames)
        if username == None or ('btp' not in username and 'ftp' not in username):
            st.info('need in ftp/btp api and select user')
            return
        temp_dir = jsonconfig.get_config('trader', 'ControlParaFilePath')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        control_db_path = '%s/backtest.db' % temp_dir
        conn = sqlite3.connect(control_db_path)
        user_id = username.split('_')[0]
        command = "create table if not exists virtual_account(user_id TEXT, balance REAL, available REAL, rspmode INT, updated INT);"
        conn.execute(command)
        user_id = username.split('_')[0]
        command = "insert into virtual_account(user_id, balance, available, rspmode, updated) select '%s', 1000000, 1000000, 0 , 0 where not exists (select * from virtual_account where user_id = '%s');" % (
            user_id, user_id)
        conn.execute(command)
        command = "select user_id, balance, available, rspmode from virtual_account where user_id = '%s';" % (user_id)
        account_para = conn.execute(command).fetchall()[0]
        conn.commit()
        conn.close()

        if len(account_para) > 0:
            account_para = self.hand_account_operation(account_para)

        if st.button("update %s" % (username.split('_')[0])):
            with st.status("update %s..." % (username.split('_')[0])) as st_status:
                self.virtual_account_set_click(account_para)
                st_status.update(label="update %s complete" % (username.split("_")[0]), state="complete")

    def virtual_account_set_click(self, updated_para):
        temp_dir = jsonconfig.get_config('trader', 'ControlParaFilePath')
        control_db_path = '%s/backtest.db' % temp_dir
        conn = sqlite3.connect(control_db_path)
        command = "update virtual_account set balance = %.15g, available = %.15g, rspmode = %d, updated = 1 where user_id = '%s';" % (
            updated_para[1], updated_para[2], updated_para[3], updated_para[0])
        conn.execute(command)
        conn.commit()
        conn.close()

    def hand_account_operation(self, account_para):
        rspmode_dict = {}
        rspmode_dict[0] = 'immediately complete'
        rspmode_dict[1] = 'waiting'
        rspmode_dict[2] = 'multiple partial'
        rspmode_dict[3] = 'multiple complete'
        rspmode_list = [rspmode_dict[item] for item in rspmode_dict]

        contain = st.container()
        col1, col2, col3 = contain.columns(3)
        balance = col1.text_input('Balance', account_para[1], key='2_%s' % account_para[0])
        available = col2.text_input('Available', account_para[2], key='3_%s' % account_para[0])
        rspmode = col3.selectbox('Source', rspmode_list, rspmode_list.index(rspmode_dict[account_para[3]]), key='4_%s' % account_para[0])
        rspmode = rspmode_list.index(rspmode)

        return [account_para[0], float(balance), float(available), rspmode]

    def order_test(self):
        if 'order_test' not in st.session_state:
            st.session_state['order_test'] = ['CZCE', 'TA401', '0001', '0', 0, 0, 'buy', 'open', 'limit limit']
        order_para = st.session_state['order_test']
        exch = st.text_input('Exch', order_para[0])
        ins = st.text_input('Ins', order_para[1])
        index = st.text_input('Index', order_para[2])
        limit_price = st.text_input('Limit price', order_para[3])
        once_volume = st.number_input('Once volume', value=order_para[4], step=-1)
        hold_volume = st.number_input('Hold volume', value=order_para[5], step=-1)
        para_list = ['buy', 'sell']
        direction = st.selectbox('Direction', para_list, para_list.index(order_para[6]), key='order test direction')
        para_list = ['open', 'close']
        comb_offset_flag = st.selectbox('Comb offset flag', para_list, para_list.index(order_para[7]), key='order test comb_offset_flag')
        order_dict = {'limit limit': 1, 'limit fak': 2, 'limit fok': 3, 'anyprice fok': 4, 'anyprice fak': 5}
        order_type = st.selectbox('Order type', list(order_dict.keys()), list(order_dict.keys()).index(order_para[8]), key='open_type')
        contain = st.container()
        col1, col2 = contain.columns(2)
        if col1.button('insert order'):
            with st.status("insert order send...") as st_status:
                topic = "strategy_trader.OrderInsertReq"

                msg = stp.message()
                oims = msg.order_insert_req
                oims.instrument = ins
                oims.index = index

                order = oims.order
                order.exchangeId = exch
                order.instrument = ins
                order.limit_price = float(limit_price)
                order.once_volume = int(once_volume)
                order.hold_volume = int(hold_volume)

                if direction == 'buy':
                    order.direction = stp.Direction.BUY
                elif direction == 'sell':
                    order.direction = stp.Direction.SELL

                if comb_offset_flag == 'open':
                    order.comb_offset_flag = stp.CombOffsetType.OPEN
                elif comb_offset_flag == 'close':
                    order.comb_offset_flag = stp.CombOffsetType.CLOSE
                elif comb_offset_flag == 'close_yesterday':
                    order.comb_offset_flag = stp.CombOffsetType.CLOSE_YESTERDAY
                elif comb_offset_flag == 'close_today':
                    order.comb_offset_flag = stp.CombOffsetType.CLOSE_TODAY
                order.order_type = order_dict[order_type]

                msg_bytes = msg.SerializeToString()
                directsender.send_msg(topic, msg_bytes)
                st_status.update(label="insert order complete", state="complete")

        if col2.button('cancle order'):
            with st.status("cancle order send...") as st_status:
                topic = "strategy_trader.OrderCancelReq"

                msg = stp.message()
                ocr = msg.order_cancel_req
                ocr.instrument = ins
                ocr.index = index

                msg_bytes = msg.SerializeToString()
                directsender.send_msg(topic, msg_bytes)
                st_status.update(label="cancle order send complete", state="complete")

        st.session_state['order_test'] = [exch, ins, index, limit_price, once_volume, hold_volume, direction, comb_offset_flag, order_type]

    def subscribe_instrument(self):
        exch = st.text_input('Exch', 'CZCE')
        ins = st.text_input('Ins', 'TA301')
        contain = st.container()
        col1, col2 = contain.columns(2)
        if col1.button('subscribe'):
            with st.status("subscribe send...") as st_status:
                topic = "strategy_market.TickSubscribeReq"
                msg = smp.message()
                tsr = msg.tick_sub_req
                info = tsr.instrument_info
                info.instrument_id = ins
                info.exchange_id = exch
                tsr.action = smp.TickSubscribeReq.Action.sub
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="subscribe send complete", state="complete")

        if col2.button('unsubcribe'):
            with st.status("unsubcribe send...") as st_status:
                topic = "strategy_market.TickSubscribeReq"
                msg = smp.message()
                tsr = msg.tick_sub_req
                info = tsr.instrument_info
                info.instrument_id = ins
                info.exchange_id = exch
                tsr.action = smp.TickSubscribeReq.Action.unsub
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="unsubcribe send complete", state="complete")

    def send_test_email(self):
        contain = st.container()
        col1, col2 = contain.columns(2)
        if col1.button('market send'):
            with st.status("market send...") as st_status:
                topic = 'ctpview_market.SendTestEmail'
                msg = cmp.message()
                mse = msg.send_email
                mse.send_action = cmp.SendTestEmail.SendAction.send
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="market send complete", state="complete")

        if col2.button('trader send'):
            with st.status("trader send...") as st_status:
                topic = 'ctpview_trader.SendTestEmail'
                msg = ctp.message()
                mse = msg.send_email
                mse.send_action = ctp.SendTestEmail.SendAction.send
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="trader send complete", state="complete")

    def get_newest_state(self):
        now_hour = datetime.datetime.now().hour
        if now_hour >= 8 and now_hour <= 15:
            now_state = 2
        elif now_hour >= 16 and now_hour <= 19:
            now_state = 3
        elif now_hour >= 20 or now_hour <= 2:
            now_state = 0
        else:
            now_state = 1

        return now_state

    def get_newest_date(self):
        if datetime.date.today().weekday() in [0, 1, 2, 3, 4]:
            if datetime.datetime.now().hour <= 20:
                select_date = st.date_input('Select date', datetime.date.today())
            else:
                if datetime.date.today().weekday() == 4:
                    select_date = st.date_input('Select date', datetime.date.today() + datetime.timedelta(days=3))
                else:
                    select_date = st.date_input('Select date', datetime.date.today() + datetime.timedelta(days=1))
        elif datetime.date.today().weekday() == 5:
            select_date = st.date_input('Select date', datetime.date.today() + datetime.timedelta(days=2))
        elif datetime.date.today().weekday() == 6:
            select_date = st.date_input('Select date', datetime.date.today() + datetime.timedelta(days=1))

        datestr = '%04d%02d%02d' % (select_date.year, select_date.month, select_date.day)

        return datestr

    def market_state(self):
        now_state = self.get_newest_state()
        market_state = st.selectbox('Market state', ['night open', 'night close', 'day open', 'day close'], now_state, key='market_state')
        datestr = self.get_newest_date()

        if st.button('send'):
            with st.status("market state send...") as st_status:
                topic = "market_trader.MarketStateReq"
                msg = mtp.message()
                mmsr = msg.market_state_req
                if market_state == 'day open':
                    mmsr.market_state = mtp.MarketStateReq.MarketState.day_open
                elif market_state == 'day close':
                    mmsr.market_state = mtp.MarketStateReq.MarketState.day_close
                elif market_state == 'night open':
                    mmsr.market_state = mtp.MarketStateReq.MarketState.night_open
                elif market_state == 'night close':
                    mmsr.market_state = mtp.MarketStateReq.MarketState.night_close
                else:
                    mmsr.market_state = mtp.MarketStateReq.MarketState.reserve

                mmsr.date = datestr
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="market state send complete", state="complete")
