from openai import OpenAI
import streamlit as st

# OpenAIのAPIキーを設定
client = OpenAI(api_key = st.secrets["openai"]["OPENAI_API_KEY"])

# GPTの初期設定
gpt_model = "gpt-4o"

def gpt_chatbot():
    #入力欄用のカスタムCSS
    chat_input_style = f"""
    <style>
        .stChatInput {{
            position: fixed;
            bottom: 3rem;
            z-index:1;
        }}
    </style>
    """
    st.markdown(chat_input_style, unsafe_allow_html=True)

    # メッセージの初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "こんにちは。"}]

    # あれば、過去のメッセージを表示
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    # ユーザー入力の取得
    user_input= st.chat_input("質問などを入力")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)

        # GPTの応答を取得
        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
            ]
        )
        gpt_reply = response.choices[0].message.content

        # GPTの返答を追加
        st.session_state.messages.append({"role": "assistant", "content": gpt_reply})
        st.chat_message("assistant").markdown(gpt_reply)

def gpt_code_feedback(user_code, user_problem, user_input):
    # 入力フォームの内容を取得
    code = user_code
    problem = user_problem
    input_example = user_input
    if code:
        gpt_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # プロンプトを追加
        gpt_messages.append(
            {"role": "system", "content": "日本の高校生がわかるように回答してください。\nユーザが質問するまで、修正コードを含めないでください。\n「理解できていること」と「理解できていないこと」は箇条書きにし、次のように記述してください。\n\n[該当コード]: [状況]\n解答は次の形式で[]を置き換えて記述してください。\n理解できていること[]\n理解できていないこと[]\nコードのフィードバック[]"})
        gpt_messages.append(
            {"role": "user", "content": f"以下のコードに対するフィードバックをお願いします。\n問題文: {problem}\n解答: {code}\n入力例: {input_example}"}
            )

        # GPTの応答を取得
        response = client.chat.completions.create(
            model=gpt_model,
            messages=gpt_messages
        )
        gpt_reply = response.choices[0].message.content

        # GPTの返答を追加
        st.session_state.messages.append({"role": "assistant", "content": gpt_reply})

        return gpt_reply

