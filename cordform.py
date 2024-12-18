import streamlit as st
from chatbot import gpt_code_feedback

def cord_form():
    # 初期化
    if "submitted_code" not in st.session_state:
        st.session_state["submitted_code"] = ""

    if "submitted_input_example" not in st.session_state:
        st.session_state["submitted_input_example"] = ""

    # 生成問題エリア
    if "generated_problem" in st.session_state:
        st.subheader("生成問題:")
        st.text(st.session_state["generated_problem"])

    # コード入力エリア
    with st.form("user_form"):
        user_code = st.text_area(
            "Pythonコードを入力してください",
            height=200,
            key="user_code"
        )
        problem = st.text_area(
            "(あれば)問題文を入力してください",
            height=200,
            key="problem"
        )
        input_example = st.text_area(
            "(あれば)入力例を入力してください",
            height=100,
            key="input_example"
        )
        submitted = st.form_submit_button("提出")

    if submitted:
        # 入力内容を保存
        st.session_state["submitted_user_code"] = user_code
        st.session_state["submitted_problem"] = problem
        st.session_state["submitted_input_example"] = input_example

        # 入力されたコードと入力例を表示
        st.subheader("入力されたコード:")
        st.code(st.session_state["submitted_user_code"], language="python")

        if "submitted_problem" in st.session_state:
            st.subheader("入力された問題:")
            st.text(st.session_state["submitted_problem"])

        if "submitted_input_example" in st.session_state:
            st.subheader("指定された入力例:")
            st.text(st.session_state["submitted_input_example"])

        # チャットボット側へフィードバックの要請
        gpt_code_feedback(user_code, problem, input_example)

