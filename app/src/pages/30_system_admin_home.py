import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Sidebar nav links based on session role
SideBarLinks()

# Welcome section
st.title(f"Welcome System Admin, {st.session_state['first_name']}")
st.write('')
st.write('### Admin Control Panel')

# Navigation Buttons
if st.button('Update GM Info', use_container_width=True):
    st.switch_page('pages/04_Update_GM_Info.py')

if st.button('Add New Match', use_container_width=True):
    st.switch_page('pages/04_Add_Match.py')

if st.button('Add New GM', use_container_width=True):
    st.switch_page('pages/04_Add_GM.py')

if st.button('Update Match Score', use_container_width=True):
    st.switch_page('pages/04_Update_Match_Score.py')

if st.button('Delete User', use_container_width=True):
    st.switch_page('pages/04_Delete_User.py')