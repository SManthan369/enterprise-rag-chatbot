import time

from langsmith import traceable

from src.chatbot import get_llm
from src.retriever import get_retriever


class RAGChatbot:

    def __init__(self):
        self.llm = get_llm()
        self.retriever = get_retriever()


    @traceable(run_type="retriever", name="Document Retrieval")
    def retrieve(self, question):

        return self.retriever.invoke(question)


    @traceable(name="Prompt Builder")
    def build_prompt(self, question, docs):

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        return f"""
You are an Enterprise AI Assistant.

Answer ONLY using the information present in the provided context.

If the answer exists anywhere in the context,
answer it clearly and completely.

Only reply with:

"I couldn't find that information in the document."

if the answer truly does not appear in the context.

================ CONTEXT ================

{context}

=========================================

Question:
{question}

Answer:
"""


    @traceable(run_type="llm", name="Groq LLM")
    def generate(self, prompt):

        return self.llm.invoke(prompt)


    @traceable(name="Enterprise RAG Pipeline")
    def ask(self, question):

        overall_start = time.perf_counter()

        # ----------------------------------
        # Retrieval
        # ----------------------------------

        retrieval_start = time.perf_counter()

        docs = self.retrieve(question)

        retrieval_time = time.perf_counter() - retrieval_start


        # ---------- DEBUG : Retrieved Chunks ----------

        print("\n========== RETRIEVED CHUNKS ==========\n")

        if not docs:
            print("No documents retrieved.\n")

        for i, doc in enumerate(docs, start=1):

            print(f"Chunk {i}")

            print(f"Metadata : {doc.metadata}")

            print("-" * 70)

            print(doc.page_content)

            print("-" * 70)

            print()

        print("======================================\n")


        # ----------------------------------
        # Prompt
        # ----------------------------------

        prompt_start = time.perf_counter()

        prompt = self.build_prompt(
            question,
            docs
        )

        prompt_time = time.perf_counter() - prompt_start


        # ---------- DEBUG : Prompt ----------

        print("\n========== GENERATED PROMPT ==========\n")
        print(prompt)
        print("\n======================================\n")


        # ----------------------------------
        # LLM
        # ----------------------------------

        llm_start = time.perf_counter()

        answer = self.generate(prompt)

        llm_time = time.perf_counter() - llm_start


        overall_time = time.perf_counter() - overall_start


        print("\n========== PERFORMANCE ==========")
        print(f"Retrieval : {retrieval_time:.3f} sec")
        print(f"Prompt    : {prompt_time:.3f} sec")
        print(f"LLM       : {llm_time:.3f} sec")
        print(f"Total     : {overall_time:.3f} sec")
        print("=================================\n")


        return answer, docs