import streamlit as st
from datetime import datetime
from utils import AiModelHelper
from dotenv import load_dotenv

st.set_page_config(page_title="LLM Defense Testing")
st.title("LLM Defense Testing")

load_dotenv()

st.sidebar.header("Model Configuration")

model_family = st.sidebar.selectbox(
    "Select Model Family",
    ["Gemini", "Qwen", "GPT"]
)

if model_family == "Gemini":
    version = st.sidebar.selectbox(
        "Select Gemini Version",
        ["gemini-2.0-flash", "gemini-2.0-pro", "gemini-2.5-flash", "gemini-2.5-pro"]
    )
elif model_family == "Qwen":
    version = st.sidebar.selectbox(
        "Select Qwen Version",
        ["qwen/qwen3-next-80b-a3b-thinking"]
    )
elif model_family == "GPT":
    version = st.sidebar.selectbox(
        "Select GPT Version",
        ["openai/gpt-oss-20b"]
    )
else:
    version = None

st.sidebar.warning("WARNING: Switching the model or version will clear chat history")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "prev_model" not in st.session_state:
    st.session_state.prev_model = model_family
if "prev_version" not in st.session_state:
    st.session_state.prev_version = version

if (st.session_state.prev_model != model_family) or (st.session_state.prev_version != version):
    st.session_state.messages = []
    st.session_state.prev_model = model_family
    st.session_state.prev_version = version

st.subheader("Chat Controls")

col1, col2 = st.columns([1, 1])

if st.session_state.messages:
    chat_text = f"{model_family}, {version}" + "\n\n".join(
        [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages]
    )
else:
    chat_text = "No chat history yet."

with col1:
    st.download_button(
        label="Download Chat History",
        data=chat_text.encode("utf-8"),
        file_name=f"chat_history_{datetime.now()}.txt",
        mime="text/plain",
        use_container_width=True
    )

@st.dialog("Confirm Chat Clear")
def confirm():
    st.write("Are you sure you want to clear the chat? You can download it first.")
    col_confirm, col_cancel = st.columns(2)

    with col_confirm:
        if st.button("Yes, Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_cancel:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

with col2:
    if st.button("Clear chat", use_container_width=True):
        confirm()

st.markdown('---')
                    
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your message here...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                helper = AiModelHelper(model_family)
                reply = helper.get_response(version, prompt)
            except Exception as e:
                reply = f"Error: {e}"

            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
