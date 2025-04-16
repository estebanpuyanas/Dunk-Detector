import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"General Manager Information:, {st.session_state['first_name']}")

col1, col2 = st.columns(2)

with col1:
  st.subheader("Search by Team")

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
                                placeholder='Search for a team...',
  )


with col2:
  st.subheader('Search by Name')
  try:
    all_gms = requests.get('http://api:4000/g/gm').json()
    all_gms = [gm['firstName'] + " " + gm['lastName'] for gm in all_gms]
  except:
    st.write('Could not connect to the database to get GM list')

  # Create dropbox
  gm_options = all_gms
  selected_gm = st.selectbox('GMs:', 
                             gm_options,
                             index=None,
                             placeholder='Search for a GM...')


# Create dataframe when a team is selected
if selected_team:
  
  logger.info(f'Team = {selected_team}')
  try:
    results = requests.get(f'http://api:4000/g/gm/teams/{selected_team}').json()
  except:
    st.write('Could not connect to the database to find the General Manager')
  else:
    st.dataframe(results)

  # Create dataframe when a team is selected
if selected_gm:
  logger.info(f'Team = {selected_gm}')
  try:
    results = requests.get(f'http://api:4000/g/gm/{selected_gm}').json()
  except:
    st.write("Could not connect to the database to find the General Manager")
  else:
    st.dataframe(results)