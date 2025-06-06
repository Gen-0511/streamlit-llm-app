import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# --- OpenAI APIキーは Streamlit Cloud の secrets.toml に設定する ---
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# --- LLM設定（LangChain）---
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# --- 専門家のプロンプト定義 ---
expert_prompts = {
    "栄養士": "あなたはプロの栄養士です。ユーザーの質問に対して、科学的根拠のあるアドバイスを行ってください。",
    "ビジネスコンサルタント": "あなたは一流のビジネスコンサルタントです。質問に対して、論理的かつ実践的な戦略を提案してください。",
    "歴史研究家": "あなたは歴史に精通した専門家です。ユーザーの質問に対して、時代背景や事実に基づいた説明をしてください。",
}

# --- LLM応答生成関数 ---
def generate_response(expert_type, user_input):
    system_message = SystemMessage(content=expert_prompts[expert_type])
    human_message = HumanMessage(content=user_input)
    response = llm([system_message, human_message])
    return response.content

# --- Streamlit UI ---
st.set_page_config(page_title="専門家に聞いてみよう！", layout="centered")

st.title("🧠 専門家AIチャット")
st.markdown("以下のフォームに質問を入力し、相談したい専門家を選んでください。LLMがその専門家になりきってお答えします。")

# --- 専門家選択 ---
expert_type = st.radio("相談する専門家を選択してください：", list(expert_prompts.keys()))

# --- 質問入力 ---
user_input = st.text_area("質問を入力してください", height=150)

# --- 応答表示 ---
if st.button("質問する"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("専門家が回答中..."):
            answer = generate_response(expert_type, user_input)
        st.success("✅ 回答結果")
        st.write(answer)
