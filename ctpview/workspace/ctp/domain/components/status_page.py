import psutil
import streamlit as st
import socket
import json

from ctpview.workspace.common.file_util import jsonconfig

class status():
    def __init__(self):
        pass

    def getprocessid(self, processname):
        # --获取进程信息--
        ret = []
        pl = psutil.pids()  #所有的进程列出来

        for pid in pl:
            try:
                for item in processname:
                    if item in psutil.Process(pid).name():
                        ret.append(pid)
            except:
                continue
        return ret

    def update(self):
        process_list = self.getprocessid(['proxy', 'market', 'trader', 'streamlit'])
        for item in process_list:
            name = psutil.Process(item).name()
            cpu_percent = psutil.Process(item).cpu_percent(interval=1)
            memory_percent = psutil.Process(item).memory_percent()
            st.write('{}: `start` cup: `{:.2}` memory: `{:.2}`'.format(name, cpu_percent, memory_percent))

        count = 0
        for item in psutil.cpu_percent(interval=1, percpu=True):
            name = 'core%d'%(count)
            st.write('{} utilization rate: `{:.2}`'.format(name, item))
            count = count + 1

        memory_msg = psutil.virtual_memory()
        st.write('mem total: `{}` mem used: `{}` mem free: `{}`'.format(int(memory_msg.total/1024/1024), \
            int(memory_msg.used/1024/1024), int(memory_msg.free/1024/2014)))

        hostname=socket.gethostname()
        ip = socket.gethostbyname(hostname)
        st.write('local ip: `%s`'%(ip))

        subscribe_list = []
        try:
            st.write()
            st.write('market veriosn: `%s`'%(jsonconfig.get_config('market', 'version')))
            st.write('trader version: `%s`'%(jsonconfig.get_config('trader', 'version')))
            with open(jsonconfig.get_config('market', 'ControlParaFilePath'), 'r', encoding='utf8') as fp:
                control_json = json.load(fp)
                fp.close()
                for item in control_json.keys():
                    for i in range(len(control_json[item]['instrument'])):
                        subscribe_list.append(control_json[item]['instrument'][i]["id"]["ins"])
        except:
            pass

        subscribe_list = list(set(subscribe_list))
        st.write('subscribe instrument number from strategy: `%d`'%(len(subscribe_list)))
        st.write(subscribe_list)

status_page = status()