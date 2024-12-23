import streamlit as st
from db_utils import fetch_username, add_problem, delete_problem, fetch_problems, fetch_submissions, fetch_submissions_by_problem
from analysis import analyze_class_feedback

# Teacher dashboard
def teacher_dashboard():
    st.header("先生用ページ")
    st.write("左のサイドバーから各項目にアクセスできます。")
    st.divider()

    # サイドバーに項目表示
    section = st.sidebar.radio("項目を選択", ["問題の追加", "問題一覧", "各問題の分析情報"])

    # 問題追加ボタン
    if section == "問題の追加":
        st.subheader("問題の追加")
        st.write("生徒に表示する問題を追加できます。")
        title = st.text_input("問題名")
        description = st.text_area("問題文の内容")
        input_example = st.text_input("入力例")
        output_example = st.text_input("出力例")
        display_order = 1

        if st.button("追加"):
            add_problem(title, description, input_example, output_example, display_order)
            st.success("問題が追加されました！")

    # 問題一覧ボタン
    elif section == "問題一覧":
        st.subheader("問題一覧")
        st.write("現在生徒に表示される問題の一覧です。")
        problems = fetch_problems()
        if problems:
            for problem in problems:
                st.subheader(problem['title'])
                st.write(problem['description'])
                st.write("入力例:")
                st.code(problem['input_example'], language="python")
                st.write("出力例:")
                st.code(problem['output_example'], language="python")
                if st.button("この問題を削除", key=f"delete_{problem['problem_id']}"):
                    delete_problem(problem['problem_id'])
                    st.success(f"'{problem['title']}' を削除しました。")
                st.divider()
        else:
            st.write("登録されている問題はありません。")

    # 各問題へアクセス
    elif section == "各問題の分析情報":
        st.subheader("各問題の分析情報")
        st.write("生徒が提出した解答を基に、GPT-4oを用いて分析します。")
        problems = fetch_problems()
        problem_titles = [problem['title'] for problem in problems]
        selected_problem_title = st.selectbox("問題を選択", problem_titles)

        # 選択された問題を取得
        selected_problem = next(problem for problem in problems if problem['title'] == selected_problem_title)

        st.divider()

        # 問題を表示
        st.subheader(selected_problem['title'])
        st.write(selected_problem['description'])
        st.write("入力例:")
        st.code(selected_problem['input_example'], language="python")
        st.write("出力例:")
        st.code(selected_problem['output_example'], language="python")

        st.divider()

        # 提出結果の総評
        st.subheader("提出結果の総評")

        if st.button("総評を生成"):
            submissions = fetch_submissions_by_problem(selected_problem['problem_id'])
            if submissions:
                feedbacks = [submission['feedback'] for submission in submissions]

                class_feedback = analyze_class_feedback(feedbacks)
                st.write(class_feedback)

            else:
                st.write("学生の回答がありません。")

        st.divider()

        # 提出結果一覧
        st.subheader("提出結果一覧")
        submissions = fetch_submissions()
        for submission in submissions:
            username = fetch_username(submission['user_id'])
            st.write(f"学生ユーザ名: {username}")
            st.write("解答:")
            st.code(submission['code'], language="python")
            st.write("実行結果:")
            st.code(submission['result'])
            st.write(f"フィードバック: {submission['feedback']}")
            st.divider()
