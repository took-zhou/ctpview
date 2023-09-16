import base64
import os
import sqlite3
import time

import psutil
import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig


class control:

    def __init__(self):
        pass

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

    def update(self):
        self.control_process('market')

        self.control_process('trader')

    def control_process(self, _name):
        '''
        只针对market和trader
        '''
        if not os.path.exists(jsonconfig.get_config(_name, 'LogPath')):
            os.makedirs(jsonconfig.get_config(_name, 'LogPath'))

        # 进程控制
        st.header('%s' % ("%s:" % (_name)))
        contain = st.container()
        col1, col2 = contain.columns(2)
        process_id = self.checkprocess(_name)
        if isinstance(process_id, int):
            st.session_state['%s_id' % (_name)] = process_id
            process_status = 'start'
        else:
            process_status = 'not start'

        if col1.button('start', key='%s1' % (_name)) and not (isinstance(process_id, int)):
            command = 'nohup %s </dev/null 1>/dev/null 2> %s/log/%s/%s_exception.log &' % (_name, os.environ.get('HOME'), _name, _name)
            os.system(command)
            time.sleep(0.1)

        if col2.button('stop', key='%s2' % (_name)) and isinstance(process_id, int):
            os.system('kill -9 %d' % (process_id))
            time.sleep(0.1)

        login_logout = "logout"
        try:
            if _name == "market":
                username = jsonconfig.get_config('market', 'User')[0]
                control_db_path = '%s/%s/control.db' % (jsonconfig.get_config('market', 'ControlParaFilePath'), username)
            elif _name == "trader":
                control_db_path = '%s/control.db' % (jsonconfig.get_config('trader', 'ControlParaFilePath'))
            conn = sqlite3.connect(control_db_path)
            try:
                command = 'select login_state from service_info;'
                if conn.execute(command).fetchall()[0][0] == 1:
                    login_logout = "login"
            except:
                # error_msg = traceback.format_exc()
                # print(error_msg)
                pass
            conn.close()
        except:
            pass

        coredump_status = 'normal'
        core_dump_list = os.listdir('/home/tsaodai/.local/coredump')
        for item in core_dump_list:
            if '%s_id' % (_name) in st.session_state and str(st.session_state['%s_id' % (_name)]) in item and _name in item:
                coredump_status = 'coredump'
                break

        if process_status == 'start':
            st.write('%s status: `start, %s`' % (_name, login_logout))
        else:
            st.write('%s status: `no start, %s`' % (_name, coredump_status))


control_page = control()
