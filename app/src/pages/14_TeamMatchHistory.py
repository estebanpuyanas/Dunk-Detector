import logging
import streamlit as st
import requests
import pandas as pd
import altair as alt
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
st.title("Team Match History")

try:
    response = requests.get("http://api:4000/ma/matches")
    response.raise_for_status()
    matches = pd.DataFrame(response.json())
except Exception as e:
    st.error("Failed to fetch match data.")
    st.stop()

team_names = pd.unique(matches[['homeTeamName', 'awayTeamName']].values.ravel()) ## FLATTENS TO a 1d array

selected_team = st.selectbox("Select a team", sorted(team_names))

team_matches = matches[
    (matches['homeTeamName'] == selected_team) |
    (matches['awayTeamName'] == selected_team)
]

st.subheader(f"Match History for {selected_team}")
st.dataframe(
    team_matches.sort_values("date", ascending=False)[[
        "homeTeamName", "awayTeamName",
        "homeScore", "awayScore", "finalScore", "date"
    ]]
)
