import logging
logger = logging.getLogger(__name__)
import datetime
import streamlit as st
import requests 
import json
from streamlit_extras.app_logo import add_logo 
from modules.nav import SideBarLinks

SideBarLinks()


# TEMPLATE
# st.write("# More API Access Examples")
# st.write("## Creating a New Product")


# DELETE THIS BUTTON 
#if st.button('View Selected Gameplan', 
#             type='primary',
#             use_container_width=True):
#  st.switch_page('pages/01_Selected_Gameplan.py')

# DELETE 01_New_Gameplan.py...
#if st.button('Create New Gameplan', 
#             type='primary',
#             use_container_width=True):
#  st.switch_page('pages/01_New_Gameplan.py')

# TESTED 
st.write("# View All Gameplans")
# Simply retrieving data from a REST api running in a separate Docker Container.
#If the container isn't running, this will be very unhappy.  But the Streamlit app 
#should not totally die. 

data = {} 
try:
  data = requests.get('http://api:4000/gp/gameplans').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

#st.dataframe(data)
st.table(data)

# TESTED - creating a form 
st.write("## Make a New Gameplan!")

with st.form("Make a New Gameplan!"):
    # today_date = datetime.date.today()
    plan_date = st.date_input("Date created:", value=None) 
    plan_content = st.text_input("Describe New Gameplan:")
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

    # Insert a file uploader that accepts multiple files at a time
    for uploaded_file in uploaded_files: 
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        # st.write(bytes_data) we do not need to see binary translation of image on screen
    
    submitted = st.form_submit_button("Submit")

    if submitted:
      data = {}
      if not plan_date or not plan_content or not uploaded_files:
        st.warning("Please fill all required fields: date, content, and file(s)")
        data['gameplan_date'] = plan_date
        # data['gameplan_files'] = uploaded_files
      else:
        data['gameplan_date'] = plan_date.isoformat()
        data['gameplan_content'] = plan_content
        # data['gameplan_files'] = uploaded_files.isoformat() error
        st.write(data) #helpful to see if data was proccessed 
        st.success("Gameplan successfully submitted", icon="✅")

        requests.post('http://api:4000/gp/gameplans', json=data)