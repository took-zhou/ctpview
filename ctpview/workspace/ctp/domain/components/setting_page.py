import streamlit as st
import time
import os

class setting():
    def __init__(self):
        pass

    def update(self):
        if st.button('clear process'):
            self.clear_process()

        if st.button('clear record'):
            self.clear_record()

        if st.button('clear log'):
            self.clear_log()

    def clear_process(self,):
        id = self.checkprocess("proxy")
        if isinstance(id, int):
            os.system("kill -9 %d"%(self.checkprocess("proxy")))
            time.sleep(1)
        id = self.checkprocess("proxy")
        if isinstance(self.checkprocess("market"), int):
            os.system("kill -9 %d"%(self.checkprocess("market")))
            time.sleep(1)
        id = self.checkprocess("proxy")
        if isinstance(self.checkprocess("trader"), int):
            os.system("kill -9 %d"%(self.checkprocess("trader")))

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
