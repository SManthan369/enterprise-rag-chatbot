from src.loader import load_pdf
from src.splitter import split_documents
from src.embeddings import get_embedding_model
from src.vectorstore import create_vector_store


def create_index(pdf_path):

    print("Loading document...")

    documents = load_pdf(pdf_path)

    print("Splitting document...")

    chunks = split_documents(documents)

    print("Creating embeddings...")

    embeddings = get_embedding_model()

    print("Creating FAISS index...")

    db = create_vector_store(
        chunks,
        embeddings
    )

    return db