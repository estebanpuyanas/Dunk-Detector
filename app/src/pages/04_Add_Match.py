import streamlit as st
from modules.nav import SideBarLinks

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
        else:
            insert_query = """
                    INSERT INTO matches (homeTeamId, awayTeamId, date, time, location, homeScore, awayScore, finalScore)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            values = (int(home_team_id), int(away_team_id), date, time, location, int(home_score), int(away_score), 
                      final_score)

            st.success(f"Match result added successfully: {final_score}")