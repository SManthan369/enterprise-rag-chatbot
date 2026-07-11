import streamlit as st
from src.rag import RAGChatbot

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Enterprise AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise AI Document Assistant")
st.caption("Ask questions about your PDF documents using RAG")

# ------------------------------
# Initialize Chatbot
# ------------------------------
if "bot" not in st.session_state:
    with st.spinner("Loading AI Assistant..."):
        st.session_state.bot = RAGChatbot()

# ------------------------------
# Initialize Chat History
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# Display Previous Messages
# ------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Show sources only for assistant messages
        if (
            message["role"] == "assistant"
            and "sources" in message
        ):

            with st.expander("📄 View Sources"):

                for doc in message["sources"]:

                    page = doc.metadata.get("page", 0) + 1
                    source = doc.metadata.get("source", "Unknown")

                    st.markdown(f"**📄 File:** `{source}`")
                    st.markdown(f"**📑 Page:** {page}")

                    st.info(doc.page_content[:250] + "...")

# ------------------------------
# User Input
# ------------------------------
question = st.chat_input("Ask a question about your documents...")

if question:

    # Display user message
    st.chat_message("user").markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Searching documents..."):

            answer, docs = st.session_state.bot.ask(question)

        st.markdown(answer)

        # Display retrieved sources
        with st.expander("📄 View Sources"):

            for doc in docs:

                page = doc.metadata.get("page", 0) + 1
                source = doc.metadata.get("source", "Unknown")

                st.markdown(f"**📄 File:** `{source}`")
                st.markdown(f"**📑 Page:** {page}")

                st.info(doc.page_content[:250] + "...")

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": docs
        }
    )