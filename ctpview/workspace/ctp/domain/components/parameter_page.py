import json
import os

import psutil
import streamlit as st


class parameter:

    def __init__(self):
        self.disable_write = False

    def update(self):
        self.check_parameter_writtable()

        self.update_common_para()

        self.update_market_para()

        self.update_trader_para()

        st.write('____')

        self.online_update_para()

    def update_common_para(self):
        st.header('%s' % ("common:"))

        common_needshow_para = ['ApiType', 'RunMode']
        email_needshow_para = ['redipients']
        try:
            with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
                read_json = json.load(fp)

            common_json = read_json['common']
            for item in common_json:
                if item in common_needshow_para:
                    if item == 'ApiType':
                        title = st.selectbox('%s(%s): ' % (item, 'common'), ['ctp', 'xtp', 'btp'], ['ctp', 'xtp',
                                                                                                    'btp'].index(common_json[item]),
                                             key='apitype',
                                             disabled=self.disable_write)
                        read_json["common"][item] = title
                    elif item == 'RunMode':
                        title = st.selectbox('%s(%s): ' % (item, 'common'), ['realtime', 'fastback'], ['realtime',
                                                                                                       'fastback'].index(common_json[item]),
                                             key='runmode',
                                             disabled=self.disable_write)
                        read_json["common"][item] = title
                    else:
                        title = st.text_input('%s(%s): ' % (item, 'common'), common_json[item], disabled=self.disable_write)
                        read_json["common"][item] = title

            email_json = read_json['emailbox']
            for item in email_json:
                if item in email_needshow_para:
                    if item == 'redipients':
                        title = st.multiselect('%s(%s): ' % (item, 'common'),
                                               email_json['emails'],
                                               email_json[item],
                                               disabled=self.disable_write)
                        read_json["emailbox"][item] = title
                    else:
                        pass
            fp.close()
            if self.disable_write == False:
                f_d = open('/etc/marktrade/config.json', 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def update_market_para(self):
        st.header('%s' % ("market:"))

        market_needshow_para = ['User', 'LogInTimeList', 'SubscribeMarketDataFrom']
        try:
            with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
                read_json = json.load(fp)

            market_json = read_json['market']
            for item in market_json:
                if item in market_needshow_para:
                    if item == 'SubscribeMarketDataFrom':
                        title = st.selectbox('SubscribeMarketDataFrom: ', ['local', 'strategy', 'api'], \
                            ['local', 'strategy', 'api'].index(read_json["market"][item]), key='datafrom', disabled=self.disable_write)
                        read_json["market"][item] = title
                    elif item == 'User':
                        user_list = [item for item in read_json['users'].keys()]
                        api_users = self.get_users(user_list, read_json['common']['ApiType'])
                        now_user = read_json['market']['User'][0]
                        if now_user in api_users:
                            user_id = st.selectbox('%s(%s): ' % (item, 'market'),
                                                   api_users,
                                                   api_users.index(now_user),
                                                   key='marketuserid',
                                                   disabled=self.disable_write)
                        else:
                            user_id = st.selectbox('%s(%s): ' % (item, 'market'),
                                                   api_users,
                                                   0,
                                                   key='marketuserid',
                                                   disabled=self.disable_write)
                        read_json['market']['User'] = [user_id]
                    else:
                        title = st.text_input('%s(%s): ' % (item, 'market'), market_json[item], disabled=self.disable_write)
                        read_json["market"][item] = title
            fp.close()
            if self.disable_write == False:
                f_d = open('/etc/marktrade/config.json', 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def update_trader_para(self):
        order_rsp_mode = ['success', 'waiting', 'part_success', 'no_money', 'no_open']
        trader_needshow_para = ['User', 'LogInTimeList', 'OrderRspMode']
        st.header('%s' % ("trader:"))
        try:
            with open('/etc/marktrade/config.json', 'r', encoding='utf8') as fp:
                read_json = json.load(fp)

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
                        read_json['trader']['User'] = title
                    elif item == 'OrderRspMode':
                        title = st.selectbox('%s(%s): ' % (item, 'trader'),
                                             order_rsp_mode,
                                             order_rsp_mode.index(trader_json[item]),
                                             key='order_rsp',
                                             disabled=self.disable_write)
                        read_json["trader"][item] = title
                    else:
                        title = st.text_input('%s(%s): ' % (item, 'trader'), trader_json[item], disabled=self.disable_write)
                        read_json["trader"][item] = title

            fp.close()
            if self.disable_write == False:
                f_d = open('/etc/marktrade/config.json', 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def online_update_para(self):
        if st.button('update para'):
            if 'para update' in st.session_state and st.session_state['para update'] == True:
                pass

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
