import streamlit as st
import json
import os
import psutil

class parameter:
    def __init__(self):
        self.disable_write = False

    def update(self):
        self.check_parameter_writtable()

        self.update_common_para()

        self.update_market_para()

        self.update_trader_para()

    def update_common_para(self):
        st.header('%s'%("common:"))

        common_needshow_para = ['PrintNetworkDelay']
        email_needshow_para = ['redipients']
        email_receivers = ['zhoufan@cdsslh.com', 'cuiwenhong@cdsslh.com']
        try:
            with open('%s/config/config.json'%(os.environ.get('HOME')), 'r', encoding='utf8') as fp:
                read_json = json.load(fp)

            user_list = [item for item in read_json['users'].keys()]
            now_user = read_json['common']['user']
            user_id = st.selectbox('SelectUser: ', user_list, user_list.index(now_user), key='userid')
            read_json['common']['user'] = user_id

            common_json = read_json['common']
            for item in common_json:
                if item in common_needshow_para:
                    if item == 'PrintNetworkDelay':
                        title = st.selectbox('IsPrintNetworkDelay ', ['yes', 'no'], ['yes', 'no'].index(common_json[item]), key='isprint')
                        read_json["common"][item] = title
                    else:
                        title = st.text_input('%s(%s): '%(item, 'common'), common_json[item])
                        read_json["common"][item] = title

            email_json = read_json['emailbox']
            for item in email_json:
                if item in email_needshow_para:
                    if item  == 'redipients':
                        title = st.multiselect('%s(%s): '%(item, 'common'), email_receivers, email_json[item])
                        read_json["emailbox"][item] = title
                    else:
                        pass
            fp.close()
            if self.disable_write == False:
                f_d = open('%s/config/config.json'%(os.environ.get('HOME')), 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def update_market_para(self):
        st.header('%s'%("market:"))

        market_needshow_para = ['LoginMode', 'LogInTimeList', 'SubscribeMarketDataFrom']
        try:
            with open('%s/config/config.json'%(os.environ.get('HOME')), 'r', encoding='utf8') as fp:
                read_json = json.load(fp)

            market_json = read_json['market']
            for item in market_json:
                if item in market_needshow_para:
                    if item == 'LoginMode':
                        title = st.selectbox('LoginMode: ', ['normal', '7x24'], key='market')
                        read_json["market"][item] = title
                    elif item == 'SubscribeMarketDataFrom':
                        title = st.selectbox('SubscribeMarketDataFrom: ', ['local', 'strategy', 'market', 'trader'], \
                            ['local', 'strategy', 'market', 'trader'].index(read_json["market"][item]), key='datafrom')
                        read_json["market"][item] = title
                    else:
                        title = st.text_input('%s(%s): '%(item, 'market'), market_json[item])
                        read_json["market"][item] = title
            fp.close()
            if self.disable_write == False:
                f_d = open('%s/config/config.json'%(os.environ.get('HOME')), 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def update_trader_para(self):
        trader_needshow_para = ['LoginMode', 'LogInTimeList']
        st.header('%s'%("trader:"))
        try:
            with open('%s/config/config.json'%(os.environ.get('HOME')), 'r', encoding='utf8') as fp:
                read_json = json.load(fp)

            trader_json = read_json['trader']
            for item in trader_json:
                if item in trader_needshow_para:
                    if item == 'LoginMode':
                        title = st.selectbox('LoginMode: ', ['normal', '7x24'], key='trader')
                        read_json["trader"][item] = title
                    else:
                        title = st.text_input('%s(%s): '%(item, 'trader'), trader_json[item])
                        read_json["trader"][item] = title
            fp.close()
            if self.disable_write == False:
                f_d = open('%s/config/config.json'%(os.environ.get('HOME')), 'w', encoding="utf-8")
                json.dump(read_json, f_d, indent=4)
                f_d.close()
        except:
            pass

    def check_parameter_writtable(self):
        process = ['market', 'trader']
        for item in process:
            process_id = self.checkprocess(item)
            if isinstance(process_id, int):
                self.disable_write = True
                return

        self.disable_write = False
        return

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
