import logging
logger = logging.getLogger(__name__)
import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import date

SideBarLinks()

# TESTED - creating a form 
#st.write("# Make a Report!")

#with st.form("Make a Report!"):
#    coach_id = st.text_input("Coach ID*")
#    report_date = st.date_input("Date Created*") 
#    content = st.text_input("Content*")
    
#    submitted = st.form_submit_button("Submit")

#    if submitted:
#        data = {}
#        if not coach_id or not report_date or not content:
#            st.warning("Please fill all required fields*")
#            data['report_date'] = report_date
#        else: 
#            data['coach_id'] = coach_id
#            data['report_date'] = report_date.isoformat()
#            data['repoty_content'] = content
#            st.write(data)
#            st.success("Report successfully submitted", icon="✅") 

#            requests.post('http://api:4000/gp/gameplans', json=data) 
            #TODO change to report routes 
            #TODO update reports page to show reports and make reports 


# JEROME'S PLAYER NOTES PAGE FOR DATA ANALYST

st.title("Player Notes")

# 1) Fetch notes (cached)
@st.cache_data
def fetch_notes():
    r = requests.get("http://api:4000/rp/reports")
    r.raise_for_status()
    return r.json()

# 2) Display existing notes
st.markdown("### Existing Notes")
try:
    notes = fetch_notes()
except Exception as e:
    st.error(f"Could not load notes: {e}")
    notes = []

if notes:
    for n in notes:
        st.write(f"**{n['reportDate']}** — Author **{n['firstName']}** **{n['lastName']}**")
        st.write(n["content"])
        st.markdown("---")
else:
    st.info("No notes yet.")

# 3) Add a new note
st.markdown("### Add a New Note")
with st.form("new_note"):
    author  = st.text_input("Author ID")
    content = st.text_area("Note content")
    submitted = st.form_submit_button("Submit Note")

if submitted:
    if not author or not content:
        st.error("Both author and content are required.")
    else:
        payload = {
            "authorId":   author,
            "reportDate": date.today().isoformat(),
            "content":    content,
            "reportType": "general"
        }
        try:
            resp = requests.post("http://api:4000/rp/reports", json=payload)
            resp.raise_for_status()
            st.success("Note added!")
            # clear cache so next fetch picks up the new note
            fetch_notes.clear()
        except Exception as e:
            st.error(f"Failed to add note: {e}")

        