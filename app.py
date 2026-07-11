import streamlit as st
from src.rag import RAGChatbot

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Enterprise AI Document Assistant")

if "bot" not in st.session_state:
    st.session_state.bot = RAGChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask something...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = st.session_state.bot.ask(question)

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )