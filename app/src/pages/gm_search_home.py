import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"General Manager Information:, {st.session_state['first_name']}.")

# create a 1 column layout
col1, col2 = st.columns(2)

with col1:
  var_01 = st.number_input('Team Id: ',
                           step=1)
  
with col2:
  var_02 = st.number_input('GM Id:',
                           step=1)


logger.info(f'Team = {var_01}')
logger.info(f'Name = {var_02}')

if st.button('Search by Team',
             type='primary',
             use_container_width=True):
    
    results = requests.get(f'http://api:4000/c/gm/{var_01}').json()
  st.dataframe(results)


if st.button('Search by Name',
             type='primary',
             use_container_width=True):
   results = requests.get(f'http://api:4000/c/gm/{var_02}').json()
  st.dataframe(results)