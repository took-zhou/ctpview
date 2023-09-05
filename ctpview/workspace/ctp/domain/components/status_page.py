import socket
import sqlite3

import psutil
import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig


class status():

    def __init__(self):
        pass

    def getprocessid(self, processname):
        # --获取进程信息--
        ret = []
        pl = psutil.pids()  #所有的进程列出来

        for pid in pl:
            try:
                for item in processname:
                    if item in psutil.Process(pid).name():
                        ret.append(pid)
            except:
                continue
        return ret

    def update(self):
        process_list = self.getprocessid(['proxy', 'market', 'trader', 'streamlit'])
        for item in process_list:
            name = psutil.Process(item).name()
            cpu_percent = psutil.Process(item).cpu_percent(interval=1)
            memory_percent = psutil.Process(item).memory_percent()
            st.write('{}: `start` cup: `{:.2}` memory: `{:.2}`'.format(name, cpu_percent, memory_percent))

        count = 0
        for item in psutil.cpu_percent(interval=1, percpu=True):
            name = 'core%d' % (count)
            st.write('{} utilization rate: `{:.2}`'.format(name, item))
            count = count + 1

        memory_msg = psutil.virtual_memory()
        st.write('mem total: `{}` mem used: `{}` mem free: `{}`'.format(int(memory_msg.total/1024/1024), \
            int(memory_msg.used/1024/1024), int(memory_msg.free/1024/2014)))

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        st.write('local ip: `%s`' % (ip))

        market_compile_time = '--'
        trader_compile_time = '--'
        try:
            username = jsonconfig.get_config('market', 'User')[0]
            control_db_path = '%s/%s/control.db' % (jsonconfig.get_config('market', 'ControlParaFilePath'), username)
            conn = sqlite3.connect(control_db_path)
            try:
                command = 'select compile_time from service_info;'
                market_compile_time = conn.execute(command).fetchall()[0][0]
            except:
                # error_msg = traceback.format_exc()
                # print(error_msg)
                pass
            conn.close()
            control_db_path = '%s/control.db' % (jsonconfig.get_config('trader', 'ControlParaFilePath'))
            conn = sqlite3.connect(control_db_path)
            try:
                command = 'select compile_time from service_info;'
                trader_compile_time = conn.execute(command).fetchall()[0][0]
            except:
                # error_msg = traceback.format_exc()
                # print(error_msg)
                pass
            conn.close()
        except:
            pass

        st.write('market compile time: `%s`' % (market_compile_time))
        st.write('trader compile time: `%s`' % (trader_compile_time))

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

        st.write('subscribe instrument number from strategy: `%d`' % (len(subscribe_list)))
        st.write(subscribe_list)


status_page = status()
