import streamlit as st
import time
import os
import psutil

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

    def clear_process(self,):
        id = self.checkprocess("market")
        if isinstance(id, int):
            os.system("kill -9 %d"%(id))
            time.sleep(1)

        id = self.checkprocess("trader")
        if isinstance(id, int):
            os.system("kill -9 %d"%(id))
            time.sleep(1)

    def clear_record(self):
        data_path = '%s/data/'%(os.environ.get('HOME'))

        if os.path.exists(data_path):
            st.info('rm -rf %s'%(data_path))
            os.system('rm -rf %s'%(data_path))

    def clear_log(self):
        log_path = '%s/log/'%(os.environ.get('HOME'))

        if os.path.exists(log_path):
            st.info('rm -rf %s'%(log_path))
            os.system('rm -rf %s'%(log_path))

setting_page = setting()
