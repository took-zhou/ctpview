import os

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from ctpview.workspace.ctp.domain.components.account_page import account
from ctpview.workspace.ctp.domain.components.authenticate_page import authenticate
from ctpview.workspace.ctp.domain.components.control_page import control
from ctpview.workspace.ctp.domain.components.manual_page import manual
from ctpview.workspace.ctp.domain.components.parameter_page import parameter
from ctpview.workspace.ctp.domain.components.setting_page import setting
from ctpview.workspace.ctp.domain.components.status_page import status
from ctpview.workspace.ctp.domain.components.update_page import update


class ctpview():

    def __init__(self):
        st.set_page_config(page_title='tsaodai ctp operation control',
                           layout='centered',
                           page_icon='%s/.local/resource/icon.png' % (os.environ.get('HOME')))
        self.authenticate_page = authenticate()

    def update(self):
        self.authenticate_page.login()
        if 'authentication_status' in st.session_state and st.session_state['authentication_status'] != True:
            return

        if 'name' in st.session_state and st.session_state['name'] == 'admin':
            page_list = ('parameter', 'control', 'account', 'status', 'update', 'setting', 'manual')
            module_option = st.sidebar.radio('Operation', page_list)
        else:
            page_list = ('parameter', 'account', 'status')
            module_option = st.sidebar.radio('Operation', page_list)

        if module_option == 'parameter':
            parameter().update()
        elif module_option == 'control':
            control().update()
        elif module_option == 'account':
            account().update()
        elif module_option == 'status':
            status().update()
        elif module_option == 'update':
            update().update()
        elif module_option == 'setting':
            setting().update()
        elif module_option == 'manual':
            manual().update()

        self.authenticate_page.logout()
        if module_option not in ['update', 'setting']:
            st_autorefresh(interval=10000, limit=10000, key="auto_update")


app = ctpview()
app.update()
