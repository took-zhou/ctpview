import os

import psutil
import streamlit as st


class update():

    def __init__(self):
        self.package_list = ["tickmine", "ticknature", "ctpview"]

    def update(self):
        self.update_market_trader()

        st.write('____')

        self.update_package_list()

        st.write('____')

        self.update_version()

    def update_version(self):
        if st.button("update version"):
            with st.status("update version...") as st_status:
                self.update_version_click()
                st_status.update(label="update version complete", state="complete")

    def update_version_click(self):
        temp_items = os.popen('sudo apt-cache show %s' % ('marktrade'))
        lines_items = temp_items.readlines()
        for item in lines_items:
            if 'Version' in item:
                st.session_state['marktrade_installed_version'] = item.split(":")[-1].strip(" ")
        st.session_state['marktrade_newest_version'] = self.find_newest_version_deb('marktrade')

        for package in self.package_list:
            newest_version = self.find_newest_version_pip(package)
            temp_items = os.popen('pip list')
            lines_items = temp_items.readlines()
            for item in lines_items:
                key_values = [value for value in item.split(' ') if value != '']
                if key_values[0] == package:
                    st.session_state['%s_installed_version' % (key_values[0])] = key_values[1]
                    st.session_state['%s_newest_version' % (key_values[0])] = newest_version
                    break

    def update_market_trader(self):
        contain = st.container()
        col1, col2 = contain.columns(2)
        if 'marktrade_installed_version' in st.session_state and 'marktrade_newest_version' in st.session_state:
            col1.write('marktrade`%s --> %s`' %
                       (st.session_state['marktrade_installed_version'], st.session_state['marktrade_newest_version']))
        else:
            col1.write('marktrade`? --> ?`')
        if col2.button('update marktrade'):
            with st.status("update marktrade...") as st_status:
                self.update_single_deb('marktrade', st.session_state['marktrade_newest_version'])
                os.system("sudo ldconfig")
                st_status.update(label="update marktrade complete", state="complete")

    def update_package_list(self):
        for package in self.package_list:
            contain = st.container()
            col1, col2 = contain.columns(2)
            if '%s_installed_version' % (package) in st.session_state and '%s_newest_version' % (package) in st.session_state:
                col1.write('%s`%s --> %s`' % (package, st.session_state['%s_installed_version' %
                                                                        (package)], st.session_state['%s_newest_version' % (package)]))
            else:
                col1.write('%s`? --> ?`' % (package))

            if col2.button('update %s' % package):
                with st.status("update %s..." % package) as st_status:
                    self.update_single_pip(package, st.session_state['%s_newest_version' % (package)])
                    st_status.update(label="update %s complete" % package, state="complete")

    def find_newest_version_pip(self, item):
        newest_version = ''
        command = 'pip install --no-deps --index-url https://devpi.tsaodai.com/root/dev %s== --trusted-host devpi.tsaodai.com 2>%s/out.txt' % (
            item, os.environ.get('HOME'))
        os.system(command)
        with open('%s/out.txt' % (os.environ.get('HOME')), 'r') as f:
            line = f.readline()
            newest_version = line.split('from versions: ')[-1].split(')')[0].split(',')[-1].replace(' ', '')
            f.close()
            os.system('rm %s/out.txt' % (os.environ.get('HOME')))
        return newest_version

    def find_newest_version_deb(self, item):
        os.system('sudo apt update')
        temp_items = os.popen('sudo apt-cache madison %s' % (item))
        lines_items = temp_items.readlines()
        newest_version = lines_items[0].split('|')[1].strip(' ')
        return newest_version

    def update_single_pip(self, _module, _version=''):
        command = 'pip uninstall -y %s' % (_module)
        os.system(command)

        command = 'pip install --no-deps --index-url https://devpi.tsaodai.com/root/dev %s --trusted-host devpi.tsaodai.com' % (_module)
        os.system(command)

        command = 'pip install %s' % (_module)
        os.system(command)

        if _module == 'ctpview':
            ui_id = self.checkprocess('streamlit')
            import ctpview
            command = 'nohup kill -9 %d && streamlit run %s/workspace/ctp/domain/presentation.py >> %s/.streamlit/output.log 2>&1 &' % (
                ui_id, ctpview.__path__[0], os.environ.get('HOME'))
            os.system(command)

    def update_single_deb(self, _module, _version=''):
        command = 'sudo apt install -y %s=%s' % (_module, _version)
        os.system(command)

    def checkprocess(self, processname):
        pl = psutil.pids()

        for pid in pl:
            try:
                if psutil.Process(pid).name() == processname:
                    return pid
            except:
                continue

        return ''
