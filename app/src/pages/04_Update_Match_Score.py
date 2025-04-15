import streamlit as st
import requests
from modules.nav import SideBarLinks, AdminPageNav, AddPlayers, AddMatch, DelPlayer, UpdateScore, UpdateUser

# Layout and sidebar
st.set_page_config(layout="wide")
SideBarLinks()
AdminPageNav()
AddPlayers()
AddMatch()
DelPlayer()
UpdateScore()
UpdateUser()

st.title("Update Match Score")

with st.form("score_update_form"):
    st.subheader("Enter Score Update Details")

    match_id = st.number_input("Match ID", min_value=1, step=1)
    home_score = st.number_input("Home Team Score", min_value=0, step=1)
    away_score = st.number_input("Away Team Score", min_value=0, step=1)
    final_score = st.text_input("Final Score Summary")

    submit = st.form_submit_button("Update Score")

    if submit:
        if not match_id:
            st.warning("Please enter a valid Match ID.")
        else:
            update_data = {}
            if home_score is not None:
                update_data["homeScore"] = int(home_score)
            if away_score is not None:
                update_data["awayScore"] = int(away_score)
            if final_score.strip():
                update_data["finalScore"] = final_score.strip()

            if not update_data:
                st.warning("Please provide at least one score field to update.")
            else:
                try:
                    api_link = f'http://api:4000/m/matches/{int(match_id)}'
                    response = requests.patch(api_link, json=update_data)
                    response.raise_for_status()  # Ensure the status code is checked for errors

                    if response.status_code == 200:
                        st.success(f"Match ID {match_id} updated successfully.")
                    elif response.status_code == 404:
                        st.error(f"Match with ID {match_id} not found.")
                    else:
                        st.error(f"Failed to update match. Status: {response.status_code}.")
                        st.error(response.text)

                except requests.exceptions.RequestException as e:
                    st.error(f"Error while connecting to API: {e}")