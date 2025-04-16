import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Rosters:, {st.session_state['first_name']}.")

try:
    all_teams = requests.get('http://api:4000/t/teams').json()
    all_teams = [team['name'] for team in all_teams]  
except:
    st.write('Could not connect to the database to get teams list')

# Create searchbox
team_options = all_teams
selected_team = st.selectbox('Team:',
                              options=team_options,
                              index=None,
                              placeholder="Search for a team...",
)

if selected_team != None:
    results = requests.get(f'http://api:4000/t/teams/{selected_team}').json()
    st.dataframe(results)



