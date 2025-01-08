import streamlit as st
from db_utils import fetch_problems, save_submission, save_user_profile, fetch_user_profile
from analysis import execute_code, analyze_submission, response_chatbot, analyze_user_feedback

st.set_page_config(layout="wide")

# Student dashboard
def student_dashboard():
    feedback = []
    submitted_code = "未提出"
    output_result = "未提出"

    col_form, col_chatbot = st.columns(spec=2, gap="medium")

    with col_form:
        st.header("解答提出ページ")
        st.write("問1 ~ 4を解き、コードを提出してください。")
        st.write("他の問題は、左のサイドバーから選択できます。")
        st.write("回答は何度でも再提出できます。")
        st.write("**注意：コードの入力はメモ帳などからコピー＆ペーストでお願いします！**")
        st.divider()

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

            # 解答の提出
            submitted_code = st.text_area("解答のコードを入力してください", key=selected_problem['problem_id'], height=300)
            if st.button("提出", key=f"submit_{selected_problem['problem_id']}"):
                user_profile = fetch_user_profile(st.session_state.user_id)
                output_result = execute_code(submitted_code, selected_problem['input_example'])
                feedback = analyze_submission(selected_problem['description'], selected_problem['input_example'], selected_problem['output_example'], submitted_code, output_result, user_profile)
                save_submission(st.session_state.user_id, selected_problem['problem_id'], submitted_code, output_result, feedback)
                st.write("問題が提出されました!")
                st.write("提出したコード:")
                st.code(submitted_code, language="python")
                st.write("実行結果: 上の入力例をあなたのコードで実行した結果です。")
                st.code(output_result)
                if(feedback.answer_result == "正解"):
                    st.success("正解!")
                if(feedback.answer_result == "不正解"):
                    st.error("不正解のようです。")
                st.write("フィードバック:")
                st.write(feedback.feedback)
                st.write(feedback)
                user_profile = analyze_user_feedback(feedback, user_profile)
                save_user_profile(st.session_state.user_id, user_profile)
                st.write(user_profile)
                fetch_user_profile(st.session_state.user_id)
        else:
            st.write("練習問題はありません。")

    with col_chatbot:
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

            user_profile = fetch_user_profile(st.session_state.user_id)

            # GPTの応答を取得
            gpt_reply = response_chatbot(selected_problem['description'], selected_problem['input_example'], selected_problem['output_example'], submitted_code, output_result, feedback, user_profile)

            # GPTの返答を追加
            st.session_state.messages.append({"role": "assistant", "content": gpt_reply})
            st.chat_message("assistant").markdown(gpt_reply)
