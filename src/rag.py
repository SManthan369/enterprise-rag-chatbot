from src.chatbot import get_llm
from src.retriever import get_retriever


class RAGChatbot:
    def __init__(self):
        self.llm = get_llm()
        self.retriever = get_retriever()

    def ask(self, question: str) -> str:
        docs = self.retriever.invoke(question)

        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context, say:
"I couldn't find that information in the document."

Context:
{context}

Question:
{question}

Answer:
"""

        return self.llm.invoke(prompt)