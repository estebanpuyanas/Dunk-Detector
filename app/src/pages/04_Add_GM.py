import streamlit as st
import mysql.connector
from modules.nav import SideBarLinks

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Add New General Manager")

# Session role check (optional safety check)
if st.session_state["role"] != "system_admin":
    st.error("Access Denied: You do not have permission to view this page.")
    st.stop()

# DB connection setup
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="dunk_detector"
    )

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
            try:
                conn = get_connection()
                cursor = conn.cursor()

                insert_query = """
                    INSERT INTO general_managers (firstName, lastName, email, teamId)
                    VALUES (%s, %s, %s, %s)
                """
                values = (first_name, last_name, email, int(team_id))
                cursor.execute(insert_query, values)
                conn.commit()

                st.success(f"GM '{first_name} {last_name}' added successfully!")
            except mysql.connector.Error as err:
                st.error(f"Database error: {err}")
            finally:
                cursor.close()
                conn.close()
