import os
from langchain_ollama import OllamaEmbeddings

def get_embedding_model():
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )