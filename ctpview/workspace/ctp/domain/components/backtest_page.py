import datetime
import json

import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig
from ctpview.workspace.common.protobuf import ctpview_market_pb2 as cmp
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender


class backtest:

    def __init__(self):
        self.backtest_control_json = {}

    def update(self):
        self.backtest_control_json = {}
        try:
            for item in jsonconfig.get_config('market', 'User'):
                market_control_path = jsonconfig.get_config('market', 'ControlParaFilePath')
                with open('%s/%s/BacktestControl/control.json' % (market_control_path, item), 'r', encoding='utf8') as fp:
                    self.backtest_control_json = json.load(fp)
                    fp.close()
        except:
            pass

        self.operation()

    def operation(self):
        contain = st.container()
        col1, col2, col3 = contain.columns(3)
        if self.backtest_control_json != {}:
            begin = col1.text_input('begin time', self.backtest_control_json['begin'])
            end = col2.text_input('end time', self.backtest_control_json['end'])
            speed = col3.number_input('speed', 1, 1000, self.backtest_control_json['speed'], 10)
        else:
            begin = col1.text_input('begin time', '2015-01-01 09:00:00')
            end = col2.text_input('end time', '2020-12-31 15:00:00')
            speed = col3.number_input('speed', 1, 1000, 1, 10)

        begin_date = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        if 'now' in self.backtest_control_json and self.backtest_control_json['now'] != '':
            temp_date = self.backtest_control_json['now'].split('.')[0]
            now_date = datetime.datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')
        else:
            now_date = begin_date
        level1_iteration1 = st.empty()
        level1_bar = st.progress(0)
        process = int((now_date.timestamp() - begin_date.timestamp()) / (end_date.timestamp() - begin_date.timestamp()) * 100)
        process = 0 if process < 0 else process
        process = 100 if process > 100 else process
        level1_iteration1.text(f'Iteration {process}, now time: %s' % (now_date))
        level1_bar.progress(process)

        contain = st.container()
        col1, col2, col3, col4 = contain.columns(4)
        if col1.button('start', key='start2'):
            self.handle_start_button(begin, end, speed)
        if col2.button('stop', key='stop2'):
            self.handle_stop_button()
        if col3.button('finish', key='finish2'):
            self.handle_finish_button()
        if col4.button('update speed', key='update2'):
            self.handle_speed_change(begin, end, speed)

    def handle_speed_change(self, begin, end, speed):
        topic = "ctpview_market.BackTestControl"
        msg = cmp.message()
        mbc = msg.backtest_control
        mbc.begin_time = begin
        mbc.end_time = end
        mbc.speed = speed
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

    def handle_start_button(self, begin, end, speed):
        topic = "ctpview_market.BackTestControl"
        msg = cmp.message()
        mbc = msg.backtest_control
        mbc.begin_time = begin
        mbc.end_time = end
        mbc.speed = speed
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.start
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

    def handle_stop_button(self):
        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.stop
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)

    def handle_finish_button(self):
        topic = "ctpview_market.TickStartStopIndication"
        msg = cmp.message()
        mtsi = msg.tick_start_stop_indication
        mtsi.type = cmp.TickStartStopIndication.MessageType.finish
        msg_bytes = msg.SerializeToString()
        proxysender.send_msg(topic, msg_bytes)


backtest_page = backtest()
