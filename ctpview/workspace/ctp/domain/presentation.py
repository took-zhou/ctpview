import os

import streamlit as st

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
        module_option = st.sidebar.radio('modue', ('configure', 'control', 'status', 'backtest', 'update', 'setting', 'manual'))
        if module_option == 'configure':
            parameter_page.update()
        elif module_option == 'control':
            control_page.update()
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


app = ctpview()
app.update()
