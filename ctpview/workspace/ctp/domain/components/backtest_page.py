import datetime
import json

import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig
from ctpview.workspace.common.protobuf import ctpview_market_pb2 as cmp
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender


class backtest:

    def __init__(self):
        self.para_control_json = {}
        self.backtest_control_json = {}
        self.prids = []
        self.prid = ''

    def update(self):
        try:
            for item in jsonconfig.get_config('market', 'User'):
                market_control_path = jsonconfig.get_config('market', 'ControlParaFilePath')
                with open('%s/%s/BacktestControl/control.json' % (market_control_path, item), 'r', encoding='utf8') as fp:
                    self.backtest_control_json = json.load(fp)
                    fp.close()
        except:
            pass

        try:
            market_control_path = jsonconfig.get_config('market', 'ControlParaFilePath')
            with open('%s/controlPara/control.json' % (market_control_path), 'r', encoding='utf8') as fp:
                self.para_control_json = json.load(fp)
                fp.close()
                self.prids = list(set(self.para_control_json['prid']))
        except:
            self.prids = []
            pass

        self.prid = st.selectbox('prids', self.prids, key='prids')

        self.operation()

    def operation(self):
        contain = st.container()
        col1, col2, col3 = contain.columns(3)
        if self.prid in self.backtest_control_json:
            begin = col1.text_input('begin time', self.backtest_control_json[self.prid]['begin'])
            end = col2.text_input('end time', self.backtest_control_json[self.prid]['end'])
            speed = col3.number_input('speed', self.backtest_control_json[self.prid]['speed'])
            now = self.backtest_control_json[self.prid]['now']
        else:
            begin = col1.text_input('begin time', '2015-01-01 09:00:00')
            end = col2.text_input('end time', '2020-12-31 15:00:00')
            speed = col3.number_input('speed', 1)
            now = begin

        begin_date = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        now_date = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        level1_iteration1 = st.empty()
        level1_bar = st.progress(0)
        process = int((now_date - begin_date).days / (end_date - begin_date).days * 100)
        level1_iteration1.text(f'Iteration {process}, date: %s' % (str(now_date).split(' ')[0]))
        level1_bar.progress(process)

        st.write('single')
        contain = st.container()
        col1, col2, col3 = contain.columns(3)
        if col1.button('start', key='start1'):
            self.hand_single_start_button(begin, end, speed)
        if col2.button('stop', key='stop1'):
            self.hand_single_stop_button()
        if col3.button('finish', key='finish1'):
            self.hand_single_finish_button()

        st.write('total')
        contain = st.container()
        col1, col2, col3 = contain.columns(3)
        if col1.button('start', key='start2'):
            self.hand_total_start_button(begin, end, speed)
        if col2.button('stop', key='stop2'):
            self.hand_total_stop_button()
        if col3.button('finish', key='finish2'):
            self.hand_total_finish_button()

    def hand_single_start_button(self, begin, end, speed):
        topic = "ctpview_market.BackTestControl"
        msg = cmp.message()
        mbc = msg.backtest_control
        mbc.process_random_id = self.prid
        mbc.begin_time = begin
        mbc.end_time = end
        mbc.speed = speed
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.start
        mtsi.process_random_id = self.prid
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

    def hand_single_stop_button(self):
        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.stop
        mtsi.process_random_id = self.prid
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

    def hand_single_finish_button(self):
        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.finish
        mtsi.process_random_id = self.prid
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

    def hand_total_start_button(self, begin, end, speed):
        for prid in self.prids:
            topic = "ctpview_market.BackTestControl"
            msg = cmp.message()
            mbc = msg.backtest_control
            mbc.process_random_id = prid
            mbc.begin_time = begin
            mbc.end_time = end
            mbc.speed = speed
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.start
        mtsi.process_random_id = ""
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

    def hand_total_stop_button(self):
        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.stop
        mtsi.process_random_id = ""
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

    def hand_total_finish_button(self):
        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.finish
        mtsi.process_random_id = ""
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)


backtest_page = backtest()
