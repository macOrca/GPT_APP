import streamlit as st
from cordform import cord_form
from chatbot import gpt_chatbot

# ログインフォーム
def show_login_form():
    user_name = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button('ログイン'):
        # 簡易的な認証処理
        if user_name == "admin" and password == "password":
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが間違っています。")

def main():
    # ログイン状態の初期化
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # ログインしていない場合はログインフォームを表示
    if not st.session_state['authenticated']:
        show_login_form()

    else:
        # カラム設定
        st.set_page_config(layout="wide")
        col_cord, col_chat = st.columns(spec=2, gap="medium")

        with col_cord:
            cord_form()

        with col_chat:
            gpt_chatbot()

if __name__ == "__main__":
    main()
