import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Rosters:, {st.session_state['first_name']}.")

var_01 = st.text_input('Team: ')

logger.info(f'var_01 = {var_01}')

if var_01:
    results = requests.get(f'http://api:4000/t/teams/{var_01}').json()
    st.dataframe(results)

if st.button('List of Teams',
             type='primary',
             use_container_width=True):
    
    data = {}
    data = requests.get(f'http://api:4000/t/teams').json()
    st.dataframe(data)




