import streamlit as st
import subprocess
from openai import OpenAI
from pydantic import BaseModel

# OpenAIのAPIキーを設定
client = OpenAI(api_key = st.secrets["openai"]["OPENAI_API_KEY"])

# GPTの初期設定
gpt_model = "gpt-4o"

class Feedback(BaseModel):
    problem_understanding: str
    algorithm_design: str
    code_implementation: str
    execution_result: str
    error_point: str
    error_inference: str
    answer_result: str
    feedback: str

class User_Profile(BaseModel):
    understanding: str
    misunderstanding: str

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

def response_chatbot(problem_description, sample_code, input_example, output_example, code, execution_result, feedback, user_profile):
    prompt = f"""
    問題文:
    {problem_description}

    参考コード:
    {sample_code}

    入力例:
    {input_example}

    出力例:
    {output_example}

    提出されたコード:
    {code}

    提出されたコードの実行結果:
    {execution_result}

    フィードバック:
    {feedback}

    学習者の理解しているトピック:
    {user_profile[0]}

    学習者の理解していないトピック:
    {user_profile[1]}

    内容を更新しました。上記の内容を考慮し、ユーザの質問に答えてください。ユーザは高校生を想定し、高校生が理解できているように簡潔で専門用語の少ない内容で回答してください。また回答する際に、最低限の文章量で直接正解を示さず、ユーザが正しい回答にたどり着くためのヒントを示してください。
    """

    problem_message = {
        "role": "system",
        "content": prompt
    }

    chat_messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

    # problem_messageを最後の1つ前に挿入
    insert_position = len(chat_messages)  # 最後の要素の位置
    chat_messages.insert(insert_position - 1, problem_message)  # 1つ前に挿入

    # GPTの応答を取得
    response = client.chat.completions.create(
        model=gpt_model,
        messages=chat_messages
    )

    feedback = response.choices[0].message.content
    analyze_user_feedback(feedback, user_profile)

    return feedback

def analyze_submission(problem_description, sample_code, input_example, output_example, code, execution_result, user_profile):
    prompt = f"""
    問題文:
    {problem_description}

    参考コード:
    {sample_code}

    入力例:
    {input_example}

    出力例:
    {output_example}

    提出されたコード:
    {code}

    提出されたコードの実行結果:
    {execution_result}

    上記の内容に基づいて、以下の指示に従ってください。高校生にもわかるように、専門用語を使わず、平易で要点を絞った表現にしてください。まず、問題の理解、アルゴリズム設計、コード実装、実行結果の4点について、ユーザの理解状態を推測してください。次に、ユーザの誤った理解の内容を示し、原因を推測してください。加えて、解答について、「正解」、「不正解」のどちらかのみを回答してください。最後に、提出コードの良い点と誤った点をフィードバックしてください。回答にあたっては学習者の理解状態を考慮し、良い点は褒め、誤った点については誤りを含む場所を示し、直接の正解を示さず、ユーザが正解にたどり着くためのヒントのみを示してください。

    学習者の理解している内容:
    {user_profile[0]}

    学習者の理解していない内容:
    {user_profile[1]}

    """
    response = client.beta.chat.completions.parse(
        model=gpt_model,
        messages=[
            {"role": "system", "content": "あなたは優秀なプログラミング教育の先生です。生成は日本語で行ってください。"},
            {"role": "user", "content": prompt},
        ],
        response_format=Feedback
    )
    feedback = response.choices[0].message.parsed
    return feedback

def analyze_class_feedback(problem, code):
    prompt = f"""
    以下はプログラミングの問題と、それに対する各学生の回答集です：

    {problem}

    {', '.join(code)}

    専門用語を使わず、平易で要点を絞った表現にしてください。クラス全体の提出コードを分析し、学生全体で理解できている内容、理解に誤りがある内容を明確に提示してください。user_idが同じ回答は同じユーザの回答です。各学生ごとに結果の良いものを最終結果としてください。
    """
    response = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": "あなたは優秀なプログラミング教育の先生です。生成は日本語で行ってください。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def analyze_user_feedback(feedback, user_profile):
    prompt = f"""
    以下はユーザが提出したプログラミングの問題に対するフィードバックです。

    {feedback}

    ・前回の学習者モデル
    {user_profile}

    専門用語を使わず、平易で要点を絞った表現にしてください。このフィードバック(もしくは質問文)と、前回の学習者モデルの内容を統合し、抜けがないように注意して、ユーザが理解できている内容、理解に誤りがある内容を明確に箇条書きで提示してください。
    """
    response = client.beta.chat.completions.parse(
        model=gpt_model,
        messages=[
            {"role": "system", "content": "あなたは優秀なプログラミング教育の先生です。生成は日本語でお願いします。"},
            {"role": "user", "content": prompt}
        ],
        response_format=User_Profile
    )
    return response.choices[0].message.parsed
