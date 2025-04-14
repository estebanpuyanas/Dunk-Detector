import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Delete User")

# Form
with st.form("delete_user_form"):
    st.subheader("Delete User Info")

    user_id = st.number_input("Enter User ID to Delete", min_value=1, step=1)

    submit = st.form_submit_button("Delete User")

    if submit:
        try:
            response = requests.delete(f"http://api:4000/u/users/{int(user_id)}")

            if response.status_code == 200:
                st.success(f"User with ID '{user_id}' deleted successfully!")
            elif response.status_code == 404:
                st.error(f"No user found with ID '{user_id}'.")
            else:
                st.error(f"Failed to delete user. Status: {response.status_code}, Error: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to user API: {e}")