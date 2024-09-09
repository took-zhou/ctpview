import json
import os
import sqlite3
from datetime import datetime

import pandas as pd
import plotly.graph_objs as go
import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig
from ctpview.workspace.common.protobuf import ctpview_trader_pb2 as ctp
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender


class account():

    def __init__(self):
        pass

    def update(self):
        self.now_user = []
        try:
            with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
                read_json = json.load(fp)
            temp_now_user = read_json['trader']['User']
            self.now_user = [item.split('_')[0] for item in temp_now_user]
        except:
            pass

        if not os.path.exists(jsonconfig.get_config('trader', 'ControlParaFilePath')):
            os.makedirs(jsonconfig.get_config('trader', 'ControlParaFilePath'))

        st.subheader('exist')
        for item in self.now_user:
            self.show_info(item)
            self.show_capital(item)
            self.show_position(item)
            st.write('----')

        st.subheader('operation')
        self.show_group()
        self.update_group()

    def show_info(self, user_id):
        control_db_path = '%s/control.db' % (jsonconfig.get_config('trader', 'ControlParaFilePath'))
        conn = sqlite3.connect(control_db_path)
        last_info = []
        try:
            command = 'select session_id,balance,available,open_blacklist from account_info where user_id="%s";' % (user_id)
            last_info = conn.execute(command).fetchall()[0]
        except:
            # error_msg = traceback.format_exc()
            # print(error_msg)
            pass
        conn.close()

        if last_info != []:
            message = 'account`%s|%.15g|%.15g|%s`' % (user_id, last_info[1], last_info[2], last_info[3])
            st.write(message)

    def show_capital(self, user_id):
        control_db_path = '%s/control.db' % (jsonconfig.get_config('trader', 'ControlParaFilePath'))
        conn = sqlite3.connect(control_db_path)
        history_info = []
        try:
            command = 'select date, balance from account where user_id="%s";' % (user_id)
            history_info = conn.execute(command).fetchall()
        except:
            # error_msg = traceback.format_exc()
            # print(error_msg)
            pass
        conn.close()

        date_list = [datetime.strptime(item[0], '%Y%m%d') for item in history_info]
        balance_list = [item[1] for item in history_info]

        if len(date_list) > 0:
            data = [
                go.Scatter(x=date_list, y=balance_list, name='balance', showlegend=True),
            ]
            st.plotly_chart(data)

    def show_position(self, user_id):
        control_db_path = '%s/control.db' % (jsonconfig.get_config('trader', 'ControlParaFilePath'))
        conn = sqlite3.connect(control_db_path)
        position_info = []
        try:
            command = 'select order_index, yesterday_volume, today_volume from order_lookup where user_id like "%%%s";' % (user_id)
            position_info = conn.execute(command).fetchall()
        except:
            # error_msg = traceback.format_exc()
            # print(error_msg)
            pass
        conn.close()

        if position_info != []:
            index_list = []
            ins_list = []
            yesterday_volume_list = []
            today_volume_list = []
            for item in position_info:
                if item[1] != 0 or item[2] != 0:
                    index_list.append(item[0].split('.')[1])
                    ins_list.append(item[0].split('.')[0])
                    yesterday_volume_list.append(item[1])
                    today_volume_list.append(item[2])

            pisition_dict = {
                'index': index_list,
                'ins': ins_list,
                'yesterday volume': yesterday_volume_list,
                'today volume': today_volume_list
            }

            position_df = pd.DataFrame(pisition_dict)
            st.table(position_df)

    def show_group(self):
        contain = st.container()
        col1, col2 = contain.columns([1, 4])
        self.select_group = col1.selectbox('group name', [item for item in ['name%02d' % (i + 1) for i in range(32)]])
        control_db_path = '%s/control.db' % (jsonconfig.get_config('trader', 'ControlParaFilePath'))
        conn = sqlite3.connect(control_db_path)
        exist_accounts = []
        account_info = []
        try:
            command = 'select account from group_info where group_id="%s";' % (self.select_group)
            account_info = conn.execute(command).fetchall()
        except:
            # error_msg = traceback.format_exc()
            # print(error_msg)
            pass
        conn.close()
        for item in account_info:
            if item[0] in self.now_user:
                exist_accounts.append(item[0])

        self.select_accounts = col2.multiselect('account list', self.now_user, exist_accounts, key=self.select_group)

    def update_group(self):
        if st.button('update group'):
            with st.status("update group...") as st_status:
                topic = "ctpview_trader.UpdateAccountGroup"
                msg = ctp.message()
                muag = msg.update_account_group
                muag.group_id = self.select_group
                for item in self.select_accounts:
                    muag.account.append(item)
                msg_bytes = msg.SerializeToString()
                proxysender.send_msg(topic, msg_bytes)
                st_status.update(label="update group complete", state="complete")
