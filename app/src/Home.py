##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('The Dunk Detector - Basketball Scouting & Analytics Application')
st.write('\n\n')
st.write('### Hi! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Mike Thompson, a Basketball Coach", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'coach'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Mike'
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Coach Mike Thompson")
    
    st.switch_page('pages/00_Coach_Home_Nav.py') 
    #TODO UPDATE THIS PAGE TO COACH NEEDS. 

if st.button('Act as Phillip, a data anlyst for the New York Knicks', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'data_analyst'
    st.session_state['first_name'] = 'Phillip'
    logger.info("Logging in as Knicks Data Analyst Phillip")
    st.switch_page('pages/10_data_analyst_home.py') #TODO UPDATE THIS PAGE TO DATA ANALYST NEEDS.

if st.button('Act as Patrick Carter, an NBA General Manager', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'general_manager'
    st.session_state['first_name'] = 'Patrick'
    logger.info("Logging in as GM Patrick Carter")
    st.switch_page('pages/20_general_manager_home.py') #TODO UPDATE THIS PAGE TO GM NEEDS.

if st.button('Act as Alex Montgomery, a System Administrator',
             type = 'primary', 
             use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['first_name'] = 'Alex'
        logger.info("Logging in as System Admin Alex Montgomery")
        st.switch_page('pages/30_system_admin_home.py') #TODO IMPLEMENT THIS PAGE.



