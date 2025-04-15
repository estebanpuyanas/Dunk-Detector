import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks, AdminPageNav, AddPlayers, AddMatch, DelPlayer, UpdateScore, UpdateUser
st.set_page_config(layout='wide')

# Sidebar nav links based on session role
# Sidebar nav links based on session role
SideBarLinks()
AdminPageNav()
AddPlayers()
AddMatch()
DelPlayer()
UpdateScore()
UpdateUser()

# Welcome section
st.title(f"Welcome System Admin, {st.session_state['first_name']}")
st.write('')
st.write('What would you like to do today?')

# Navigation Buttons
if st.button('Update User Info', type='primary', use_container_width=True):
    st.switch_page('pages/04_Update_user_Info.py')

if st.button('Add New PLayer', type='primary', use_container_width=True):
    st.switch_page('pages/04_Add_Player.py')

if st.button('Delete PLayer', type='primary', use_container_width=True):
    st.switch_page('pages/04_Delete_Player.py')

if st.button('Add New Match', type='primary', use_container_width=True):
    st.switch_page('pages/04_Add_Match.py')

if st.button('Update Match Score', type='primary', use_container_width=True):
    st.switch_page('pages/04_Update_Match_Score.py')