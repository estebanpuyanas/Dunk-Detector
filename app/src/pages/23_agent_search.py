import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Rosters:, {st.session_state['first_name']}.")

if st.button('Player Agents',
             type='primary',
             use_container_width=True):
  
  var_01 = st.number_input('Player\'s ID: ', step=1, value=None)
  logger.info(f'Player = {var_01}')

  try:
    results = requests.get(f'http://api:4000/a/agents/player/{var_01}').json()
  except:
    st.write("Could not connect to the database to find the Agent")
  else:
    st.dataframe(results)

if st.button('Coaches\' Agents',
             type='primary',
             use_container_width=True):
  
  var_02 = st.number_input('Coach\'s ID: ', step=1, value=None)
  logger.info(f'Coach = {var_02}')

  try:
    results = requests.get(f'http://api:4000/a/agents/coach/{var_01}').json()
  except:
    st.write("Could not connect to the database to find the Agent")
  else:
    st.dataframe(results)
