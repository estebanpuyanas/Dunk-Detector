import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('General Manager Home Page')

if st.button('General Manager Search', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_gm_search.py')

if st.button('Roster Look Up',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_player_roster.py')

if st.button('Agent Look Up',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_agent_search.py')

if st.button("Compare Players",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_FindMostSimilarPlayer.py')