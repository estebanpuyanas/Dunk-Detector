import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"General Manager Information:, {st.session_state['first_name']}")
  
var_01 = st.text_input('Team: ')
logger.info(f'Team = {var_01}')

if st.button('Search by Team',
             type='primary',
             use_container_width=True):
  try:
    results = requests.get(f'http://api:4000/g/gm/teams/{var_01}').json()
  except:
    st.write("Could not connect to the database to find the General Manager")
  else:
    st.dataframe(results)


var_02 = st.text_input('Name: ')
logger.info(f'Name = {var_02}')

if st.button('Search by Name',
             type='primary',
             use_container_width=True):

  try:
    results = requests.get(f'http://api:4000/g/gm/{var_02}').json()
  except:
    st.write("Could not connect to the database to find the General Manager")
  else:
    st.dataframe(results)