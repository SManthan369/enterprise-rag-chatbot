from src.loader import load_pdf
from src.splitter import split_documents
from src.embeddings import get_embedding_model
from src.vectorstore import create_vector_store


# Load PDF
documents = load_pdf(
    "data/handbook.pdf"
)

print("Pages:", len(documents))


# Split documents
chunks = split_documents(
    documents
)

print("Chunks:", len(chunks))


# Create embeddings
embedding_model = get_embedding_model()

print("Embedding model loaded")


# Create FAISS database
db = create_vector_store(
    chunks,
    embedding_model
)

print("FAISS database created")