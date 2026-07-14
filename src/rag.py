import time

from src.chatbot import get_llm
from src.retriever import get_retriever


class RAGChatbot:

    def __init__(self):
        self.llm = get_llm()
        self.retriever = get_retriever()

    def ask(self, question):

        overall_start = time.perf_counter()

        # Retrieval
        retrieval_start = time.perf_counter()
        docs = self.retriever.invoke(question)
        retrieval_time = time.perf_counter() - retrieval_start

        # Prompt creation
        prompt_start = time.perf_counter()

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

        prompt_time = time.perf_counter() - prompt_start

        # LLM
        llm_start = time.perf_counter()
        answer = self.llm.invoke(prompt)
        llm_time = time.perf_counter() - llm_start

        overall_time = time.perf_counter() - overall_start

        print("\n========== PERFORMANCE ==========")
        print(f"Retrieval : {retrieval_time:.3f} sec")
        print(f"Prompt    : {prompt_time:.3f} sec")
        print(f"LLM       : {llm_time:.3f} sec")
        print(f"Total     : {overall_time:.3f} sec")
        print("=================================\n")

        return answer, docs