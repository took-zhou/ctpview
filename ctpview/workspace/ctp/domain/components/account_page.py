import json
import sqlite3
from datetime import datetime

import pandas as pd
import plotly.graph_objs as go
import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig


class account():

    def __init__(self):
        pass

    def update(self):
        now_user = []
        try:
            with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
                read_json = json.load(fp)
            temp_now_user = read_json['trader']['User']
            now_user = [item.split('_')[0] for item in temp_now_user]
        except:
            pass

        for item in now_user:
            control_db_path = '%s/control.db' % (jsonconfig.get_config('trader', 'ControlParaFilePath'))
            conn = sqlite3.connect(control_db_path)
            last_info = []
            try:
                command = 'select session_id, balance, available, open_blacklist from account_info where user_id="%s";' % (item)
                last_info = conn.execute(command).fetchall()[0]
            except:
                # error_msg = traceback.format_exc()
                # print(error_msg)
                pass
            conn.close()

            if last_info != []:
                message = 'account: %s, balance: %f, available: %f, open_blacklist: %s' % (item, last_info[1], last_info[2], last_info[3])
                with st.expander(message):
                    self.show_capital(item)
                    self.show_position(item)

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

        data = [
            go.Scatter(x=date_list, y=balance_list, name='balance', showlegend=True),
        ]
        st.plotly_chart(data)

    def show_position(self, user_id):
        control_db_path = '%s/control.db' % (jsonconfig.get_config('trader', 'ControlParaFilePath'))
        conn = sqlite3.connect(control_db_path)
        position_info = []
        try:
            command = 'select order_index, yesterday_volume, today_volume from order_lookup where user_id="%s";' % (user_id)
            position_info = conn.execute(command).fetchall()
        except:
            # error_msg = traceback.format_exc()
            # print(error_msg)
            pass
        conn.close()

        if position_info != []:
            ins_list = []
            yesterday_volume_list = []
            today_volume_list = []
            for item in position_info:
                if item[1] != 0 or item[2] != 0:
                    ins_list.append(item[0].split('.')[0])
                    yesterday_volume_list.append(item[1])
                    today_volume_list.append(item[2])

            pisition_dict = {'ins': ins_list, 'yesterday_volume': yesterday_volume_list, 'today_volume': today_volume_list}

            position_df = pd.DataFrame(pisition_dict)
            st.table(position_df)


account_page = account()