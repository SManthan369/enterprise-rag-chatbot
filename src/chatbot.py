import os
from langchain_ollama import OllamaLLM

def get_llm():
    return OllamaLLM(
        model="gemma2:2b",
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )