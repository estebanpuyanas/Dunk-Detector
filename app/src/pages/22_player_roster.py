import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Rosters:, {st.session_state['first_name']}.")

# response = requests.get('http://api:4000/teams')
# st.write(response.status_code)
# st.write(response.text)

var_01 = (st.text_input('Team: '))

if st.button('List of Teams',
             type='primary',
             use_container_width=True):
    data = {}
    # try:
    data = requests.get(f'http://api:4000/teams').json()
    # except:
    #     st.write("Could not connect to the database to find a list of Teams")
    # else:
    st.dataframe(data)

# try:
#     results = requests.get(f'http://host.docker.interal:4000/t/teams/{var_01}').json()
# except:
#     st.write("Could not connect to the database to find the Roster")
# else:
#     st.dataframe(results)
# response = requests.get('http://host.docker.internal:4000/teams')
# print(response.status_code)
# print(response.text) 



