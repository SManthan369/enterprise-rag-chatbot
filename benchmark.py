import time

from src.embeddings import get_embedding_model
from src.vectorstore import load_vector_store
from src.chatbot import get_llm


QUESTION = "What is Artificial Intelligence?"


print("=" * 60)
print("🚀 ENTERPRISE RAG BENCHMARK")
print("=" * 60)


# ----------------------------------------------------
# Embedding Benchmark
# ----------------------------------------------------

embeddings = get_embedding_model()

start = time.perf_counter()

query_embedding = embeddings.embed_query(QUESTION)

embedding_time = time.perf_counter() - start

print(f"\n✅ Query Embedding Time : {embedding_time:.3f} sec")


# ----------------------------------------------------
# FAISS Benchmark
# ----------------------------------------------------

db = load_vector_store(embeddings)

start = time.perf_counter()

docs = db.similarity_search_by_vector(
    query_embedding,
    k=3
)

faiss_time = time.perf_counter() - start

print(f"✅ FAISS Search Time    : {faiss_time:.3f} sec")


# ----------------------------------------------------
# Prompt
# ----------------------------------------------------

context = "\n\n".join(
    doc.page_content
    for doc in docs
)

prompt = f"""
Answer ONLY using the context.

Context:
{context}

Question:
{QUESTION}

Answer:
"""


# ----------------------------------------------------
# LLM Benchmark
# ----------------------------------------------------

llm = get_llm()

start = time.perf_counter()

answer = llm.invoke(prompt)

llm_time = time.perf_counter() - start

print(f"✅ LLM Generation Time : {llm_time:.3f} sec")

print("\nAnswer:\n")
print(answer)

print("\n" + "=" * 60)
print(f"Embedding : {embedding_time:.3f} sec")
print(f"FAISS     : {faiss_time:.3f} sec")
print(f"LLM       : {llm_time:.3f} sec")
print(f"TOTAL     : {embedding_time + faiss_time + llm_time:.3f} sec")
print("=" * 60)