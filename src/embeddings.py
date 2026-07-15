import os

from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings

load_dotenv()


def get_embedding_model():

    return OllamaEmbeddings(
        model=os.getenv(
            "EMBEDDING_MODEL",
            "nomic-embed-text"
        ),
        base_url=os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434"
        )
    )