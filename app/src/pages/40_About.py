import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    Welcome to The Dunk Detector 🏀! 

    We built this application for our CS3200 - Database Design course at Northeastern University. 
    This application is designed to provide general managers, coaches, socuts, and data analysts 
    with the tools they need to analyze player performance, statistics, and trends
    to make informed decisions about player acquisitions, trades, and game strategies.  

    The application is built using Python, using Streamlit for the front-end, Flask for the back-end, and MySQL for the database.  
   
    We are a team of 5 students:
    - Komdean Masoumi
    - Gokul Ramanan
    - Jerome Rodrigo
    - Esteban Puyana
    - Annie Wong

    We hope you enjoy using this application as much as we enjoyed building it!

    """
        )
