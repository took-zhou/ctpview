import os
import time

import psutil
import streamlit as st


class update():

    def __init__(self):
        self.package_list = ["tickmine", "ticknature", "ctpview"]
        self.apt_source_dict = {}
        self.apt_source_dict['http://192.168.0.106:8095/debian'] = 'deb [trusted=yes] http://192.168.0.106:8095/debian/ ./\n'
        self.apt_source_dict['http://aptserver.tsaodai.com/debian'] = 'deb [trusted=yes] http://aptserver.tsaodai.com/debian/ ./\n'
        self.pip_source_dict = {}
        self.pip_source_dict['http://192.168.0.106:3141/root/temp'] = [
            '[global]\n', 'trusted-host = 192.168.0.106\n', 'index-url = http://192.168.0.106:3141/root/temp\n'
        ]
        self.pip_source_dict['http://192.168.0.106:3141/root/dev'] = [
            '[global]\n', 'trusted-host = 192.168.0.106\n', 'index-url = http://192.168.0.106:3141/root/dev\n'
        ]
        self.pip_source_dict['http://devpi.tsaodai.com/root/temp'] = [
            '[global]\n', 'trusted-host = devpi.tsaodai.com\n', 'index-url = http://devpi.tsaodai.com/root/temp\n'
        ]
        self.pip_source_dict['http://devpi.tsaodai.com/root/dev'] = [
            '[global]\n', 'trusted-host = devpi.tsaodai.com\n', 'index-url = http://devpi.tsaodai.com/root/dev\n'
        ]
        self.apt_source = 'http://192.168.0.106:8095/debian'
        self.pip_source = 'http://192.168.0.106:3141/root/dev'

    def update(self):
        self.read_para()

        self.update_apt_link()
        self.update_market_trader()

        st.write('____')

        self.update_pypi_link()
        self.update_package_list()

        st.write('____')

        self.write_para()

    def read_para(self):
        try:
            with open('/etc/apt/sources.list', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if '[trusted=yes]' in line:
                        for item in self.apt_source_dict:
                            if self.apt_source_dict[item] == line:
                                self.apt_source = item
            f.close()

            with open('%s/.pip/pip.conf' % (os.environ.get('HOME')), 'r') as f:
                lines = f.readlines()
                for item in self.pip_source_dict:
                    if self.pip_source_dict[item] == lines:
                        self.pip_source = item
        except:
            pass

    def write_para(self):
        if st.button("update version"):
            self.write_para_click()
            st.info('update version ok')

    def write_para_click(self):
        os.system('sudo chmod 777 /etc/apt/sources.list')

        origin_lines = []
        with open('/etc/apt/sources.list', 'r') as f:
            lines = f.readlines()
            origin_lines = lines.copy()
            for line in lines:
                if '[trusted=yes]' in line:
                    origin_lines.remove(line)
            f.close()

        origin_lines.append(self.apt_source_dict[self.apt_source])
        with open('/etc/apt/sources.list', 'w') as f:
            f.writelines(origin_lines)
            f.close()

        if not os.path.exists('%s/.pip/pip.conf' % (os.environ.get('HOME'))):
            command = 'mkdir %s/.pip/' % (os.environ.get('HOME'))
            os.system(command)
            command = 'touch %s/.pip/pip.conf' % (os.environ.get('HOME'))
            os.system(command)

        with open('%s/.pip/pip.conf' % (os.environ.get('HOME')), 'w') as f:
            f.writelines(self.pip_source_dict[self.pip_source])
            f.close()

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
                    st.session_state['%s_installed_version'%(key_values[0])] = key_values[1]
                    st.session_state['%s_newest_version'%(key_values[0])] = newest_version
                    break

    def update_apt_link(self):
        apt_list = [item for item in self.apt_source_dict]
        title = st.selectbox('select apt', apt_list, apt_list.index(self.apt_source))
        self.apt_source = title

    def update_pypi_link(self):
        pypi_list = [item for item in self.pip_source_dict]
        title = st.selectbox('select pypi', pypi_list, pypi_list.index(self.pip_source))
        self.pip_source = title

    def update_market_trader(self):
        contain = st.container()
        col1, col2 = contain.columns(2)
        if 'marktrade_installed_version' in st.session_state and 'marktrade_newest_version' in st.session_state:
            col1.write('marktrade`%s --> %s`' % (st.session_state['marktrade_installed_version'], st.session_state['marktrade_newest_version']))
        else:
            col1.write('marktrade`? --> ?`')
        if col2.button('update marktrade'):
            self.update_single_deb('marktrade', st.session_state['marktrade_newest_version'])
            os.system("sudo ldconfig")

    def update_package_list(self):
        for package in self.package_list:
            contain = st.container()
            col1, col2 = contain.columns(2)
            if '%s_installed_version'%(package) in st.session_state and '%s_newest_version'%(package) in st.session_state:
                col1.write('%s`%s --> %s`' % (package, st.session_state['%s_installed_version'%(package)], st.session_state['%s_newest_version'%(package)]))
            else:
                col1.write('%s`? --> ?`'%(package))
        
            if col2.button('update %s' % package):
                self.update_single_pip(package, st.session_state['%s_newest_version'%(package)])

    def find_newest_version_pip(self, item):
        newest_version = ''
        if os.path.exists('%s/.pip/pip.conf' % (os.environ.get('HOME'))):
            command = 'pip install --no-deps  %s== 2>%s/out.txt' % (item, os.environ.get('HOME'))
        else:
            command = 'pip install --no-deps --index-url http://devpi.tsaodai.com/root/dev %s== --trusted-host devpi.tsaodai.com 2>%s/out.txt'% \
            (item, os.environ.get('HOME'))
        os.system(command)
        with open('%s/out.txt' % (os.environ.get('HOME')), 'r') as f:
            line = f.readline()
            newest_version = line.split('from versions: ')[-1].split(')')[0].split(',')[-1].replace(' ', '')
            f.close()
            os.system('rm %s/out.txt' % (os.environ.get('HOME')))
        return newest_version

    def update_single_pip(self, _module, _version=''):
        command = 'pip uninstall -y %s' % (_module)
        os.system(command)
        # 安装
        if os.path.exists('%s/.pip/pip.conf' % (os.environ.get('HOME'))):
            command = 'pip install --no-deps  %s' % (_module)
        else:
            command = 'pip install --no-deps --index-url http://devpi.tsaodai.com/root/dev %s\
                    --trusted-host devpi.tsaodai.com' % (_module)
        os.system(command)
        # 安装依赖
        command = 'pip install %s' % (_module)
        os.system(command)
        st.info('update %s ok' % (_module))

        if _module == 'ctpview':
            # 重启streamlit
            ui_id = self.checkprocess('streamlit')
            import ctpview
            command = 'nohup kill -9 %d; nohup /%s/.local/bin/streamlit run %s/workspace/ctp/domain/presentation.py >> \
                %s/.streamlit/output.log 2>&1 &' % (ui_id, os.environ.get('HOME'), ctpview.__path__[0], os.environ.get('HOME'))
            os.system(command)

    def find_newest_version_deb(self, item):
        os.system('sudo chmod 777 /etc/apt/sources.list')
        origin_lines = []
        after_lines = []
        newest_version = ''
        with open('/etc/apt/sources.list', 'r') as f:
            lines = f.readlines()
            origin_lines = lines.copy()
            for line in lines:
                if '[trusted=yes]' in line:
                    after_lines.append(line)
            f.close()

        with open('/etc/apt/sources.list', 'w') as f:
            f.writelines(after_lines)
            f.close()

        os.system('sudo apt update')

        temp_items = os.popen('sudo apt-cache madison %s' % (item))
        lines_items = temp_items.readlines()
        newest_version = lines_items[0].split('|')[1].strip(' ')

        with open('/etc/apt/sources.list', 'w') as f:
            f.writelines(origin_lines)
            f.close()

        return newest_version

    def update_single_deb(self, _module, _version=''):
        command = 'sudo apt install -y %s=%s' % (_module, _version)
        os.system(command)
        st.info('update marktrade ok')

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


update_page = update()
