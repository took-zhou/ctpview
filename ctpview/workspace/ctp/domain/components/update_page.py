import streamlit as st
import os
import configparser
import psutil

class update():
    def __init__(self):
        pass

    def update(self):
        self.update_market_trader()

        st.write('____')

        self.update_ctpview()

    def update_market_trader(self):
        cf = configparser.ConfigParser()
        cf.read("%s/.marktrade.conf"%(os.environ.get('HOME')))
        installed_pack = cf.get('global', 'PROJPATH')
        pack_name = installed_pack.split('.')[0].split('/')[-1]

        command = 'rm %s/package/file.txt; wget -P %s/package/ http://%s:%s/pack/file.txt'%(os.environ.get('HOME'), os.environ.get('HOME'), \
            os.environ.get('http_ip'), os.environ.get('http_port'))
        os.system(command)
        f = open('%s/package/file.txt'%(os.environ.get('HOME')))
        lines = f.readlines()
        f.close()

        pack_list = [item.split('.')[0] for item in lines]
        pack_list.sort()
        newest_name = pack_list[-1]

        contain = st.container()
        col1,col2 = contain.columns(2)
        col1.write('marktrade: %s --> %s'%(pack_name, newest_name))
        if col2.button('update', key='update2'):
            os.system('cic update marktrade')

    def update_ctpview(self):
        newest_version = self.find_newest_version('ctpview')

        temp_items = os.popen('pip list')
        lines_items = temp_items.readlines()
        for item in lines_items:
            key_values = [value for value in item.split(' ') if value != '']
            if key_values[0] == 'ctpview':
                contain = st.container()
                col1,col2 = contain.columns(2)
                col1.write('%s: %s --> %s'%(key_values[0], key_values[1], newest_version))
                if col2.button('update', key=key_values[0]):
                    self.update_single(key_values[0], key_values[1])
                break

    def find_newest_version(self, item):
        newest_version = ''
        if os.path.exists('%s/.pip/pip.conf'%(os.environ.get('HOME'))):
            command = 'pip install --no-deps  %s== 2>%s/out.txt'%(item, os.environ.get('HOME'))
        else:
            command = 'pip install --no-deps --index-url http://devpi.cdsslh.com:8090/root/dev %s== --trusted-host devpi.cdsslh.com 2>%s/out.txt'% \
            (item, os.environ.get('HOME'))
        os.system(command)
        with open('%s/out.txt'%(os.environ.get('HOME')), 'r') as f:
            line = f.readline()
            newest_version = line.split('from versions: ')[-1].split(')')[0].split(',')[-1].replace(' ', '')
            f.close()
            os.system('rm %s/out.txt'%(os.environ.get('HOME')))
        return newest_version

    def update_single(self, _module, _version=''):
        st.write('updating %s ...'%(_module))

        command = 'pip uninstall -y %s'%(_module)
        os.system(command)
        # 安装
        if os.path.exists('%s/.pip/pip.conf'%(os.environ.get('HOME'))):
            command = 'pip install --no-deps  %s'%(_module)
        else:
            command = 'pip install --no-deps --index-url http://devpi.cdsslh.com:8090/root/dev %s\
                    --trusted-host devpi.cdsslh.com'%(_module)
        st.write('pip install --no-deps  %s'%(_module))
        os.system(command)
        # 安装依赖
        command = 'pip install %s'%(_module)
        os.system(command)

        if _module == 'ctpview':
            # 重启streamlit
            ui_id = self.checkprocess('streamlit')
            import ctpview
            command = 'nohup kill -9 %d; nohup streamlit run %s/workspace/ctp/domain/presentation.py >> \
                %s/.streamlit/output.log 2>&1 &'%(ui_id, ctpview.__path__[0], os.environ.get('HOME'))
            os.system(command)

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
