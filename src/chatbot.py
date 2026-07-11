from langchain_ollama import OllamaLLM


def get_llm():

    llm = OllamaLLM(
        model="gemma2:2b"
    )

    return llm