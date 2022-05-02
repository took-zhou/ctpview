import streamlit as st
import os

from ctpview.workspace.ctp.domain.components.parameter_page import parameter_page
from ctpview.workspace.ctp.domain.components.control_page import control_page
from ctpview.workspace.ctp.domain.components.debug_page import debug_page
from ctpview.workspace.ctp.domain.components.status_page import status_page
from ctpview.workspace.ctp.domain.components.update_page import update_page
from ctpview.workspace.ctp.domain.components.setting_page import setting_page
from ctpview.workspace.ctp.infra.sender.proxy_sender import proxysender

class ctpview():
    def __init__(self):
        st.set_page_config(page_title='tsaodai ctp operation control', layout='centered', page_icon="..")

    def update(self):
        proxysender.set_config()

        if os.environ.get('run_mode') == 'debug' or 'simnow' in os.environ.get('base_url'):
            module_option = st.sidebar.radio('modue', ('configure', 'control', 'status', 'debug', 'update', 'setting'))
        else:
            module_option = st.sidebar.radio('modue', ('configure', 'control', 'status', 'update', 'setting'))

        if module_option == 'configure':
            parameter_page.update()
        elif module_option == 'control':
            control_page.update()
        elif module_option == 'status':
            status_page.update()
        elif module_option == 'debug':
            debug_page.update()
        elif module_option == 'update':
            update_page.update()
        elif module_option == 'setting':
            setting_page.update()

app = ctpview()
app.update()
