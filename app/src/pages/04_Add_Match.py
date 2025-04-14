import streamlit as st
from modules.nav import SideBarLinks
import requests
import datetime

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Add New Match Result")

# Form
with st.form("match_form"):
    st.subheader("Match Info")

    home_team_id = st.number_input("Home Team ID", min_value=1, step=1)
    away_team_id = st.number_input("Away Team ID", min_value=1, step=1)
    date = st.date_input("Match Date")
    time = st.time_input("Match Time")
    location = st.text_input("Location")
    home_score = st.number_input("Home Team Score", min_value=0, step=1)
    away_score = st.number_input("Away Team Score", min_value=0, step=1)
    final_score = st.text_input("Final Score (e.g., 102–98)")

    submit = st.form_submit_button("Add Match Result")

    if submit:
        if not (home_team_id and away_team_id and location and final_score):
            st.warning("Please fill in all required fields.")
        elif home_team_id == away_team_id: 
            st.warning("You entered two teams with the same ID.")
        else:
            match_payload = {
                "homeTeamId": int(home_team_id),
                "awayTeamId": int(away_team_id),
                "date": str(date),
                "time": str(time),
                "location": location,
                "homeScore": int(home_score),
                "awayScore": int(away_score),
                "finalScore": final_score
            }
            try: 
                response = requests.post('http://host.docker.internal:4000/matches_routes.py', json = match_payload)
                if response.status_code == 201:
                    match_id = response.json().get("id")
                    st.success(f"Match result added successfully! Match ID: {match_id}")
                else:
                    st.error(f"Failed to add match. Status code: {response.status_code}")
                    st.error(response.text)
            except Exception as e: 
                st.error(f"Error: {e}")
                