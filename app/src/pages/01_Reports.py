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
    coach_id = st.text_input("Coach ID:")
    report_date = st.date_input("Date Created:") 
    content = st.text_input("Content:")
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {}
        if not coach_id or not report_date or not content:
            st.warning("Please fill all required fields: date, content")
            data['report_date'] = report_date
        else: 
            data['coach_id'] = coach_id
            data['report_date'] = report_date.isoformat()
            data['repoty_content'] = content
            st.write(data)
            st.success("Report successfully submitted", icon="✅") 

            requests.post('http://api:4000/gp/gameplans', json=data) 
            #TODO change to report routes 
            #TODO update reports page to show reports and make reports 
        