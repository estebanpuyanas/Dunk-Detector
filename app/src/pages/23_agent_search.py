import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Agents:, {st.session_state['first_name']}")

col1, col2 = st.columns(2)

with col1:
  st.subheader("Search for a Player's Agent")

  try:
    all_players = requests.get('http://api:4000/pl/players').json()
    all_players = [player['firstName'] + " " + player['lastName'] for player in all_players]  
  except:
    st.write('Could not connect to the database to get Player list')

  # Create searchbox
  selected_player = st.selectbox('Player:',
                                options=all_players,
                                index=None,
                                placeholder='Search for a Player...',
  )

with col2:
  st.subheader("Search for a Coach's Agent")

  try:
    all_coaches = requests.get('http://api:4000/c/coaches').json()
    all_coaches = [coach['firstName'] + " " + coach['lastName'] for coach in all_coaches]  
  except:
    st.write('Could not connect to the database to get Player list')

  # Create searchbox
  selected_coach = st.selectbox('Coach :',
                                options=all_coaches,
                                index=None,
                                placeholder='Search for a Coach...',
  )


if selected_player:
  st.write(f'{selected_player}\'s Agent: ')
  results = requests.get(f'http://api:4000/a/agents/player/{selected_player}').json()
  st.dataframe(results)

if selected_coach:
  st.write(f'{selected_coach}\'s Agent: ')
  results = requests.get(f'http://api:4000/a/agents/coach/{selected_coach}').json()
  st.dataframe(results)


# var_02 = st.text_input('Coach: ', value=None)
# logger.info(f'Coach = {var_02}')

# if var_02:
#   results = requests.get(f'http://api:4000/a/agents/coach/{var_02}').json()
#   st.dataframe(results)
