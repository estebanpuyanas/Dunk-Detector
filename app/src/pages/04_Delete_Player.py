import streamlit as st
from modules.nav import SideBarLinks, AdminPageNav, AddPlayers, AddMatch, DelPlayer, UpdateScore, UpdateUser
import requests

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()
AdminPageNav()
AddPlayers()
AddMatch()
DelPlayer()
UpdateScore()
UpdateUser()

st.title("Delete Player")

# Form
with st.form("delete_player_form"):
    st.subheader("Delete Player Info")

    player_id = st.number_input("Enter Player ID to Delete", min_value=1, step=1)

    submit = st.form_submit_button("Delete Player")

    if submit:
        try:
            api_link = f'http://api:4000/pl/players/{int(player_id)}'
            response = requests.delete(api_link)
            response.raise_for_status()  # Ensure the status code is checked for errors

            if response.status_code == 200:
                st.success(f"Player with ID '{player_id}' deleted successfully!")
            elif response.status_code == 404:
                st.error(f"No user found with ID '{player_id}'.")
            else:
                st.error(f"Failed to delete user. Status: {response.status_code}, Error: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to user API: {e}")
