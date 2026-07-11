from src.embeddings import get_embedding_model
from src.vectorstore import load_vector_store


def get_retriever():

    embeddings = get_embedding_model()

    db = load_vector_store(
        embeddings
    )

    return db.as_retriever(
        search_kwargs={"k": 3}
    )