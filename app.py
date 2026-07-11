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
    "Upload multiple documents and ask questions using Retrieval-Augmented Generation"
)


# ------------------------------
# PDF Upload Section
# ------------------------------

st.sidebar.header("📄 Document Upload")


uploaded_files = st.sidebar.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    upload_folder = "data/uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )


    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            upload_folder,
            uploaded_file.name
        )


        with open(file_path, "wb") as f:

            f.write(
                uploaded_file.getbuffer()
            )


    st.sidebar.success(
        f"{len(uploaded_files)} PDF(s) uploaded successfully"
    )


    if st.sidebar.button(
        "Create Knowledge Base"
    ):


        with st.spinner(
            "Processing documents and creating embeddings..."
        ):


            create_index(
                upload_folder
            )


        # Reload chatbot with new FAISS index

        st.session_state.bot = RAGChatbot()


        st.sidebar.success(
            "Knowledge base created successfully!"
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



    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": docs
        }
    )