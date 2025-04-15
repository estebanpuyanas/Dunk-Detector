import streamlit as st
from modules.nav import SideBarLinks
import requests
import datetime

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Add New Player")
min_date = datetime.date(1900, 1, 1)
max_date = datetime.date.today()

# Form
with st.form("add_player_form"):
    st.subheader("New Player Info")

    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name (optional)")
    last_name = st.text_input("Last Name")
    agent_id = st.number_input("Agent ID", min_value=1, step=1)
    position = st.text_input("Position")
    team_id = st.number_input("Team ID", min_value=1, step=1)
    height = st.number_input("Height (in)", min_value=50, max_value=100)
    weight = st.number_input("Weight (lbs)", min_value=100, max_value=500)
    dob = st.date_input("Date of Birth", min_value=min_date, max_value=max_date)
    injury_id = st.number_input("Injury ID (optional)", min_value=0, step=1)

    submit = st.form_submit_button("Add GM")

    if submit:
        if not (first_name and last_name and agent_id and position and team_id and height and weight and dob):
            st.warning("Please fill in all required fields (first name, last name, etc.)")
        else:
            # Build the payload
            player_payload = {
                "firstName": first_name,
                "middleName": middle_name if middle_name else None,
                "lastName": last_name,
                "agentId": int(agent_id),
                "position": position,
                "teamId": int(team_id),
                "height": int(height),
                "weight": int(weight),
                "dob": dob.strftime("%Y-%m-%d"),
                "injuryId": int(injury_id) if injury_id else None
            }
            try:
                api_link = 'http://api:4000/pl/players'
                response = requests.post(api_link, json=player_payload)
                response.raise_for_status()  # Ensure the status code is checked for errors

                if response.status_code == 201:
                    results = response.json()
                    new_id = results.get("id", "Unknown")
                    st.success(f"Player added successfully! Player ID: {new_id}")
                else:
                    st.error(f"Failed to add player. Server responded with status code {response.status_code}")
                    st.error(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {e}")