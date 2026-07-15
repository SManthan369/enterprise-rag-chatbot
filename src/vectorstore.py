from langchain_community.vectorstores import FAISS
import os
import time


def create_vector_store(chunks, embeddings):

    max_retries = 5

    for attempt in range(max_retries):

        try:

            vectorstore = FAISS.from_documents(
                chunks,
                embeddings
            )

            save_path = "faiss_index"

            os.makedirs(save_path, exist_ok=True)

            vectorstore.save_local(save_path)

            print(f"FAISS index saved to: {os.path.abspath(save_path)}")

            return vectorstore

        except Exception as e:

            error = str(e)

            if "RESOURCE_EXHAUSTED" in error or "429" in error:

                wait_time = min(15 * (attempt + 1), 60)

                print(f"\n⚠ Gemini rate limit reached.")
                print(f"Retrying in {wait_time} seconds...\n")

                time.sleep(wait_time)

            else:
                raise

    raise RuntimeError("Failed to create vector store after multiple retries.")


def load_vector_store(embeddings):

    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )