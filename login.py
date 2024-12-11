import streamlit as st

# ログインフォーム
def login_form():
    user_name = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button('ログイン'):
        # 簡易的な認証処理
        if user_name == "admin" and password == "password":
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが間違っています。")
