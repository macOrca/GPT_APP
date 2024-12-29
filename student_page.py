import streamlit as st
from db_utils import fetch_problems, save_submission
from analysis import execute_code, analyze_submission, response_chatbot


def code_form():
    problems = fetch_problems()
    if problems:
        # サイドバーで問題を選択
        problem_titles = [problem['title'] for problem in problems]
        selected_problem_title = st.sidebar.selectbox("問題を選択", problem_titles)

        # 選択された問題を取得
        selected_problem = next(problem for problem in problems if problem['title'] == selected_problem_title)

        # 問題を表示
        st.subheader(selected_problem['title'])
        st.write(selected_problem['description'])
        st.write("入力例:")
        st.code(selected_problem['input_example'], language="python")
        st.write("出力例:")
        st.code(selected_problem['output_example'], language="python")
        submitted_code = st.text_area("解答のコードを入力してください", key=selected_problem['problem_id'])
        if st.button("提出", key=f"submit_{selected_problem['problem_id']}"):
            output_result = execute_code(submitted_code, selected_problem['input_example'])
            feedback = analyze_submission(selected_problem['description'], selected_problem['input_example'], selected_problem['output_example'], submitted_code, output_result)
            save_submission(st.session_state.user_id, selected_problem['problem_id'], submitted_code, output_result, feedback)
            st.write("問題が提出されました!")
            st.write("提出したコード:")
            st.code(submitted_code, language="python")
            st.write("実行結果: 上の入力例をあなたのコードで実行した結果です。")
            st.code(output_result)
            st.write("フィードバック:")
            st.write(feedback)
    else:
        st.write("練習問題はありません。")

def chatbot():
    #入力欄用のカスタムCSS
    chat_input_style = f"""
    <style>
        .stChatInput {{
            position: fixed;
            bottom: 3rem;
        }}
    </style>
    """
    st.markdown(chat_input_style, unsafe_allow_html=True)

    # メッセージの初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "こんにちは。質問があれば、下の入力欄に入力してください。"}]

    # あれば、過去のメッセージを表示
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    # ユーザー入力の取得
    user_input= st.chat_input("質問などを入力")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)

        # GPTの応答を取得
        gpt_reply = response_chatbot()

        # GPTの返答を追加
        st.session_state.messages.append({"role": "assistant", "content": gpt_reply})
        st.chat_message("assistant").markdown(gpt_reply)

# Student dashboard
def student_dashboard():
    col_form, col_chatbot = st.columns(spec=2, gap="medium")

    with col_form:
        st.header("解答提出ページ")
        st.write("以下の練習問題を解き、解答のコードを提出してください。")
        st.write("他の問題は、左のサイドバーから選択できます。")
        st.divider()
        code_form()

    with col_chatbot:
        chatbot()
