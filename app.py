import streamlit as st
import os

from src.rag import RAGChatbot
from src.indexer import create_index


# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Enterprise AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Enterprise AI Document Assistant")
st.caption(
    "Upload documents and ask questions using Retrieval-Augmented Generation"
)


# ------------------------------
# PDF Upload Section
# ------------------------------

st.sidebar.header("📄 Document Upload")


uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


if uploaded_file:

    os.makedirs(
        "data/uploads",
        exist_ok=True
    )

    file_path = (
        f"data/uploads/{uploaded_file.name}"
    )


    with open(file_path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )


    st.sidebar.success(
        "PDF uploaded successfully"
    )


    if st.sidebar.button(
        "Create Knowledge Base"
    ):

        with st.spinner(
            "Processing document..."
        ):

            create_index(file_path)


        # Reload chatbot with new FAISS index
        st.session_state.bot = RAGChatbot()


        st.sidebar.success(
            "Document indexed successfully!"
        )



# ------------------------------
# Initialize Chatbot
# ------------------------------

if "bot" not in st.session_state:

    with st.spinner(
        "Loading AI Assistant..."
    ):

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

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


        if (
            message["role"] == "assistant"
            and "sources" in message
        ):

            with st.expander(
                "📄 View Sources"
            ):

                for doc in message["sources"]:

                    page = (
                        doc.metadata.get("page", 0)
                        + 1
                    )

                    source = doc.metadata.get(
                        "source",
                        "Unknown"
                    )


                    st.markdown(
                        f"**📄 File:** `{source}`"
                    )

                    st.markdown(
                        f"**📑 Page:** {page}"
                    )

                    st.info(
                        doc.page_content[:250]
                        + "..."
                    )



# ------------------------------
# Chat Input
# ------------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)


if question:


    # User message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )



    # AI Response

    with st.chat_message(
        "assistant"
    ):


        with st.spinner(
            "Searching documents..."
        ):

            answer, docs = (
                st.session_state.bot.ask(
                    question
                )
            )


        st.markdown(
            answer
        )



        with st.expander(
            "📄 View Sources"
        ):


            for doc in docs:


                page = (
                    doc.metadata.get("page", 0)
                    + 1
                )

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )


                st.markdown(
                    f"**📄 File:** `{source}`"
                )

                st.markdown(
                    f"**📑 Page:** {page}"
                )


                st.info(
                    doc.page_content[:250]
                    + "..."
                )



    # Save AI message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": docs
        }
    )