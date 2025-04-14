import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Update General Manager Info")

with st.form("update_gm_form"):
    st.subheader("Enter New Info for a User")

    user_id = st.number_input("User ID", min_value=1, step=1)
    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")
    last_name = st.text_input("Last Name")
    mobile = st.text_input("Phone Number")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["general manager", "coach", "player", "admin"])

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

            try:
                response = requests.put(
                    f"http://host.docker.internal:4000/users_routes.py/{int(user_id)}",
                    json=updated_user
                )

                if response.status_code == 200:
                    st.success(f"User with ID {user_id} updated successfully!")
                elif response.status_code == 404:
                    st.error(f"No user found with ID {user_id}.")
                else:
                    st.error(f"Failed to update user. Status: {response.status_code}, Error: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to user API: {e}")