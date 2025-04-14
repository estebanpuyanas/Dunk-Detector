import streamlit as st
from modules.nav import SideBarLinks

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Add New General Manager")

# Form
with st.form("gm_form"):
    st.subheader("New GM Info")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    team_id = st.number_input("Team ID", min_value=1, step=1)

    submit = st.form_submit_button("Add GM")

    if submit:
        if not (first_name and last_name and email and team_id):
            st.warning("Please fill in all fields.")
        else:
            insert_query = """
                    INSERT INTO general_managers (firstName, lastName, email, teamId)
                    VALUES (%s, %s, %s, %s)
                """
            values = (first_name, last_name, email, int(team_id))

            st.success(f"GM '{first_name} {last_name}' added successfully!")