import os
import time

import psutil
import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig


class setting():

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
        if st.button('clear process'):
            self.clear_process()

        if st.button('clear record'):
            self.clear_record()

        if st.button('clear log'):
            self.clear_log()

        if st.button('clear coredump'):
            self.clear_coredump()

        if st.button('clear tick'):
            self.clear_tick()

    def clear_process(self, ):
        id = self.checkprocess("market")
        if isinstance(id, int):
            os.system("kill -9 %d" % (id))
            time.sleep(1)

        id = self.checkprocess("trader")
        if isinstance(id, int):
            os.system("kill -9 %d" % (id))
            time.sleep(1)

    def clear_record(self):
        data_path = '%s/data/' % (os.environ.get('HOME'))

        if os.path.exists(data_path):
            for root, dirs, files in os.walk(data_path):
                for f in files:
                    if f.split('.')[-1] == 'json' or f.split('.')[-1] == 'db':
                        f_path = os.path.join(root, f)
                        os.system('rm -f %s' % (f_path))

        st.info('rm -rf %s' % (data_path))

    def clear_log(self):
        log_path = '%s/log/' % (os.environ.get('HOME'))

        if os.path.exists(log_path):
            for root, dirs, files in os.walk(log_path):
                for f in files:
                    if f.split('.')[-1] == 'log':
                        f_path = os.path.join(root, f)
                        os.system('rm -f %s' % (f_path))

        st.info('rm -rf %s' % (log_path))

    def clear_coredump(self):
        coredump_path = '%s/.local/coredump' % (os.environ.get('HOME'))

        if os.path.exists(coredump_path):
            st.info('rm -f %s/*' % (coredump_path))
            os.system('rm -f %s/*' % (coredump_path))

    def clear_tick(self):
        tick_path = jsonconfig.get_config('market', 'HistoryTickPath')

        if os.path.exists(tick_path):
            st.info('rm -f %s/*' % (tick_path))
            os.system('rm -f %s/*' % (tick_path))


setting_page = setting()
