import streamlit as st
from db_utils import fetch_problems, save_submission
from analysis import execute_code, analyze_submission

# Student dashboard
def student_dashboard():
    st.header("解答提出ページ")
    st.write("以下の練習問題を解き、解答のコードを提出してください。")
    st.write("他の問題は、左のサイドバーから選択できます。")
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
