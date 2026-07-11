import os

from src.loader import load_pdf
from src.splitter import split_documents
from src.embeddings import get_embedding_model
from src.vectorstore import create_vector_store


def create_index(folder_path):

    all_documents = []


    for file in os.listdir(folder_path):

        if file.lower().endswith(".pdf"):

            pdf_path = os.path.join(
                folder_path,
                file
            )

            print(f"Loading: {pdf_path}")


            documents = load_pdf(
                pdf_path
            )


            all_documents.extend(
                documents
            )


    print(
        f"Total documents loaded: {len(all_documents)}"
    )


    chunks = split_documents(
        all_documents
    )


    print(
        f"Total chunks created: {len(chunks)}"
    )


    embeddings = get_embedding_model()


    vectorstore = create_vector_store(
        chunks,
        embeddings
    )


    return vectorstore