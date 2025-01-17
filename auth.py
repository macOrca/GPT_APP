import streamlit as st
import sqlite3

def authenticate(username, password, user_type):
    if user_type == "先生":
        teacher_username = st.secrets["teacher"]["username"]
        teacher_password = st.secrets["teacher"]["password"]
        if username == teacher_username and password == teacher_password:
            return "teacher"
        else: None

    if user_type == "学生":
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, password FROM Users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            st.session_state.user_id = user[0]
            return "student"
        else: None
