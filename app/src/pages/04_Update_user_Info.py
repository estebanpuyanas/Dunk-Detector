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

# Fetch all users
try:
    api_link = 'http://api:4000/u/users'  # API endpoint to get users
    response = requests.get(api_link)
    response.raise_for_status()  # Raise an exception for bad responses
    users = response.json()  # Assuming this returns a list of users
    
    # Check if users exist
    if users:
        user_options = [f"{user['id']} - {user['firstName']} {user['lastName']}" for user in users]
        selected_user = st.selectbox("Select a User to Update", user_options)
        
        # Extract the selected user's ID
        selected_user_id = int(selected_user.split(" ")[0])  # Extract ID from the string

        # Display user info fields for update
        with st.form("update_gm_form"):
            st.subheader(f"Update Info for User ID: {selected_user_id}")

            # Get the selected user's data (you can fill in the form with their current info)
            user_data = next(user for user in users if user['id'] == selected_user_id)
            
            first_name = st.text_input("First Name", value=user_data.get('firstName'))
            middle_name = st.text_input("Middle Name", value=user_data.get('middleName', ''))
            last_name = st.text_input("Last Name", value=user_data.get('lastName'))
            mobile = st.text_input("Phone Number", value=user_data.get('mobile', ''))
            email = st.text_input("Email", value=user_data.get('email'))
            role = st.selectbox("Role", ["general manager", "coach", "player", 'data analyst', "admin"], index=["general manager", "coach", "player", 'data analyst', "admin"].index(user_data.get('role')))

            submit = st.form_submit_button("Update User")

            if submit:
                if not (first_name and last_name and email and role):
                    st.warning("Please fill in all required fields.")
                else:
                    updated_user = {
                        "firstName": first_name,
                        "middleName": middle_name,
                        "lastName": last_name,
                        "mobile": mobile,
                        "email": email,
                        "role": role
                    }

                    # Make the API call to update the user
                    try:
                        api_link = f'http://api:4000/u/users/{selected_user_id}'  # API endpoint to update user
                        response = requests.put(api_link, json=updated_user)
                        response.raise_for_status()

                        if response.status_code == 200:
                            st.success(f"User with ID {selected_user_id} updated successfully!")
                        elif response.status_code == 404:
                            st.error(f"No user found with ID {selected_user_id}.")
                        else:
                            st.error(f"Failed to update user. Status: {response.status_code}, Error: {response.text}")

                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to user API: {e}")

    else:
        st.error("No users found.")
    
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching users: {e}")