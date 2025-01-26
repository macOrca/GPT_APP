import streamlit as st
from db_utils import fetch_username, add_problem, delete_problem, fetch_problems, fetch_submissions_by_problem, fetch_users
from analysis import analyze_class_feedback

# Teacher dashboard
def teacher_dashboard():
    st.header("先生用ページ")
    st.write("左のサイドバーから各項目にアクセスできます。")
    st.divider()

    # サイドバーに項目表示
    section = st.sidebar.radio("項目を選択", ["各問題の分析情報", "学生ごとの分析情報", "問題の追加", "問題一覧"])

    # 各問題へアクセス
    if section == "各問題の分析情報":
        st.subheader("各問題の分析情報")
        st.write("問題別の学生による提出結果とその分析を表示します。")
        problems = fetch_problems()
        problem_titles = [problem['title'] for problem in problems]
        selected_problem_title = st.selectbox("問題を選択", problem_titles)

        # 選択された問題を取得
        selected_problem = next(problem for problem in problems if problem['title'] == selected_problem_title)

        st.divider()

        # 問題を表示
        st.subheader(selected_problem['title'])
        st.write(selected_problem['description'])
        if(selected_problem['sample_code'] != "" and selected_problem['sample_code'] != None):
            st.write("参考コード:")
            st.code(selected_problem['sample_code'], language="python")
        if(selected_problem["input_example"] != "" or selected_problem["output_example"] != ""):
            st.write("入力例:")
            st.code(selected_problem['input_example'], language="python")
            st.write("出力例:")
            st.code(selected_problem['output_example'], language="python")

        st.divider()

        # 提出結果の総評
        st.subheader("提出結果の総評")

        if st.button("総評を確認"):
            submissions = fetch_submissions_by_problem(selected_problem['problem_id'])
            if submissions:
                code = [f"user_id: {submission['user_id']}\n{submission['code']}" for submission in submissions]

                class_feedback = analyze_class_feedback(selected_problem, code)
                st.write(class_feedback)

            else:
                st.write("生徒の回答がありません。")

        st.divider()

        # 提出結果一覧
        st.subheader("提出結果一覧")
        submissions = fetch_submissions_by_problem(selected_problem["problem_id"])
        for submission in submissions:
            username = fetch_username(submission['user_id'])
            st.write(f"生徒ユーザ名: {username}")
            st.write("解答:")
            st.code(submission['code'], language="python")
            st.write("実行結果:")
            st.code(submission['output'], language="python")
            st.markdown(f"**:red[{submission["answer_result"]}]**")
            if(submission["answer_result"] != "正解"):
                st.write(f"間違った点: {submission['error_point']}")
                st.write(f"原因の推測: {submission['error_inference']}")
            st.divider()

    # 問題追加ボタン
    elif section == "問題の追加":
        st.subheader("問題の追加")
        st.write("生徒に表示する問題を追加できます。")
        title = st.text_input("問題名")
        description = st.text_area("問題文の内容", height=200)
        sample_code = st.text_area("参考コード", height=300)
        input_example = st.text_area("入力例")
        output_example = st.text_area("出力例")

        if st.button("追加"):
            add_problem(title, description, sample_code, input_example, output_example)
            st.success("問題が追加されました！")

        st.divider()

        with open("app.db", "rb") as file:
            st.download_button(
                label="データベースファイルのダウンロード",
                data=file,
                file_name="app.db",
                mime="application/octet-stream"
            )

    elif section == "生徒ごとの分析情報":
        st.subheader("生徒ごとの分析情報")
        st.write("生徒ごとの理解できている内容と、理解に誤りがある内容のまとめです。")
        st.divider()

        users = fetch_users()
        for user in users:
            st.write(f"生徒ユーザ名: {user["username"]}")
            st.write("理解できている内容:")
            st.write(user["understanding"])
            st.write("理解に誤りがある内容:")
            st.write(user["misunderstanding"])
            st.divider()

    # 問題一覧ボタン
    elif section == "問題一覧":
        st.subheader("問題一覧")
        st.write("現在生徒に表示される問題の一覧です。")
        problems = fetch_problems()
        if problems:
            for problem in problems:
                st.subheader(problem['title'])
                st.write(problem['description'])
                st.write("参考コード")
                st.code(problem['sample_code'], language="python")
                st.write("入力例:")
                st.code(problem['input_example'], language="python")
                st.write("出力例:")
                st.code(problem['output_example'], language="python")
                #if st.button("この問題を削除", key=f"delete_{problem['problem_id']}"):
                #    delete_problem(problem['problem_id'])
                #    st.success(f"'{problem['title']}' を削除しました。")
                st.divider()
        else:
            st.write("登録されている問題はありません。")
