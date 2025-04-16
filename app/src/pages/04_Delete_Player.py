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

def fetch_players():
    try:
        response = requests.get("http://api:4000/pl/players")
        response.raise_for_status()
        players = response.json()  # Expecting a list of player dicts from the API
        return players
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching players: {e}")
        return []

players = fetch_players()

# Convert to "ID - Full Name" format for dropdown
def format_full_name(player):
    # Handles NULL middle name cleanly
    first = player.get("firstName", "")
    middle = player.get("middleName", "")
    last = player.get("lastName", "")
    full_name = f"{first} {middle + ' ' if middle else ''}{last}".strip()
    return f"{player['id']} - {full_name}"

player_options = [format_full_name(p) for p in players]

def extract_player_id(option_str):
    return int(option_str.split(" - ")[0])

# Form
with st.form("delete_player_form"):
    st.subheader("Delete Player Info")

    selected_player = st.selectbox("Select a player to delete", options=player_options)

    submit = st.form_submit_button("Delete Player")

    if submit and selected_player:
        player_id = extract_player_id(selected_player)
        try:
            api_link = f'http://api:4000/pl/players/{player_id}'
            response = requests.delete(api_link)
            response.raise_for_status()

            if response.status_code == 200:
                st.success(f"Player with ID '{player_id}' deleted successfully!")
            elif response.status_code == 404:
                st.error(f"No user found with ID '{player_id}'.")
            else:
                st.error(f"Failed to delete user. Status: {response.status_code}, Error: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to user API: {e}")