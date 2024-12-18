import sqlite3
import streamlit as st

# データベース接続用関数
def authenticate_user(user_name, password):
    if user_name == st.secrets["login"]["name"] and password == st.secrets["login"]["pass"]:
        return True, 1

    conn = sqlite3.connect("student_model.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password, id FROM users WHERE name = ?", (user_name,))
    result = cursor.fetchone()

    conn.close()

    # 認証成功がTrue
    if result and result[0] == password:
        st.session_state["user_id"] = result[1]
        return True, 0
    return False, 0

# ログインフォーム
def login_form():
    user_name = st.text_input("ユーザ名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        # 認証処理
        success, admin = authenticate_user(user_name, password)
        if success:
            st.session_state["authenticated"] = True
            st.session_state["admin"] = admin
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが間違っています。")
