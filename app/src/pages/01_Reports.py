import logging
logger = logging.getLogger(__name__)
import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

# TESTED - creating a form 
st.write("# Make a Report!")

with st.form("Make a Report!"):
    date = st.date_input("Date Created:", value=None) 
    content = st.text_input("Describe New Report:")
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {}
        if not date or not content:
            st.warning("Please fill all required fields: date, content")
            data['report_date'] = date
        else: 
            data['report_date'] = date.isoformat()
            data['repoty_content'] = content
            st.write(data)
            st.success("Report successfully submitted", icon="✅") 

            requests.post('http://api:4000/gp/gameplans', json=data) 
            #TODO change to report routes 
            #TODO update reports page to show reports and make reports 
        