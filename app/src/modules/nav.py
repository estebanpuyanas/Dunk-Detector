# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/40_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of coach ------------------------
def CoachHomeNav():
    st.sidebar.page_link(
        "pages/00_Coach_Home_Nav.py", label="Coach Home", icon="👤"
    )

def OtherTeamStats():
    st.sidebar.page_link(
        "pages/01_OtherTeamStats.py", label="Other Team Stats", icon="📈"
    )

def ViewMakeReports():
    st.sidebar.page_link(
        "pages/01_Reports.py", label="View/Make Reports", icon="📊"
    )

def ViewAllGameplans():
    st.sidebar.page_link(
        "pages/01_Gameplans_Home_Nav.py", label="View All Gameplans", icon="🏀"
    )

## ------------------------ Examples for Role of Data Analyst ------------------------
def playerReports():
    st.sidebar.page_link(
        "pages/11_Player_Data_Report.py", label="Player Data Reports", icon="🛜")


def makeNotes():
    st.sidebar.page_link(
        "pages/12_Add_notes.py", label="Make Notes", icon="📈"
    )


def comparePlayers():
    st.sidebar.page_link(
        "pages/13_FindMostSimilarPlayer.py", label="Compare Players", icon="🌺"
    )

def matchHistory():
    st.sidebar.page_link(
        "pages/14_TeamMatchHistory.py", label="Team Match History Viewer", icon="🌺"
    )

## ------------------------ Examples for Role of General Manager ------------------------
def GmSearch():
    st.sidebar.page_link(
        "pages/21_gm_search.py", label="General Manager Search", icon="🛜")


def rosterSearch():
    st.sidebar.page_link(
        "pages/22_player_roster.py", label="Roster Look Up", icon="📈"
    )


def agentSearch():
    st.sidebar.page_link(
        "pages/23_agent_search.py", label="Agent Search", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/30_system_admin_home.py", label="System Admin", icon="🖥️")

def AddPlayers():
    st.sidebar.page_link(
        "pages/04_Add_Player.py", label="Add Player", icon="➕"
    )

def AddMatch():
    st.sidebar.page_link(
        "pages/04_Add_Match.py", label="Add Match", icon="📅"
    )

def DelPlayer():
    st.sidebar.page_link(
        "pages/04_Delete_Player.py", label="Delete Player", icon="🗑️"
    )

def UpdateScore():
    st.sidebar.page_link(
        "pages/04_Update_Match_Score.py", label="Update Match Score", icon="🔢"
    )

def UpdateUser():
    st.sidebar.page_link(
        "pages/04_Update_user_Info.py", label="Update User Info", icon="👤"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("/static/Dunk-Detector-Logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "coach":
            CoachHomeNav()
            OtherTeamStats()
            ViewMakeReports()
            ViewAllGameplans()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "general_manager":
            GmSearch()
            rosterSearch()
            agentSearch()
            comparePlayers()

        if st.session_state["role"] == "data_analyst":
            playerReports()
            makeNotes()
            comparePlayers()
            matchHistory()
            

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")