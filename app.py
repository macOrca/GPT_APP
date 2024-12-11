import streamlit as st
from cordform import cord_form
from chatbot import gpt_chatbot
from login import login_form

def main():
    # ログイン状態の初期化
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # ログインしていない場合はログインフォームを表示
    if not st.session_state['authenticated']:
        login_form()

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
