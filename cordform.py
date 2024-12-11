import streamlit as st

def cord_form():
    # コード入力エリア
    st.subheader("Pythonコードを入力してください")
    user_code = st.text_area(
        "コード入力",
        height=200,
        placeholder="ここにPythonコードを入力してください",
        key="user_code"
    )

    # 入力例エリア
    st.subheader("入力例を指定してください")
    input_example = st.text_area(
        "入力例",
        height=100,
        placeholder="ここに入力例を指定してください（標準入力として利用されます）",
        key="input_example"
    )

    # 入力されたコードと入力例を表示（デバッグ目的）
    if user_code.strip():
        st.subheader("入力されたコード:")
        st.code(user_code, language="python")

    if input_example.strip():
        st.subheader("指定された入力例:")
        st.text(input_example)
