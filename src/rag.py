from src.chatbot import get_llm
from src.retriever import get_retriever


class RAGChatbot:

    def __init__(self):
        self.llm = get_llm()
        self.retriever = get_retriever()

    def ask(self, question):

        docs = self.retriever.invoke(question)

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
You are an Enterprise AI Assistant.

Answer ONLY using the provided context.

If the answer is unavailable, reply:

"I couldn't find that information in the document."

Context:
{context}

Question:
{question}

Answer:
"""

        answer = self.llm.invoke(prompt)

        return answer, docs