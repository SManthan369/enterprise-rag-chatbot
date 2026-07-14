from src.rag import RAGChatbot

def main():
    print("=" * 50)
    print("Enterprise RAG Chat")
    print("Type 'exit' to quit")
    print("=" * 50)

    bot = RAGChatbot()

    while True:
        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer, docs = bot.ask(question)

        print("\nAssistant:")
        print(answer)

        print("\nSources:")
        for doc in docs:
            print(
                f"- {doc.metadata.get('source')} "
                f"(Page {doc.metadata.get('page', 0) + 1})"
            )

if __name__ == "__main__":
    main()