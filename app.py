import streamlit as st
import os
from student_page import student_dashboard
from teacher_page import teacher_dashboard
from auth import authenticate
from db_utils import init_db

# データベースの初期設定
if not os.path.exists("app.db"):
    init_db()

# Login state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.user_id = None

if not st.session_state.authenticated:
    st.header("情報I支援システム")
    st.subheader("ログイン")
    user_type = st.radio("ユーザータイプを選択してください:", ["生徒", "先生"])
    username = st.text_input("ユーザ名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        role = authenticate(username, password, user_type)
        if role:
            st.session_state.authenticated = True
            st.session_state.role = role
            st.rerun()
        else:
            st.error("ユーザ名またはパスワードが間違っています。")
else:
    if st.session_state.role == "teacher":
        user_type = "先生"
    elif st.session_state.role == "student":
        user_type = "学生"
    st.sidebar.header(f"{user_type}用ページ")

    if st.session_state.role == "student":
        student_dashboard()
    elif st.session_state.role == "teacher":
        teacher_dashboard()

    # ログアウトボタン
    if st.sidebar.button("ログアウト"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.user_id = None
        st.rerun()
