import json
import os

import streamlit as st
import streamlit_authenticator as stauth


class authenticate():

    def __init__(self):
        pass

    def login(self):
        json_data = None
        config_path = '%s/.local/ctpview/config.json' % (os.environ.get('HOME'))
        with open(config_path, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            fp.close()

        if json_data is not None:
            self.authenticator = stauth.Authenticate(json_data['credentials'], json_data['cookie']['name'], json_data['cookie']['key'],
                                                     json_data['cookie']['expiry_days'], json_data['preauthorized'])

            name, status, username = self.authenticator.login('Login', 'main')
            if status == False:
                st.error('Username/password is incorrect')
            elif status == None:
                st.warning('Please enter your username and password')

    def logout(self):
        st.sidebar.write('----')
        self.authenticator.logout('Logout', 'sidebar')
        st.sidebar.write(f'welcome `%s`' % (st.session_state['name']))
