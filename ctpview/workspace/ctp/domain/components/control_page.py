import streamlit as st
import psutil
import os
import time
import base64

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

    def get_binary_file_downloader_html(self, bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">download {file_label}</a>'
        return href

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
        st.header('%s'%("%s:"%(_name)))
        contain = st.container()
        col1,col2 = contain.columns(2)
        if col1.button('start', key='%s1'%(_name)) and not(isinstance(self.checkprocess(_name), int)):
            command = 'nohup %s </dev/null 1>/dev/null 2> %s/log/%s/%s_exception.log &'%(_name, os.environ.get('HOME'), _name, _name)
            os.system(command)
            time.sleep(0.1)

        if col2.button('stop', key='%s2'%(_name)) and isinstance(self.checkprocess(_name), int):
            os.system('kill -9 %d'%(self.checkprocess(_name)))
            time.sleep(0.1)

        if isinstance(self.checkprocess(_name), int):
            status = 'start'
        else:
            status = 'not start'
        st.write('status: `%s`'%(status))
        log_files = []
        if os.path.isdir('%s/log/%s'%(os.environ.get('HOME'), _name)):
            temp_list = os.listdir('%s/log/%s'%(os.environ.get('HOME'), _name))
            for item in sorted(temp_list, reverse=True):
                log_files.append(item)

        index = st.selectbox('process log', log_files, index=0, key='%s3'%(_name))
        if index != None:
            st.markdown(self.get_binary_file_downloader_html('%s/log/%s/%s'%(os.environ.get('HOME'), _name, index), index),
                        unsafe_allow_html=True)
            if st.button('view', key='%s4'%(_name)):
                fd = open('%s/log/%s/%s'%(os.environ.get('HOME'), _name, index))
                st.write(fd.readlines())
                fd.close()
        try:
            with open('%s/log/%s/%s_exception.log'%(os.environ.get('HOME'), _name, _name), 'r', encoding='utf8') as fp:
                exception_log = fp.readlines()
                if len(exception_log) > 0:
                    st.info(exception_log[-10:])
                fp.close()
        except:
            pass

control_page = control()
