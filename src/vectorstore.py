from langchain_community.vectorstores import FAISS
import os


def create_vector_store(chunks, embeddings):

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    save_path = "faiss_index"

    os.makedirs(save_path, exist_ok=True)

    vectorstore.save_local(save_path)

    print(f"FAISS index saved to: {os.path.abspath(save_path)}")

    return vectorstore


def load_vector_store(embeddings):

    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )