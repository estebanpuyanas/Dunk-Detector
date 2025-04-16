import logging
import streamlit as st
import requests
import pandas as pd
import altair as alt
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
st.title("Find The Most Similar Players (Based on PPG, Rebounds, and Assists)")
playerStats = requests.get("http://api:4000/pl/playerStats_minutes?min_minutes=0")
#Raise if HTTPS error
playerStats.raise_for_status()
playerStats = pd.DataFrame(playerStats.json())


#Function to make a new DF of each players averages!
def findPlayAvgs(df):
    avgs = []
    grouped = df.groupby(['playerId', 'firstname', 'lastname'])[['totalPoints','rebounds','assists']].mean()
    ##This is needed so the playerId first name and last name can be columns
    grouped = grouped.reset_index()

    grouped = grouped.rename(columns={
        'totalPoints': 'PPG',
        'rebounds':    'RPG',
        'assists':     'APG'
    })

    grouped['player'] = grouped['firstname'] + ' ' + grouped['lastname']
    return grouped

avgs = findPlayAvgs(playerStats)

players = avgs['player'].tolist()

selected_player = st.selectbox("Select a player", ["-- Select a player --"] + players)

player_data = avgs[avgs["player"].isin(players)].copy()

selected_stats = avgs[avgs['player'] == selected_player][['player', 'PPG', 'RPG', 'APG']]

if selected_player != "-- Select a player --" :
    st.subheader(f"{selected_player}'s Stats")
    col1, col2, col3 = st.columns(3)
    row = selected_stats.iloc[0]
    col1.metric("PPG", f"{row['PPG']:.2f}")
    col2.metric("RPG", f"{row['RPG']:.2f}")
    col3.metric("APG", f"{row['APG']:.2f}")

# If a player is selected then

    selected_stats = avgs[avgs['player'] == selected_player][['PPG', 'RPG', 'APG']].values[0]

    weights = [0.65, 0.20, 0.15]

    def weighted_distance(row):
        diff = row[['PPG', 'RPG', 'APG']].values - selected_stats
        return sum((weights[i] * (diff[i])**2 for i in range(3)))**0.5

    avgs['distance'] = avgs.apply(weighted_distance, axis=1)

    # Exclude selected player and get top 5 similar players
    similar_players = avgs[avgs['player'] != selected_player].sort_values(by='distance').head(5)

    # Show results
    st.subheader("Top 5 Most Similar Players")
    st.dataframe(similar_players[['player', 'PPG', 'RPG', 'APG', 'distance']])








