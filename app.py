import streamlit as st
import os
from cordform import cord_form
from chatbot import gpt_chatbot
from login import login_form
from database import initialize_database

def main():
    # データベースの初期設定
    if not os.path.exists("student_model.db"):
        initialize_database()

    # ログイン状態の初期化
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "admin" not in st.session_state:
        st.session_state["admin"] = False


    # ログインしていない場合はログインフォームを表示
    if not st.session_state["authenticated"]:
        login_form()

    else:
        # カラム設定
        st.set_page_config(layout="wide")
        col_cordform, col_chatbot = st.columns(spec=2, gap="medium")

        with col_cordform:
            cord_form()

        with col_chatbot:
            gpt_chatbot()

if __name__ == "__main__":
    main()
