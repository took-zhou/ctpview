import json
import os

import psutil
import streamlit as st

from ctpview.workspace.common.protobuf import ctpview_market_pb2 as cmp
from ctpview.workspace.common.protobuf import ctpview_trader_pb2 as ctp
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender


class parameter:

    def __init__(self):
        self.disable_write = False
        self.common_para_change = False
        self.market_para_change = False
        self.trader_para_change = False
        self.api_types = ['ctp', 'xtp', 'btp', 'otp', 'ftp']

    def update(self):
        self.check_parameter_writtable()

        self.update_common_para()

        self.update_market_para()

        self.update_trader_para()

        st.write('____')

        self.online_update_para()

    def update_common_para(self):
        st.header('%s' % ("common:"))

        common_needshow_para = ['ApiType']
        email_needshow_para = ['redipients']
        try:
            with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
                read_json = json.load(fp)
            fp.close()

            self.common_para_change = False
            common_json = read_json['common']
            for item in common_json:
                if item in common_needshow_para:
                    if item == 'ApiType':
                        title = st.selectbox('%s(%s): ' % (item, 'common'),
                                             self.api_types,
                                             self.api_types.index(common_json[item]),
                                             key='apitype',
                                             disabled=self.disable_write)
                        if read_json["common"][item] != title:
                            read_json["common"][item] = title
                            self.common_para_change = True
                    else:
                        title = st.text_input('%s(%s): ' % (item, 'common'), common_json[item], disabled=self.disable_write)
                        if read_json["common"][item] != title:
                            read_json["common"][item] = title
                            self.common_para_change = True

            email_json = read_json['emailbox']
            for item in email_json:
                if item in email_needshow_para:
                    if item == 'redipients':
                        title = st.multiselect('%s(%s): ' % (item, 'common'),
                                               email_json['emails'],
                                               email_json[item],
                                               disabled=self.disable_write)
                        if read_json["emailbox"][item] != title:
                            read_json["emailbox"][item] = title
                            self.common_para_change = True
                    else:
                        pass

            if self.disable_write == False and self.common_para_change == True:
                f_d = open('/etc/marktrade/config.json', 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def update_market_para(self):
        st.header('%s' % ("market:"))

        market_needshow_para = ['User', 'LogInTimeList', 'TimingPush', 'SubscribeMarketDataFrom']
        try:
            with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
                read_json = json.load(fp)
            fp.close()

            self.market_para_change = False
            market_json = read_json['market']
            for item in market_json:
                if item in market_needshow_para:
                    if item == 'SubscribeMarketDataFrom':
                        title = st.selectbox('SubscribeMarketDataFrom: ', ['local', 'strategy', 'api'], \
                            ['local', 'strategy', 'api'].index(read_json["market"][item]), key='datafrom', disabled=self.disable_write)
                        read_json["market"][item] = title
                    elif item == 'TimingPush':
                        action_list = ['push', 'nopush']
                        title = st.selectbox('%s(%s): ' % (item, 'market'),
                                             action_list,
                                             action_list.index(market_json[item]),
                                             key='timeing_push',
                                             disabled=self.disable_write)
                        if read_json["market"][item] != title:
                            read_json["market"][item] = title
                            self.market_para_change = True
                    elif item == 'User':
                        user_list = [item for item in read_json['users'].keys()]
                        api_users = self.get_users(user_list, read_json['common']['ApiType'])
                        now_user = read_json['market']['User'][0]
                        if now_user in api_users:
                            title = st.selectbox('%s(%s): ' % (item, 'market'),
                                                 api_users,
                                                 api_users.index(now_user),
                                                 key='marketuserid',
                                                 disabled=self.disable_write)
                        else:
                            title = st.selectbox('%s(%s): ' % (item, 'market'),
                                                 api_users,
                                                 0,
                                                 key='marketuserid',
                                                 disabled=self.disable_write)
                        if read_json["market"][item] != [title]:
                            read_json["market"][item] = [title]
                            self.market_para_change = True
                    else:
                        title = st.text_input('%s(%s): ' % (item, 'market'), market_json[item], disabled=self.disable_write)
                        if read_json["market"][item] != title:
                            read_json["market"][item] = title
                            self.market_para_change = True

            if self.disable_write == False and self.market_para_change == True:
                f_d = open('/etc/marktrade/config.json', 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def update_trader_para(self):
        st.header('%s' % ("trader:"))

        trader_needshow_para = ['User', 'LogInTimeList', 'SendOrderEmail', 'AccountAssignMode']
        try:
            with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
                read_json = json.load(fp)
            fp.close()

            self.trader_para_change = False
            trader_json = read_json['trader']
            for item in trader_json:
                if item in trader_needshow_para:
                    if item == 'User':
                        user_list = [item for item in read_json['users'].keys()]
                        api_users = self.get_users(user_list, read_json['common']['ApiType'])
                        now_user = read_json['trader']['User']
                        d = [False for c in now_user if c not in api_users]
                        if d:
                            title = st.multiselect('%s(%s): ' % (item, 'trader'), api_users, [], disabled=self.disable_write)
                        else:
                            title = st.multiselect('%s(%s): ' % (item, 'trader'), api_users, now_user, disabled=self.disable_write)
                        if read_json["trader"][item] != title:
                            read_json["trader"][item] = title
                            self.trader_para_change = True
                    elif item == 'SendOrderEmail':
                        action_list = ['send', 'nosend']
                        title = st.selectbox('%s(%s): ' % (item, 'trader'),
                                             action_list,
                                             action_list.index(trader_json[item]),
                                             key='send_email',
                                             disabled=self.disable_write)
                        if read_json["trader"][item] != title:
                            read_json["trader"][item] = title
                            self.trader_para_change = True
                    elif item == 'AccountAssignMode':
                        assign_mode = ['cycle', 'share']
                        title = st.selectbox('%s(%s): ' % (item, 'trader'),
                                             assign_mode,
                                             assign_mode.index(trader_json[item]),
                                             key='assign_mode',
                                             disabled=self.disable_write)
                        if read_json["trader"][item] != title:
                            read_json["trader"][item] = title
                            self.trader_para_change = True
                    else:
                        title = st.text_input('%s(%s): ' % (item, 'trader'), trader_json[item], disabled=self.disable_write)
                        if read_json["trader"][item] != title:
                            read_json["trader"][item] = title
                            self.trader_para_change = True

            if self.disable_write == False and self.trader_para_change == True:
                f_d = open('/etc/marktrade/config.json', 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def online_update_para(self):
        if st.button('update para'):
            if 'para update' in st.session_state and st.session_state['para update'] == True:
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

            if 'para update' in st.session_state:
                if st.session_state['para update'] == False:
                    st.session_state['para update'] = True
                else:
                    st.session_state['para update'] = False
            else:
                st.session_state['para update'] = True

    def check_parameter_writtable(self):
        process = ['market', 'trader']
        for item in process:
            process_id = self.checkprocess(item)
            if isinstance(process_id, int):
                if 'para update' in st.session_state and st.session_state['para update'] == True:
                    self.disable_write = False
                    return
                else:
                    self.disable_write = True
                    return
        self.disable_write = False
        return

    def get_users(self, users, key):
        if key == 'ctp':
            return [item for item in users if 'simnow' in item or 'citic' in item or 'zhonghui' in item]
        elif key == 'xtp':
            return [item for item in users if 'xtp' in item]
        elif key == 'btp':
            return [item for item in users if 'btp' in item]
        elif key == 'otp':
            return [item for item in users if 'otp' in item]
        elif key == 'ftp':
            return [item for item in users if 'ftp' in item]

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


parameter_page = parameter()
