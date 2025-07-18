import json
import os
import time

import psutil
import streamlit as st

from ctpview.workspace.common.protobuf import ctpview_market_pb2 as cmp
from ctpview.workspace.common.protobuf import ctpview_trader_pb2 as ctp
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender


class parameter():

    def __init__(self):
        self.api_types = ['ctp', 'xtp', 'btp', 'otp', 'ftp', 'gtp', 'ltp', 'ytp']

    def update(self):
        self.read_para()

        self.update_common_para()

        self.update_market_para()

        self.update_trader_para()

        st.write('____')

        self.update_and_reset_para()

    def read_para(self):
        with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
            self.read_json = json.load(fp)
        fp.close()

    def update_common_para(self):
        st.subheader('common')

        common_needshow_para = ['ApiType']
        email_needshow_para = ['redipients']
        common_json = self.read_json['common']
        for item in common_json:
            if item in common_needshow_para:
                if item == 'ApiType':
                    title = st.selectbox(item, self.api_types, self.api_types.index(common_json[item]), key='apitype')
                    self.read_json["common"][item] = title
                else:
                    title = st.text_input(item, common_json[item])
                    self.read_json["common"][item] = title

        email_json = self.read_json['emailbox']
        for item in email_json:
            if item in email_needshow_para:
                if item == 'redipients':
                    title = st.multiselect(item, email_json['emails'], email_json[item])
                    self.read_json["emailbox"][item] = title
                else:
                    pass

    def update_market_para(self):
        st.subheader('market')

        market_needshow_para = ['User', 'LogInTimeList', 'TimingPush', 'SubscribeMarketDataFrom']
        market_json = self.read_json['market']
        for item in market_json:
            if item in market_needshow_para:
                if item == 'SubscribeMarketDataFrom':
                    title = st.selectbox(item, ['local', 'strategy', 'api'], \
                                         ['local', 'strategy', 'api'].index(self.read_json["market"][item]), key='datafrom')
                    self.read_json["market"][item] = title
                elif item == 'TimingPush':
                    action_list = ['yes', 'no']
                    title = st.selectbox(item, action_list, action_list.index(market_json[item]), key='timeing_push')
                    self.read_json["market"][item] = title
                elif item == 'User':
                    user_list = [item for item in self.read_json['users'].keys()]
                    api_users = self.get_users(user_list, self.read_json['common']['ApiType'])
                    now_user = self.read_json['market']['User'][0]
                    if now_user in api_users:
                        title = st.selectbox(item, api_users, api_users.index(now_user), key='marketuserid')
                    else:
                        title = st.selectbox(item, api_users, index=None, key='marketuserid')
                    self.read_json["market"][item] = [title]
                elif item == 'LogInTimeList':
                    login_time_list = ['08:06-15:15;20:06-02:30', '08:00-07:00']
                    login_index = self.get_login_index(self.read_json['common']['ApiType'], self.read_json['market']['User'])
                    title = st.selectbox(item, login_time_list, login_index, key='market_login_time')
                    self.read_json["market"][item] = title
                else:
                    title = st.text_input('Market%s' % item, market_json[item])
                    self.read_json["market"][item] = title

    def update_trader_para(self):
        st.subheader('trader')

        trader_needshow_para = ['User', 'LogInTimeList', 'SendOrderEmail', 'AccountAssignMode']
        trader_json = self.read_json['trader']
        for item in trader_json:
            if item in trader_needshow_para:
                if item == 'User':
                    user_list = [item for item in self.read_json['users'].keys()]
                    api_users = self.get_users(user_list, self.read_json['common']['ApiType'])
                    now_user = self.read_json['trader']['User']
                    d = [False for c in now_user if c not in api_users]
                    if d:
                        title = st.multiselect(item, api_users, [])
                    else:
                        title = st.multiselect(item, api_users, now_user)
                    self.read_json["trader"][item] = title
                elif item == 'SendOrderEmail':
                    action_list = ['yes', 'no']
                    title = st.selectbox(item, action_list, action_list.index(trader_json[item]), key='send_email')
                    self.read_json["trader"][item] = title
                elif item == 'AccountAssignMode':
                    assign_mode = ['cycle', 'share']
                    title = st.selectbox(item, assign_mode, assign_mode.index(trader_json[item]), key='assign_mode')
                    self.read_json["trader"][item] = title
                elif item == 'LogInTimeList':
                    login_time_list = ['08:05-15:16;20:05-02:31', '07:59-07:01']
                    login_index = self.get_login_index(self.read_json['common']['ApiType'], self.read_json['trader']['User'])
                    title = st.selectbox(item, login_time_list, login_index, key='trader_login_time')
                    self.read_json["trader"][item] = title
                else:
                    title = st.text_input('Trader%s' % item, trader_json[item])
                    self.read_json["trader"][item] = title

    def update_and_reset_para(self):
        if not ('name' in st.session_state and st.session_state['name'] == 'admin'):
            return

        contain = st.container()
        col1, col2, col3 = contain.columns(3)
        if col1.button('update para'):
            with st.status("update para...") as st_status:
                self.update_para_click()
                st_status.update(label="update para complete", state="complete")

        if col2.button('reset para'):
            with st.status("reset para...") as st_status:
                self.reset_para_click()
                st_status.update(label="reset para complete", state="complete")

        if col3.button('restore para'):
            with st.status('restore para...') as st_status:
                self.restore_para_click()
                st_status.update(label='restore para complete', state="complete")

    def update_para_click(self):
        f_d = open('/etc/marktrade/config.json', 'w', encoding="utf-8")
        json.dump(self.read_json, f_d, indent=4)
        f_d.close()

        command = 'mkdir -p ~/.local/marktrade/; cp /etc/marktrade/config.json ~/.local/marktrade/config.json'
        os.system(command)

        if self.checkprocess('market') != '' or self.checkprocess('trader') != '':
            topic = "ctpview_market.UpdatePara"
            msg = cmp.message()
            mupp = msg.update_para
            mupp.update_action = cmp.UpdatePara.UpdateAction.update
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

            topic = "ctpview_trader.UpdatePara"
            msg = ctp.message()
            mupp = msg.update_para
            mupp.update_action = ctp.UpdatePara.UpdateAction.update
            msg_bytes = msg.SerializeToString()
            proxysender.send_msg(topic, msg_bytes)

    def reset_para_click(self):
        f_d = open('/etc/marktrade/config.json', 'w', encoding="utf-8")
        self.read_json['emailbox']['redipients'] = []
        self.read_json['trader']['User'] = []
        json.dump(self.read_json, f_d, indent=4)
        f_d.close()

    def restore_para_click(self):
        command = 'cp ~/.local/marktrade/config.json /etc/marktrade/config.json'
        os.system(command)

    def get_users(self, users, key):
        if key == 'ctp':
            return [item for item in users if 'simnow' in item or 'citic' in item or 'zhonghui' in item or 'minsheng' in item]
        elif key == 'xtp':
            return [item for item in users if 'xtp' in item]
        elif key == 'btp':
            return [item for item in users if 'btp' in item]
        elif key == 'otp':
            return [item for item in users if 'otp' in item]
        elif key == 'ftp':
            return [item for item in users if 'ftp' in item]
        elif key == 'gtp':
            return [item for item in users if 'gtp' in item]
        elif key == 'ltp':
            return [item for item in users if 'ltp' in item]
        elif key == 'ytp':
            return [item for item in users if 'ytp' in item]

    def get_login_index(self, api_type, users):
        ret = 0
        if api_type in ['gtp', 'ltp', 'ytp']:
            ret = 1
        elif api_type in ['ctp']:
            ret = 0
        elif api_type in ['btp']:
            for user in users:
                if user != None and user.split('_')[0] >= '100004':
                    ret = 1
                else:
                    ret = 0
                break
        elif api_type in ['ftp']:
            for user in users:
                if user != None and user.split('_')[0] >= '200004':
                    ret = 1
                else:
                    ret = 0
                break
        else:
            ret = 0
        return ret

    def checkprocess(self, processname):
        # --获取进程信息--
        pl = psutil.pids()  #所有的进程列出来

        for pid in pl:
            try:
                if psutil.Process(pid).name() == processname:
                    return pid
            except:
                continue

        return ''
