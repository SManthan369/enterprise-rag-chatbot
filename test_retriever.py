from src.retriever import get_retriever

retriever = get_retriever()

docs = retriever.invoke(
    "How many annual leaves are employees entitled to?"
)

for i, doc in enumerate(docs):

    print("=" * 50)

    print(f"Chunk {i+1}")

    print(doc.page_content[:300])