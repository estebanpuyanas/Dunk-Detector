import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Coach, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

'''
template for switching to different pages 

if st.button('View World Bank Data Visualization', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_World_Bank_Viz.py')
'''

if st.button('View Other Team Stats', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_OtherTeamStats.py')

if st.button('View All Gameplans', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Gameplans_Home_Nav.py')

if st.button('View/Make Reports', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Reports.py')

