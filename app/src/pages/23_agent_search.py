import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Agents:, {st.session_state['first_name']}")

var_01 = st.text_input('Player: ', value=None)
logger.info(f'Player = {var_01}')

if var_01:
  results = requests.get(f'http://api:4000/a/agents/player/{var_01}').json()
  st.dataframe(results)


var_02 = st.text_input('Coach: ', value=None)
logger.info(f'Coach = {var_02}')

if var_02:
  results = requests.get(f'http://api:4000/a/agents/coach/{var_02}').json()
  st.dataframe(results)



if st.button('List of Players',
             type='primary',
             use_container_width=True):
  results = requests.get(f'http://api:4000/pl/players').json()
  st.dataframe(results)

if st.button('List of Coaches',
            type='primary',
            use_container_width=True):
  try:
    results = requests.get(f'http://api:4000/c/coaches').json()
  except:
    st.write("Could not connect to the database to find the Agent")
  else:
    st.dataframe(results)