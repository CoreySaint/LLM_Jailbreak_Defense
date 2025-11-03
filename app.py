import streamlit as st

st.set_page_config(page_title="LLM Defense Testing")
st.title("LLM Defense Testing")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

prompt = st.chat_input("Type your message here...")

if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = "placeholder until API implementation"
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
