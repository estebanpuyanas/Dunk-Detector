import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Teams")
# TODO need to get team name from teams table 

st.write("# Players")
# TODO need to get players name with their position, stats, and contact info 

