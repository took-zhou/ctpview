import configparser
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

    def update_market_trader(self):
        pack_name = ''
        temp_items = os.popen('sudo apt-cache show %s' % ('marktrade'))
        lines_items = temp_items.readlines()
        for item in lines_items:
            if 'Version' in item:
                pack_name = item.split(":")[-1].strip(" ")

        newest_name = self.find_newest_version_deb('marktrade')

        contain = st.container()
        col1, col2 = contain.columns(2)
        col1.write('marktrade: %s --> %s' % (pack_name, newest_name))
        if col2.button('update', key='update2'):
            self.update_single_deb('marktrade', newest_name)
            os.system("sudo ldconfig")

    def update_package_list(self):
        for package in self.package_list:
            newest_version = self.find_newest_version_pip(package)

            temp_items = os.popen('pip list')
            lines_items = temp_items.readlines()
            for item in lines_items:
                key_values = [value for value in item.split(' ') if value != '']
                if key_values[0] == package:
                    contain = st.container()
                    col1, col2 = contain.columns(2)
                    col1.write('%s: %s --> %s' % (key_values[0], key_values[1], newest_version))
                    if col2.button('update', key=key_values[0]):
                        self.update_single_pip(key_values[0], key_values[1])
                    break

    def find_newest_version_pip(self, item):
        newest_version = ''
        if os.path.exists('%s/.pip/pip.conf' % (os.environ.get('HOME'))):
            command = 'pip install --no-deps  %s== 2>%s/out.txt' % (item, os.environ.get('HOME'))
        else:
            command = 'pip install --no-deps --index-url http://192.168.0.102:3141/root/dev %s== --trusted-host devpi.cdsslh.com 2>%s/out.txt'% \
            (item, os.environ.get('HOME'))
        os.system(command)
        with open('%s/out.txt' % (os.environ.get('HOME')), 'r') as f:
            line = f.readline()
            newest_version = line.split('from versions: ')[-1].split(')')[0].split(',')[-1].replace(' ', '')
            f.close()
            os.system('rm %s/out.txt' % (os.environ.get('HOME')))
        return newest_version

    def update_single_pip(self, _module, _version=''):
        st.write('updating %s ...' % (_module))

        command = 'pip uninstall -y %s' % (_module)
        os.system(command)
        # 安装
        if os.path.exists('%s/.pip/pip.conf' % (os.environ.get('HOME'))):
            command = 'pip install --no-deps  %s' % (_module)
        else:
            command = 'pip install --no-deps --index-url http://192.168.0.102:3141/root/dev %s\
                    --trusted-host devpi.cdsslh.com' % (_module)
        st.write('pip install --no-deps  %s' % (_module))
        os.system(command)
        # 安装依赖
        command = 'pip install %s' % (_module)
        os.system(command)

        if _module == 'ctpview':
            # 重启streamlit
            ui_id = self.checkprocess('streamlit')
            import ctpview
            command = 'nohup kill -9 %d; nohup streamlit run %s/workspace/ctp/domain/presentation.py >> \
                %s/.streamlit/output.log 2>&1 &' % (ui_id, ctpview.__path__[0], os.environ.get('HOME'))
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
        st.write(command)

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
