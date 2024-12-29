import streamlit as st
import subprocess
from openai import OpenAI

# OpenAIのAPIキーを設定
client = OpenAI(api_key = st.secrets["openai"]["OPENAI_API_KEY"])

# GPTの初期設定
gpt_model = "gpt-4o"

def execute_code(submitted_code, input_data):
    try:
        # 入力データをファイルに保存（必要なら）
        with open("input.txt", "w") as f:
            f.write(input_data)

        # 提出コードをファイルに保存
        with open("submitted_code.py", "w") as f:
            f.write(submitted_code)

        # 提出コードを実行
        result = subprocess.run(
            ["python", "submitted_code.py"],
            input=input_data,
            text=True,
            capture_output=True
        )
        return result.stdout  # 実行結果を返す
    except Exception as e:
        return f"実行時にエラーが発生しました。エラー: {str(e)}"


def analyze_submission(problem_description, input_example, output_example, code, execution_result):
    prompt = f"""
    問題文:
    {problem_description}

    入力例:
    {input_example}

    出力例:
    {output_example}

    提出されたコード:
    {code}

    提出されたコードの実行結果:
    {execution_result}

    上記の内容は日本の高校における情報Iの授業で作成された解答です。この内容を基に次の内容を端的な内容で生成してください。
    <feedback>: コードを評価してください。
    <issues>: コードの問題点を指摘してください。
    <causes>: 問題がおきた原因を推定してください。
    <guidance>: この生徒に必要と考えられる指導内容を提案してください。
    <understanding>: 生徒の理解度を0.0から1.0の範囲で推定し、数値のみを出力してください。

    #出力形式(<>の内容のみ出力):
    <feedback>, <issues>, <causes>, <guidance>, <understanding>
    """
    response = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": "あなたは優秀なプログラミング教育の先生です。"},
            {"role": "user", "content": prompt},
        ]
    )
    feedback = response.choices[0].message.content
    return feedback

def analyze_class_feedback(feedbacks):
    prompt = f"""
    以下はプログラミングの問題に対するクラス全体のフィードバックです：

    {', '.join(feedbacks)}

    クラス全体のパフォーマンスを要約し、よく見られる間違いを特定し、改善点を簡潔かつ専門的に提案してください。
    """
    response = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": "あなたは優秀なプログラミング教育の先生です。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def response_chatbot():

        # GPTの応答を取得
        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
            ]
        )
        return response.choices[0].message.content
