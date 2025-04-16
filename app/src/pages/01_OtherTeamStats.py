import logging
import streamlit as st
import requests
import pandas as pd
import altair as alt
from modules.nav import SideBarLinks

SideBarLinks()
#st.text_input("Teams")
#st.text_input("Players")


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




st.title('Player Stats Minutes Report')

# Create a number input for minimum play time (in minutes)
min_minutes = st.number_input("Minimum Play Time (in minutes)", value=0, step=1)

st.write("Click the button below to fetch player statistics for players who have played at least the specified number of minutes.")

# Initialize a session state variable to store fetched data
if "fetched_data" not in st.session_state:
    st.session_state.fetched_data = None

# Button to fetch data from the API endpoint
if st.button('Fetch Player Stats Minutes', type='primary', use_container_width=True):
    try:
        api_url = f"http://api:4000/pl/playerStats_minutes?min_minutes={min_minutes}"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        #Json to PD df
        results = response.json()
        df = pd.DataFrame(results)
        
        # Convert match_date column to datetime as its a string in json
        if 'match_date' in df.columns:
            df['match_date'] = pd.to_datetime(df['match_date'])
        
        # Combine first and last names into a single 'player' column for convenience
        if 'firstname' in df.columns and 'lastname' in df.columns:
            df['player'] = df['firstname'] + " " + df['lastname']
        
        # Store the fetched DataFrame in session state
        st.session_state.fetched_data = df
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        logger.exception("Error fetching player stats minutes")

# Once data is fetched, display additional interactive controls
if st.session_state.fetched_data is not None:
    df = st.session_state.fetched_data
    st.dataframe(df)
    
    # Allow multiple players to be selected via a multiselect widget.
    players = df['player'].tolist() if 'player' in df.columns else []


    selected_players = st.multiselect("Select players", players, default=[])
    
    # Define the selectable statistic columns for plotting.
    stat_options = ["totalPoints", "assists", "rebounds", "steals", "blocks",
                    "fieldGoals", "threePointers", "freeThrows", "fouls", "turnovers"]
    available_stats = [col for col in stat_options if col in df.columns]
    selected_stat = st.selectbox("Select a statistic", available_stats)
    
    # Filter the DataFrame to only include rows for the selected players.
    if 'player' in df.columns and selected_players:
        player_data = df[df["player"].isin(selected_players)].copy()
        if not player_data.empty and 'match_date' in player_data.columns:
            player_data = player_data.sort_values("match_date")
        
        st.write(f"### {', '.join(selected_players)}: {selected_stat} Over Time")
        
        # Build an interactive Altair chart with multiple lines, each representing a player.
        chart = alt.Chart(player_data).mark_line(point=True).encode(
            x=alt.X("match_date:T", title="Match Date"),
            y=alt.Y(f"{selected_stat}:Q", title=selected_stat),
            color=alt.Color("player:N", title="Player"),  # Color lines by player
            tooltip=["match_date", selected_stat, "player"]
        ).properties(
            width=700,
            height=400,
            title=f"{selected_stat} Over Time for Selected Players"
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No data available for the selected players or missing match_date column.")
