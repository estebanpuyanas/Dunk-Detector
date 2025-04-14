import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the logged-in user
SideBarLinks()

st.title('Player Stats Minutes Report')

# Create a number input for minimum play time (in minutes)
min_minutes = st.number_input("Minimum Play Time (in minutes)", value=0, step=1)

st.write("Click the button below to fetch player statistics for players who have played at least the specified number of minutes.")

# Button to fetch the data from Flask endpoint
if st.button('Fetch Player Stats Minutes', type='primary', use_container_width=True):
    try:
        # Construct API URL with the query parameter for min_minutes
        api_url = f"http://host.docker.internal:4000/plstmin/playerStats_minutes?min_minutes={min_minutes}"
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse the JSON response
        results = response.json()
        
        # Display the results in a dataframe
        st.dataframe(results)
        logger.info("Successfully fetched player stats minutes data.")
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        logger.exception("Error fetching player stats minutes")
