import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Add New General Manager")

# Form
with st.form("gm_form"):
    st.subheader("New GM Info")

    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")
    last_name = st.text_input("Last Name")
    mobile = st.text_input("Phone Number")
    email = st.text_input("Email")
    team_id = st.number_input("Team ID", min_value=1, step=1)

    submit = st.form_submit_button("Add GM")

    if submit:
        if not (first_name and last_name and email and team_id):
            st.warning("Please fill in all fields.")
        else:
            insert_query = """
                    INSERT INTO general_managers (firstName, middleName, lastName, mobile, email, teamId)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            values = (first_name, middle_name, last_name, mobile, email, int(team_id))

            user_payload = {
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "mobile": mobile,
            "email": email,
            "role": "general manager"
            }
            # try:
            #     response = requests.post("http://api:4000/users_routes.py", json=user_payload)
            #     if response.status_code == 200:
            #         st.success(f"GM '{first_name} {middle_name} {last_name}' added successfully!")
            #     else:
            #         st.error(f"Failed to add GM to users. Status: {response.status_code}, Error: {response.text}")
            # except Exception as e:
            #     st.error(f"Error connecting to user API: {e}")
            try:
                response = requests.post("http://api:4000/u/users").json()
            except:
                st.write("Didn't work")
            
            