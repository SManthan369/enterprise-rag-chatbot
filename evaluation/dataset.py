import json

from src.rag import RAGChatbot


def main():

    print("Loading Enterprise RAG...")

    bot = RAGChatbot()

    print("Loading evaluation dataset...")

    with open("evaluation/dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = []

    print(f"\nTotal Questions: {len(dataset)}\n")

    for i, sample in enumerate(dataset, start=1):

        question = sample["question"]
        ground_truth = sample["ground_truth"]

        print(f"[{i}/{len(dataset)}] {question}")

        answer, docs = bot.ask(question)

        # Convert AIMessage to string
        if hasattr(answer, "content"):
            answer_text = answer.content
        else:
            answer_text = str(answer)

        contexts = [
            doc.page_content
            for doc in docs
        ]

        results.append(
            {
                "question": question,
                "answer": answer_text,
                "ground_truth": ground_truth,
                "contexts": contexts,
            }
        )

    with open(
        "evaluation/results.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\n===================================")
    print("Evaluation dataset created!")
    print("Saved to: evaluation/results.json")
    print("===================================")


if __name__ == "__main__":
    main()