import logging
logger = logging.getLogger(__name__)
import datetime
import streamlit as st
import requests 
import json
from streamlit_extras.app_logo import add_logo 
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# View All Gameplans")

#gets data from the gameplans route 
data = {} 
try:
  data = requests.get('http://api:4000/gp/gameplans').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

#shows data from gameplans route as a table on the screen
st.table(data)

# TESTED - creating a form 
st.write("## Make a New Gameplan!")

with st.form("Make a New Gameplan!"):
    coach_id = st.text_input("Coach ID*") 
    match_id = st.text_input("Match ID*") 
    plan_date = st.date_input("Date created*") 
    plan_content = st.text_input("Content*")
    uploaded_files = st.file_uploader("Choose a file*", accept_multiple_files=True)

    # Insert a file uploader that accepts multiple files at a time
    for uploaded_file in uploaded_files: 
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        # st.write(bytes_data) we do not need to see binary translation of image on screen
    
    submitted = st.form_submit_button("Submit")

    if submitted:
      data = {}
      if not coach_id or not match_id or not plan_date or not plan_content or not uploaded_files:
        st.warning("Please fill all required fields*")
        data['gameplan_date'] = plan_date
        # data['gameplan_files'] = uploaded_files
      else:
        data['coach_id'] = coach_id
        data['match_id'] = match_id
        data['gameplan_date'] = plan_date.isoformat()
        data['gameplan_content'] = plan_content
        # data['gameplan_files'] = uploaded_files.isoformat() -- error
        st.write(data) #helpful to see if data was proccessed 
        st.success("Gameplan successfully submitted", icon="✅")

        requests.post('http://api:4000/gp/gameplans', json=data)