import os

import streamlit as st

from ctpview.workspace.ctp.domain.components.account_page import account_page
from ctpview.workspace.ctp.domain.components.authenticate_page import authenticate_page
from ctpview.workspace.ctp.domain.components.backtest_page import backtest_page
from ctpview.workspace.ctp.domain.components.control_page import control_page
from ctpview.workspace.ctp.domain.components.manual_page import manual_page
from ctpview.workspace.ctp.domain.components.parameter_page import parameter_page
from ctpview.workspace.ctp.domain.components.setting_page import setting_page
from ctpview.workspace.ctp.domain.components.status_page import status_page
from ctpview.workspace.ctp.domain.components.update_page import update_page


class ctpview():

    def __init__(self):
        st.set_page_config(page_title='tsaodai ctp operation control', layout='centered', page_icon="..")

    def update(self):
        authenticate_page.login()
        if 'authentication_status' in st.session_state and st.session_state['authentication_status'] != True:
            return

        if 'name' in st.session_state and st.session_state['name'] == 'admin':
            page_list = ('configure', 'control', 'account', 'status', 'backtest', 'update', 'setting', 'manual')
            module_option = st.sidebar.radio('modue', page_list)
        else:
            page_list = ('configure', 'control', 'account', 'status', 'backtest')
            module_option = st.sidebar.radio('modue', page_list)

        if module_option == 'configure':
            parameter_page.update()
        elif module_option == 'control':
            control_page.update()
        elif module_option == 'account':
            account_page.update()
        elif module_option == 'status':
            status_page.update()
        elif module_option == 'backtest':
            backtest_page.update()
        elif module_option == 'update':
            update_page.update()
        elif module_option == 'setting':
            setting_page.update()
        elif module_option == 'manual':
            manual_page.update()

        authenticate_page.logout()


app = ctpview()
app.update()
