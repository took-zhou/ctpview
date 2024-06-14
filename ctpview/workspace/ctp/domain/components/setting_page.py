import os
import time
from datetime import date

import psutil
import streamlit as st

from ctpview.workspace.common.file_util import jsonconfig
from ctpview.workspace.ctp.domain.components.control_page import control


class setting():

    def __init__(self):
        self.history_record_path = '%s/history_record/' % (os.environ.get('HOME'))

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

        if st.button('uninstall'):
            self.uninstall_marktrade()

        if not os.path.exists(self.history_record_path):
            os.makedirs(self.history_record_path)

        if st.button('package'):
            self.pack_history_record()
        st.write('____')

        uploaded_file = st.file_uploader("Choose a file", key='setting1')
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            fw = open("%s/%s" % (self.history_record_path, uploaded_file.name), "wb")
            fw.write(bytes_data)
            fw.close()

        package_list = os.listdir(self.history_record_path)
        package = st.selectbox('Package', package_list)

        binary_file = '%s/%s' % (self.history_record_path, package)
        if os.path.exists(binary_file):
            with open(binary_file, "rb") as file:
                st.download_button(label="download", data=file, file_name=package, mime="application/octet-stream")

            if st.button('distribute', key='strategy8'):
                self.distribute_history_record(binary_file)

    def clear_process(self):
        id = self.checkprocess("market")
        if isinstance(id, int):
            os.system("kill -2 %d" % (id))
            time.sleep(1)

        id = self.checkprocess("trader")
        if isinstance(id, int):
            os.system("kill -2 %d" % (id))
            time.sleep(1)

        st.info('clear process ok')

    def clear_record(self):
        data_path = '%s/data/' % (os.environ.get('HOME'))

        if os.path.exists(data_path):
            for root, dirs, files in os.walk(data_path):
                for f in files:
                    if f.split('.')[-1] == 'json' or f.split('.')[-1] == 'db':
                        f_path = os.path.join(root, f)
                        os.system('rm -f %s' % (f_path))

        st.info('clear record ok')

    def clear_log(self):
        log_path = '%s/log/' % (os.environ.get('HOME'))

        if os.path.exists(log_path):
            for root, dirs, files in os.walk(log_path):
                for f in files:
                    if f.split('.')[-1] == 'log':
                        f_path = os.path.join(root, f)
                        os.system('rm -f %s' % (f_path))

        st.info('clear log ok')

    def clear_coredump(self):
        coredump_path = '%s/.local/coredump' % (os.environ.get('HOME'))

        if os.path.exists(coredump_path):
            os.system('rm -f %s/*' % (coredump_path))

        st.info('clear coredump ok')

    def clear_tick(self):
        tick_path = jsonconfig.get_config('market', 'HistoryTickPath')

        if os.path.exists(tick_path):
            os.system('rm -f %s/*' % (tick_path))

        st.info('clear tick ok')

    def uninstall_marktrade(self):
        command = 'sudo apt remove -y marktrade'
        os.system(command)

    def pack_history_record(self):
        file_name = 'history_record_%s.tar.gz' % (date.today())
        binary_file = '%s/%s' % (self.history_record_path, file_name)
        if os.path.exists(binary_file):
            os.remove(binary_file)

        user_name = jsonconfig.get_config('market', 'User')[0]
        trader_db_path = '%s/data/trader/control.db' % (os.environ.get('HOME'))
        market_path = '%s/data/market/%s' % (os.environ.get('HOME'), user_name)
        config_path = '/etc/marktrade/config.json'
        command = 'tar -czvf %s %s %s %s' % (binary_file, trader_db_path, market_path, config_path)
        os.system(command)

    def distribute_history_record(self, file):
        command = 'tar zxf %s -C /' % (file)
        os.system(command)
