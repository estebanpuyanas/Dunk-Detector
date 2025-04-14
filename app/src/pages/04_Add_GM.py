import streamlit as st
from modules.nav import SideBarLinks
import mysql.connector

# Set page layout
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Add New General Manager")

def get_connection():
    return mysql.connector.connect(
        host="mysql_db",         # or "db", either works inside Docker network
        user="root",
        password="rootpass",
        database="dunkdector"
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
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals():
                    conn.close()

