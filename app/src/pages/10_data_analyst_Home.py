import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.session_state["Data Analyst"] = "Phillip"

st.title(f"Welcome Data Analyst, {st.session_state['Data Analyst']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Player Data Report', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Player_Data_Report.py')

if st.button('Make Notes', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Add_notes.py')

if st.button("Compare Players",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_FindMostSimilarPlayer.py')

if st.button("Team Match History Viewer",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_TeamMatchHistory.py')

