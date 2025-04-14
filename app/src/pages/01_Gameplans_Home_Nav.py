import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests 
from streamlit_extras.app_logo import add_logo 
from modules.nav import SideBarLinks

SideBarLinks()

'''
TEMPLATE
st.write("# More API Access Examples")
st.write("## Creating a New Product")
'''
st.write("# View All Gameplans")
st.write("## Or Make A New Gameplan!")


if st.button('View Selected Gameplan', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Selected_Gameplan.py')

if st.button('Create New Gameplan', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_New_Gameplan.py')


# DOES NOT WORK
  # creating a form 
  st.write("## Make a New Gameplan!")

  with st.form("Make a New Gameplan!"):
    plan_content = st.text_input("Describe New Gameplan:")
    
    submitted = st.form_submitted_button("Submit")

    if submitted:
        data = {}
        data['gameplan_content'] = plan_content
        st.write(data)

        requests.post('http://api:4000/p/product', json=data)