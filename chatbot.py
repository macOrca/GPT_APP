from openai import OpenAI
import streamlit as st

def gpt_chatbot():
    # OpenAIのAPIキーを設定
    client = OpenAI()
    client.api_key = st.secrets["openai"]["OPENAI_API_KEY"]

    # GPTの初期設定
    gpt_model = "gpt-4o"

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

    # セッション内のメッセージの初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
