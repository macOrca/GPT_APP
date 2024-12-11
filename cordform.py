import streamlit as st

def cord_form():
    # コード入力エリア
    with st.form("user_form"):
        user_code = st.text_area(
            "Pythonコードを入力してください",
            height=200,
            key="user_code"
        )
        input_example = st.text_area(
            "(あれば)入力例を入力してください",
            height=100,
            key="input_example"
        )
        submitted = st.form_submit_button("提出")

    if submitted:
        # 入力されたコードと入力例を表示
        st.subheader("入力されたコード:")
        st.code(user_code, language="python")
        if input_example:
            st.subheader("指定された入力例:")
            st.text(input_example)

